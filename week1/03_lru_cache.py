"""
Week 1 - Problem 3: LRU Cache Implementation
Difficulty: Medium-Hard | Time Limit: 35 minutes | Google L5 Classic

PROBLEM STATEMENT:
Implement Least Recently Used (LRU) cache with O(1) get and put operations

OPERATIONS:
- get(key): Return value and mark as recently used, -1 if not found
- put(key, value): Insert/update, evict LRU if at capacity

REQUIREMENTS:
- Both operations O(1) time complexity
- get() updates the access order
- Fixed capacity with LRU eviction

ALGORITHM HINT:
HashMap + Doubly Linked List combination

REAL-WORLD CONTEXT:
OS page replacement, CPU cache management, database buffer pools

FOLLOW-UP QUESTIONS:
- Why doubly linked list vs singly linked?
- Thread safety implementation?
- Distributed LRU across multiple machines?
- LRU vs LFU vs other eviction policies?

EXPECTED INTERFACE:
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
cache.get(1)      # returns 1, makes 1 recently used
cache.put(3, 3)   # evicts key 2 (LRU)
cache.get(2)      # returns -1
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
