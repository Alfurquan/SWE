"""
Week 1 - Problem 8: Simple Rate Limiter
Difficulty: Medium | Time Limit: 25 minutes | Google L5 System Design

PROBLEM STATEMENT:
Implement a rate limiter using fixed window approach

OPERATIONS:
- isAllowed(user_id, timestamp): Return True if request allowed
- getRemainingRequests(user_id): Return remaining requests in current window
- reset(user_id): Reset rate limit for user

REQUIREMENTS:
- Fixed window rate limiting (N requests per time window)
- Configurable limits per user
- Handle time window boundaries correctly
- Efficient cleanup of old data

ALGORITHM:
Fixed window with sliding window optimization

REAL-WORLD CONTEXT:
API rate limiting, DDoS protection, resource management

FOLLOW-UP QUESTIONS:
- Sliding window implementation?
- Token bucket algorithm?
- Distributed rate limiting?
- Different limits for different endpoints?
- Memory cleanup strategies?

EXPECTED INTERFACE:
limiter = RateLimiter(max_requests=5, window_seconds=60)
print(limiter.isAllowed("user1", 1000))  # True (1st request)
# ... 4 more requests ...
print(limiter.isAllowed("user1", 1030))  # False (exceeded)
print(limiter.isAllowed("user1", 1070))  # True (new window)
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
