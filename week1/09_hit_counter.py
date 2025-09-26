"""
Week 1 - Problem 9: Hit Counter
Difficulty: Medium | Time Limit: 20 minutes | Google L5 Time-Series

PROBLEM STATEMENT:
Design a hit counter that counts hits in the last N seconds

OPERATIONS:
- hit(timestamp): Record a hit at given timestamp
- getHits(timestamp): Return number of hits in last 300 seconds

REQUIREMENTS:
- Sliding window of last N seconds
- Efficient for high frequency hits
- Handle out-of-order timestamps
- Memory efficient for large time windows

ALGORITHM APPROACHES:
1. Circular buffer with time buckets
2. Queue with timestamp cleanup
3. Sliding window with aggregation

REAL-WORLD CONTEXT:
Web analytics, API monitoring, system metrics, real-time dashboards

FOLLOW-UP QUESTIONS:
- How to handle very high hit rates?
- Memory vs accuracy trade-offs?
- Distributed hit counting?
- Different time windows simultaneously?

EXPECTED INTERFACE:
counter = HitCounter()
counter.hit(1)
counter.hit(2)
counter.hit(3)
print(counter.getHits(4))    # 3 (hits at 1,2,3)
print(counter.getHits(300))  # 2 (hits at 2,3, hit at 1 is > 300 sec old)
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
