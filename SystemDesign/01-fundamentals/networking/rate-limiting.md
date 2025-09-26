# Rate limiting

Rate limiting helps protects services from being overwhelmed by too many requests from a single user or client.

In a network system, a rate limiter is used to control the rate of traffic sent by a client or a service. In the HTTP world, a rate limiter limits the number of client requests allowed to be sent over a specified period. If the API request count exceeds the threshold defined by the rate limiter, all the excess calls are blocked. Here are a few examples:

- A user can write no more than 2 posts per second.
- You can create a maximum of 10 accounts per day from the same IP address.
- You can claim rewards no more than 5 times per week from the same device.

## Rate limiting algorithms

### Token bucket

The Token Bucket algorithm is one of the most popular and widely used rate limiting approaches due to its simplicity and effectiveness.

How it works ?

- Imagine a bucket that holds tokens.
- The bucket has a maximum capacity of tokens.
- Tokens are added to the bucket at a fixed rate (e.g., 10 tokens per second).
- When a request arrives, it must obtain a token from the bucket to proceed.
- If there are enough tokens, the request is allowed and tokens are removed.
- If there aren't enough tokens, the request is dropped.

#### Pros

- Relatively straightforward to implement and understand.
- Allows bursts of requests up to the bucket's capacity, accommodating short-term spikes.

#### Cons

- The memory usage scales with the number of users if implemented per-user.
- It doesn’t guarantee a perfectly smooth rate of requests.

### Leaky bucket

The Leaky Bucket algorithm is similar to Token Bucket but focuses on smoothing out bursty traffic.

How it works ?

- Imagine a bucket with a small hole in the bottom.
- Requests enter the bucket from the top.
- The bucket processes ("leaks") requests at a constant rate through the hole.
- If the bucket is full, new requests are discarded.

#### Pros

- Processes requests at a steady rate, preventing sudden bursts from overwhelming the system.
- Provides a consistent and predictable rate of processing requests.

#### Cons

- Does not handle sudden bursts of requests well; excess requests are immediately dropped.
- Slightly more complex to implement compared to Token Bucket.

### Fixed window counter

The Fixed Window Counter algorithm divides time into fixed windows and counts requests in each window.

How it works ?

- Time is divided into fixed windows (e.g., 1-minute intervals).
- Each window has a counter that starts at zero.
- New requests increment the counter for the current window.
- If the counter exceeds the limit, requests are denied until the next window.

### Sliding Window Log

The Sliding Window Log algorithm keeps a log of timestamps for each request and uses this to determine if a new request should be allowed.

How it works ?

- Keep a log of request timestamps.
- When a new request comes in, remove all entries older than the window size.
- Count the remaining entries.
- If the count is less than the limit, allow the request and add its timestamp to the log.
- If the count exceeds the limit, request is denied.

### Sliding Window Counter

This algorithm combines the Fixed Window Counter and Sliding Window Log approaches for a more accurate and efficient solution.

Instead of keeping track of every single request’s timestamp as the sliding log does, it focus on the number of requests from the last window.

How it works ?

- Keep track of request count for the current and previous window.
- Calculate the weighted sum of requests based on the overlap with the sliding window.
- If the weighted sum is less than the limit, allow the request.