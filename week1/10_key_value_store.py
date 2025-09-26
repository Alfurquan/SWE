"""
Week 1 - Problem 10: Simple Key-Value Store
Difficulty: Medium | Time Limit: 35 minutes | Google L5 System Design

PROBLEM STATEMENT:
Design a simple in-memory key-value store with basic persistence

OPERATIONS:
- put(key, value): Store key-value pair
- get(key): Retrieve value for key
- delete(key): Remove key-value pair
- commit(): Persist current state to disk
- rollback(): Revert to last committed state

REQUIREMENTS:
- ACID-like properties for transactions
- Basic persistence mechanism
- Handle large datasets efficiently
- Support for atomic operations

ALGORITHM CONSIDERATIONS:
- Write-ahead logging
- Copy-on-write for rollback
- Efficient serialization

REAL-WORLD CONTEXT:
Database storage engines, distributed caches, configuration stores

FOLLOW-UP QUESTIONS:
- How to implement transactions?
- Crash recovery mechanisms?
- Distributed consensus?
- Compression and optimization?
- Concurrent access patterns?

EXPECTED INTERFACE:
store = KeyValueStore()
store.put("user:1", {"name": "John", "age": 25})
store.put("user:2", {"name": "Jane", "age": 30})
store.commit()
print(store.get("user:1"))  # {"name": "John", "age": 25}
store.put("user:1", {"name": "Johnny", "age": 26})
store.rollback()
print(store.get("user:1"))  # {"name": "John", "age": 25}
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
