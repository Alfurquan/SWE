# The Problem: "The Distributed Rate Limiter"
Imagine you are an engineer at a company like Stripe or GitHub. You provide an API to customers, but you need to make sure no single customer "hogs" the system by sending too many requests.

The Task:
Implement a RateLimiter that tracks how many requests a user has made and blocks them if they exceed a certain limit within a specific time window.

The API:

1. __init__(max_requests: int, window_size_sec: int):

- max_requests: How many requests a user is allowed (e.g., 5).

- window_size_sec: The timeframe (e.g., 60 seconds).

2. allow_request(user_id: str) -> bool:

- Returns True if the user is under the limit and the request is allowed.

- Returns False if they are over the limit.

Crucial: The window is "sliding." If the limit is 5 per minute, at any given second, the user must not have made more than 5 requests in the previous 60 seconds.

## Approach:

### Data Structure:

To implement the RateLimiter, we can use a dictionary to track each user's request timestamps. The key will be the user_id, and the value will be a list of timestamps representing when the user made requests.

- Deque (double-ended queue) can be used for efficient addition and removal of timestamps.
- Dict[str, Deque[int]]: A dictionary where the key is the user_id and the value is a deque of timestamps.

### Algorithm:

1. When a request comes in, check if the user_id exists in the dictionary.
2. If it does not exist, create a new entry with an empty deque and add the current timestamp.
3. If it does exist, remove timestamps from the deque that are older than the current timestamp minus the window size (i.e., outside the sliding window).
4. Check the length of the deque:
   - If the length is less than max_requests, allow the request, add the current timestamp to the deque, and return True.
   - If the length is equal to or greater than max_requests, block the request and return False.

## Phase 2: System Design (Scaling to Millions)

Imagine you are now at Netflix. You have 500 microservices, and they all need to check the rate limit for a user. You cannot keep the deque in the memory of a single Python process anymore because a user's first request might hit "Server A" and their second request might hit "Server B."

1. The "Distributed State" Problem

Question: How do you share the request history across multiple servers? If you use a database like Redis, how would you implement this "Sliding Window" logic using Redis data structures? 

2. The "Race Condition" Problem (L5 Core)

Question: In a distributed environment, the "Check-then-Act" problem becomes much worse. If two servers check Redis at the same time, they both might allow the request. How can you make the "Cleanup, Count, and Add" steps atomic in Redis?

3. The "Memory/Performance" Trade-off

Question: The Sliding Window Log (storing every timestamp) is very accurate but takes a lot of memory ($O(N)$ per user). If we can tolerate 1-2% inaccuracy, is there a more memory-efficient algorithm (like Token Bucket or Sliding Window Counter) that uses a fixed amount of memory ($O(1)$) regardless of the number of requests?

## Answer

### 1. Distributed State Problem

To share the request history across multiple servers, we can use a centralized data store like Redis. Redis is an in-memory data structure store that supports various data structures, including lists, sets, and sorted sets, which can be used to implement the sliding window logic.

We can use a Redis sorted set to store the timestamps of requests for each user. The key can be the user_id, and the value can be a sorted set where the score is the timestamp of the request. This allows us to efficiently add new timestamps and remove old ones.

Steps to implement the sliding window logic using Redis:

1. When a request comes in, check if the user_id exists in Redis.
2. If it does not exist, create a new sorted set for the user_id and add the current timestamp with the score as the timestamp.
3. If it does exist, remove timestamps from the sorted set that are older than the current timestamp minus the window size (i.e., outside the sliding window) using the ZREMRANGEBYSCORE command.
4. Check the cardinality of the sorted set using the ZCARD command:
   - If the cardinality is less than max_requests, allow the request, add the current timestamp to the sorted set, and return True.
   - If the cardinality is equal to or greater than max_requests, block the request and return False

### 2. Race Condition

To handle the race condition problem in a distributed environment, we can use Redis transactions or Lua scripts to make the "Cleanup, Count, and Add" steps atomic.

### 3. Memory/Performance Trade-off

If we can tolerate 1-2% inaccuracy, we can use a more memory-efficient algorithm like the Token Bucket or Sliding Window Counter.

The Token Bucket algorithm allows a user to make requests at a certain rate, and if they exceed that rate, they must wait until tokens are replenished. This approach uses a fixed amount of memory regardless of the number of requests.

The Sliding Window Counter algorithm divides the time window into smaller intervals (e.g., 1 second) and maintains a count of requests in each interval. This allows us to approximate the number of requests in the sliding window without storing every timestamp, thus reducing memory usage.

So here the trade-off is between accuracy and memory usage. If we can tolerate some inaccuracy, we can use these algorithms to reduce memory usage while still enforcing rate limits effectively.