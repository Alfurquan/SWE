# Rate Limiter for Distributed Tasks

We are designing a centralized API Gateway that manages incoming requests for heavy machine-learning tasks. Because these tasks consume a massive amount of GPU compute, we need to implement a strict, rolling window rate-limiter for every unique user.

The Constraints:

- Each user is identified by a unique user_id (string).

- A user is allowed to make a maximum of max_requests within a sliding timeline window of W seconds.

- Every request comes in with an integer timestamp (in seconds). Timestamps are strictly increasing across the system.

Task: Design and implement a SlidingWindowRateLimiter class that supports a single operation:

- is_allowed(user_id: str, timestamp: int) -> bool: Returns True if the request is allowed to proceed, and False if it should be dropped (rate-limited). If the request is allowed, it must be recorded as part of the user's history.

## Example Walkthrough:

Imagine max_requests = 3 and the window size W = 10 seconds.

```python

limiter = SlidingWindowRateLimiter(max_requests=3, w=10)

# User "Alice" makes a request at timestamp 1. 
# She has 1 request in the window. Allowed.
limiter.is_allowed("Alice", 1)  # Returns True

# Alice requests at timestamp 2. (Total: 2 requests in). Allowed.
limiter.is_allowed("Alice", 2)  # Returns True

# Alice requests at timestamp 5. (Total: 3 requests in). Allowed.
limiter.is_allowed("Alice", 5)  # Returns True

# Alice requests at timestamp 8. 
# In the rolling window of (from 8 - 10 + 1 up to 8), she already has 3 requests (at 1, 2, 5).
# Adding this would make 4. Denied.
limiter.is_allowed("Alice", 8)  # Returns False

# Alice requests at timestamp 12.
# The rolling window is now (since 12 - 10 = 2, so everything > 2 is inside).
# Her old requests at 1 and 2 fall outside the window! Only the request at 5 remains.
# Total active requests = 1. She has room. Allowed.
limiter.is_allowed("Alice", 12) # Returns True

```

---

## Approach

### Data Structure:

- We can use a dictionary to map each user_id to a list of timestamps representing their request history. This allows us to efficiently track and manage requests for each user. The list here would be a deque (double-ended queue) to allow for efficient addition and removal of timestamps.

### Logic

- When a new request comes in, we will:
    1. Check the user's request history in the dictionary.
    2. Remove any timestamps that are outside the current rolling window (i.e., timestamps that are less than `timestamp - W`).
    3. Check if the number of remaining timestamps is less than `max_requests`. If it is, allow the request and add the current timestamp to the user's history. If not, deny the request.