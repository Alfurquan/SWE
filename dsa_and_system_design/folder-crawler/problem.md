# The Problem: The "Cloud Crawler"

Imagine you are building a tool that needs to audit permissions across a massive, nested cloud storage system (like Google Drive or S3).

The Task:
You are given a starting "Folder ID." You need to implement a function that crawls through this folder and all its sub-folders to find the total number of unique files that are "Publicly Accessible."

The Environment
You are provided with an API client that has two methods:

get_metadata(id): Returns an object containing:

is_folder: Boolean.

is_public: Boolean.

children: A list of IDs (only if it's a folder).

Constraint: Every API call takes a variable amount of time (10ms to 500ms) because of network latency.

---

## Approach

To solve the problem of counting the total number of unique publicly accessible files in a nested cloud storage system, we can use a depth-first search (DFS) approach. Here's how we can implement this:

- We would use a set to keep track of unique file IDs that are publicly accessible to avoid counting duplicates.
- We would define a recursive function that takes a folder ID as input, retrieves its metadata using the `get_metadata` API, and checks if it's a folder or a file.
- If it's a folder, we would recursively call the function for each of its children.
- If it's a file and is publicly accessible, we would add its ID to the set.
- To avoid calling the API multiple times for the same folder or file, we can maintain a visited set to track which IDs have already been processed.

---

## System design followups

1. Concurrency (The "Speed" Problem)
Since the bottleneck is the 500ms network delay per API call, we need to do many calls at once.

The Problem: If multiple threads are trying to pop() from todo_stack or add() to visited at the same time, you'll get Race Conditions (data corruption).

Question: How do you protect your shared data structures (visited and todo_stack) so that multiple workers can use them safely?

2. Distributed Scale (The "Memory" Problem)
You mentioned 100 million unique files. A Python set of 100 million strings might take several gigabytes of RAM. If we have multiple servers working together, they can't easily share a Python set() in memory.

Question: Instead of a local Python set, what kind of external data store would you use to keep track of visited IDs across a cluster of servers?

3. Fault Tolerance (The "Crash" Problem)
If your crawler is 90% done (after 9 minutes) and the server crashes, your current code loses the todo_stack and visited set. You have to start from zero.

Question: How would you persist the "work remaining" so that if a node fails, another node can pick up exactly where it left off?

---

## Answers

1. Concurrency: To protect shared data structures like `visited` and `todo_stack`, we can use thread-safe data structures or synchronization mechanisms. For example, we can use a `threading.Lock` to ensure that only one thread can access the `visited` set or `todo_stack` at a time. Alternatively, we could use concurrent data structures like `queue.Queue` for the `todo_stack`, which is thread-safe by design.

2. Distributed Scale: To keep track of visited IDs across a cluster of servers, we can use a distributed data store like Redis. These systems allow multiple servers to read and write to the same data store, ensuring that all servers have access to the same set of visited IDs without the need for complex synchronization.

3. Fault Tolerance: To persist the "work remaining," we can use a durable message queue like RabbitMQ or Kafka. When a worker picks up a folder ID to process, it can mark it as "in progress" in the message queue. If the worker crashes, the message will not be acknowledged, and another worker can pick it up and continue processing from where it left off. Additionally, we can periodically save the state of the `visited` set to a persistent storage like a database or a file system to ensure that we don't lose progress in case of a crash.

---

## Scenario

The Scenario:
Google Drive’s API has a rate limit of 1,000 requests per second. You have 100 workers. Suddenly, you hit a "Folder Loop" where Folder A points to B, and B points to A.

Even though you have Redis, if 50 workers all pull "Folder A" from the queue at the exact same microsecond before any of them have finished writing "Folder A" to Redis, they will all proceed to call the API for Folder A. This is called a Race Condition on the Visited Set.

How would you prevent multiple workers from processing the same ID at the exact same time before it's been marked as "visited"?

## Solution

To prevent multiple workers from processing the same ID at the exact same time before it's been marked as "visited," we can use a distributed locking mechanism provided by Redis. Here's how we can implement this:

1. When a worker picks up a folder ID from the queue, it first tries to acquire a lock for that ID in Redis. This can be done using the `SETNX` command, which sets a key only if it does not already exist.

2. If the worker successfully acquires the lock, it proceeds to process the folder ID. After processing, it releases the lock by deleting the key from Redis.

3. If the worker fails to acquire the lock (because another worker has already acquired it), it can either skip processing that ID or re-queue it for later processing.

4. We can also set an expiration time on the lock to prevent deadlocks in case a worker crashes while holding the lock. This way, if a worker fails to release the lock, it will automatically be released after a certain period of time, allowing other workers to continue processing.