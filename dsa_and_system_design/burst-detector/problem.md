# The Problem: "The Burst Detector"

In a high-throughput system, we need to monitor API keys to ensure they aren't abusing the service.

The Task:
Given a stream of logs where each log contains a timestamp (in seconds) and an api_key, identify the first api_key that exceeds a threshold of N requests within any sliding window of M seconds.

Example:

Threshold (N): 3 requests

Window (M): 10 seconds

Logs:

{key: "A", time: 100}

{key: "A", time: 105}

{key: "B", time: 107}

{key: "A", time: 109} -> "A" is the first violator (3 requests at 100, 105, 109 are all within a 10s window).

## Approach

This is how the flow would look like:

- Advance Watermark: self.watermark = max(self.watermark, log.timestamp)

- Global Cleanup: * while self.expiry_queue.timestamp <= self.watermark:
* Pop the tuple.
* Delete that key from self.deques and self.key_to_expiry.

- Process Current Log:

    - Update History: Add log.timestamp to self.deques[log.key].
    - Sliding Window Clean: While self.deques[log.key] < log.timestamp - M: pop left.
    - Violation Check: If len(self.deques[log.key]) >= N: set self.first_violator.
    - Update Expiry Queue: * Remove (old_expiry, log.key) from SortedSet using your key_to_expiry map.
    - Add (log.timestamp + M, log.key) to SortedSet.
    - Update key_to_expiry[log.key] = log.timestamp + M.

## System design

- Data Structures:
    - Deques: For each API key, maintain a deque of timestamps to track request history within the sliding window.
    - SortedSet: A global sorted set to track the expiry times of API keys for efficient cleanup.
    - Hash Map: A mapping from API keys to their current expiry times for quick updates.

"This code works great on a single machine. But our API traffic is 1 million requests per second, which is too much for one CPU. How would you distribute this 'Burst Detector' across a cluster of servers while ensuring we still find the global 'First Violator'?"

Think about:

How do you ensure all logs for Key A go to the same server?

How do you track the "First Violator" across multiple servers?

What happens if one server crashes—does it lose all the request_log deques?

## Answer

- How do you ensure all logs for Key A go to the same server?

Use consistent hashing to route logs based on their API key. This ensures that all logs for a specific key are processed by the same server, allowing us to maintain accurate request counts and timestamps for that key.

- How do you track the "First Violator" across multiple servers?

Each server maintains its own "First Violator" based on the logs it processes. To find the global "First Violator," we can use a distributed coordination service (like ZooKeeper) or a shared database to store and update the current global "First Violator." Whenever a server identifies a new "First Violator," it updates this shared state where it writes the violation timestamp in the database, and all servers can read from it to determine if they have found a new global violator.

- What happens if one server crashes—does it lose all the request_log deques?

Instead of storing the request log deques locally in memory, we could store them in external state store liked `redis`. If a server crashes, the new server will continue reading from `redis` store. Additionally, using a distributed log system (like Kafka) to store incoming logs can help ensure that no data is lost, as the logs can be reprocessed by another server if one goes down.