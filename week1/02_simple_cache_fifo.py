"""
Week 1 - Problem 2: Simple Cache with FIFO Eviction
Difficulty: Medium | Time Limit: 20 minutes | Google L5 Core Topic

PROBLEM STATEMENT:
Implement a cache with First-In-First-Out eviction policy

OPERATIONS:
- get(key): Return value if exists, otherwise -1
- put(key, value): Insert key-value pair, evict oldest if at capacity
- capacity(): Return maximum capacity
- current_size(): Return current number of items

REQUIREMENTS:
- Fixed capacity, FIFO eviction when full
- O(1) time complexity for get and put
- Handle edge cases (capacity 0, duplicate keys)

REAL-WORLD CONTEXT:
Building block for web browser cache, database buffer pools, CDN caching

FOLLOW-UP QUESTIONS:
- How to modify for LRU instead of FIFO?
- Adding TTL (time-to-live) support?
- Thread safety considerations?
- Cache statistics (hit rate, miss rate)?

EXPECTED INTERFACE:
cache = SimpleCache(capacity=3)
cache.put(1, "one")
cache.put(2, "two")
cache.put(3, "three")
cache.put(4, "four")  # evicts key 1
print(cache.get(1))   # -1 (evicted)
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
