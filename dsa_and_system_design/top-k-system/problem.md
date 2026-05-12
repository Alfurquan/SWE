# Problem Statement: Real-Time Trending Topics

Implement a system that tracks the most popular "topics" (hashtags or terms) within a sliding window of time.

## The API:

1. `__init__(k: int, window_size: int):`

    - k: The number of trending topics to return (e.g., Top 10).
    - window_size: The duration of the sliding window in seconds (e.g., 3600 for 1 hour).

2. `process_topic(topic: str, timestamp: int):`

    - Records an occurrence of a topic at a specific time.

3. `get_trending() -> List[str]:`

    - Returns the k most frequent topics within the last window_size seconds, relative to the maximum timestamp seen so far.


## Phase 1: The Coding Challenge (Single Machine)

For this first part, assume all data fits on one machine.

Your Goal:

- Implement the logic to handle the sliding window (removing topics that have "aged out").

- Efficiently retrieve the Top K.

---

## Approach

Here is how I am thinking to solve this problem

### Key Data Structures:

- A `deque` to store the timestamps of each topic. Here the deque will store pairs of (timestamp, topic) and will help us efficiently remove old topics that fall outside the sliding window.
- A `Counter` (or a dictionary) to count the occurrences of each topic within the current window.
- A `SortedSet` which stores topics based on their counts for efficient retrieval of the top K topics.
- A variable to keep track of the maximum timestamp seen so far. (This is the watermark for the sliding window.)

### Algorithm:

- We initialize the data structures in the constructor. Also initialize the watermark to 0.
- In `process_topic`
    - We update watermark = max(watermark, timestamp)
    - We do global cleanup of old topics that are outside the sliding window by checking the timestamps in the deque and removing any topics that have timestamps less than (watermark - window_size). We remove the old timestamps from the deque and update the Counter and SortedSet accordingly.
    - After cleanup, we add the new topic with its timestamp to the deque.
    - We increment the count of the topic in the Counter.
    - We add the topic to the SortedSet based on its new count.
- In `get_trending`
    - We simply return the top K topics from the SortedSet.

### Time Complexity:
- `process_topic`: O(log N) for updating the SortedSet, where N is the number of unique topics in the current window., O(1) for updating the Counter and deque.
- `get_trending`: O(K) to retrieve the top K topics.

---

## Phase 2: System Design Follow-up (The "Senior" Pressure)

Now, let's break this code with Scale.

The Scenario:
Your counts dictionary is fine, but the self.topics deque is the problem. If you are processing 100,000 tweets per second, a 24-hour window means the deque holds 8.6 billion integers. This will exceed the RAM of any single standard machine.

1. Aggregation (Bucketing):
Instead of storing every single timestamp in a deque, how could you use "Buckets" (e.g., 1-minute or 5-minute intervals) to reduce the memory of the self.topics tracking by 1000x or more?

2. Distributed Counts:
If the traffic is too much for one machine, you decide to shard the data by hash(topic).

Server A handles all #coffee tweets.

Server B handles all #tech tweets.

The Problem: How does get_trending() work now? If every server only knows its own top topics, how do you find the Global Top 10?

3. The "Heavy Hitter" Optimization:
Most hashtags are only seen once. Only a few (like #news) are seen millions of times.

Question: Could you use a Count-Min Sketch or a Space-Saving Algorithm to provide an approximate Top-K while using significantly less memory? How would you explain the trade-off between "exact counts" and "approximate counts" to a Product Manager?

How would you approach these three scaling challenges? 

---

## Solution

### 1. Aggregation (Bucketing):

Instead of storing every single timestamp, we can aggregate counts into fixed time buckets. For example, if we use 1-minute buckets, we can maintain a dictionary where the key is the bucket timestamp (e.g., the start of the minute) and the value is another dictionary that counts the occurrences of each topic within that bucket.

This way, instead of storing 8.6 billion timestamps for a 24-hour window, we would only store 1440 buckets (for 1-minute intervals) and the counts of topics within those buckets. This significantly reduces memory usage while still allowing us to track trends over time.

This way we can easily remove old buckets that fall outside the sliding window and maintain an efficient count of topics within the current window.

### 2. Distributed Counts

In this scenario, we can use a distributed approach to aggregate the counts from different servers. Each server can maintain its own local top K topics based on the topics it handles.

To get the global top K, we can use a distributed aggregation method. For example, we can have a central coordinator that periodically collects the top K from each server and merges them to find the global top K. This can be done using a min-heap or a priority queue to efficiently merge the results.

### 3. The "Heavy Hitter" Optimization:

Using a Count-Min Sketch Algorithm hels us to maintain the frequency of topics in a space efficient manner. It allows us to estimate the count of each topic with a certain error margin. The trade-off is that while we can significantly reduce memory usage, we may not get exact counts for all topics, especially those that are less frequent. However, for the most popular topics (the "heavy hitters"), the estimates will be more accurate.

This approach will always over estimate the counts, but it will never underestimate them. This means that while we may include some topics in the top K that are not actually in the top K, we will never miss any of the true top K topics. This can be a reasonable trade-off for many applications where memory constraints are a concern and exact counts are not critical.

So this way we can explain to the Product Manager that while we may not have exact counts for every topic, we can still reliably identify the most popular topics with a much smaller memory footprint, which is crucial for handling large-scale data.

