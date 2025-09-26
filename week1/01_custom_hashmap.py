"""
Week 1 - Problem 1: Custom HashMap Implementation
Difficulty: Medium | Time Limit: 45 minutes | Google L5 Foundation

PROBLEM STATEMENT:
Design and implement a hash map from scratch that handles collisions and dynamic resizing.
Your implementation should be production-ready with proper error handling and optimization.

CORE OPERATIONS:
- put(key, value): Insert or update key-value pair
- get(key): Retrieve value for given key (return None if not found)
- remove(key): Delete key-value pair (return True if removed, False if not found)
- contains(key): Check if key exists in the map
- size(): Return current number of key-value pairs
- isEmpty(): Check if map is empty
- keys(): Return list of all keys
- values(): Return list of all values
- clear(): Remove all elements

ADVANCED OPERATIONS:
- resize(): Manually trigger resize operation
- getLoadFactor(): Return current load factor
- getBucketCount(): Return number of buckets
- getCollisionCount(): Return total collisions for analysis

REQUIREMENTS:
1. **Collision Handling**: Use separate chaining (linked lists) for collision resolution
2. **Dynamic Resizing**: Automatically resize when load factor exceeds 0.75
3. **Hash Function**: Implement a good hash function that distributes keys uniformly
4. **Load Factor**: Maintain load factor between 0.25 and 0.75 for optimal performance
5. **Memory Efficiency**: Minimize memory overhead and handle edge cases
6. **Performance**: Achieve O(1) average case for all basic operations
7. **Type Support**: Handle string keys initially, extend to any hashable type

CONSTRAINTS:
- Initial capacity: 16 buckets
- Maximum load factor: 0.75 (resize up)
- Minimum load factor: 0.25 (resize down, but not below initial capacity)
- Handle null/None keys and values appropriately

ALGORITHM DETAILS:
- Hash Function: Use polynomial rolling hash or similar for strings
- Collision Resolution: Separate chaining with linked lists/arrays
- Resizing Strategy: Double size when load factor > 0.75, halve when < 0.25
- Rehashing: Redistribute all existing elements after resize

REAL-WORLD CONTEXT:
This problem appears in many forms across tech companies:
- Java HashMap internal implementation
- Python dict underlying structure  
- Redis hash table implementation
- Database index structures
- Distributed cache systems like Memcached

PERFORMANCE EXPECTATIONS:
- put(): O(1) average, O(n) worst case
- get(): O(1) average, O(n) worst case
- remove(): O(1) average, O(n) worst case
- resize(): O(n) for rehashing all elements

FOLLOW-UP QUESTIONS:
1. How would you handle hash collisions if chaining wasn't allowed?
2. What hash function would you use for integer keys vs string keys?
3. How would you make this thread-safe for concurrent access?
4. How would you implement this for a distributed system?
5. What metrics would you track to monitor hash map performance?
6. How would you handle very large datasets that don't fit in memory?

EXPECTED INTERFACE:
```python
# Basic usage
hashmap = CustomHashMap()
hashmap.put("user123", {"name": "John", "age": 30})
user = hashmap.get("user123")  # Returns {"name": "John", "age": 30}
exists = hashmap.contains("user123")  # Returns True
hashmap.remove("user123")  # Returns True
size = hashmap.size()  # Returns 0

# Advanced usage
hashmap.put("key1", "value1")
hashmap.put("key2", "value2")
load_factor = hashmap.getLoadFactor()  # Returns current load factor
bucket_count = hashmap.getBucketCount()  # Returns number of buckets
all_keys = hashmap.keys()  # Returns ["key1", "key2"]
all_values = hashmap.values()  # Returns ["value1", "value2"]
```

TEST CASES TO CONSIDER:
1. Empty map operations
2. Single element operations
3. Collision handling (keys that hash to same bucket)
4. Automatic resizing scenarios
5. Large dataset performance
6. Edge cases (None values, empty strings, etc.)
"""

# Your implementation here
class CustomHashMap:
    def __init__(self):
        # Initialize your hash map here
        pass
    
    def put(self, key, value):
        # Implement put operation
        pass
    
    def get(self, key):
        # Implement get operation
        pass
    
    def remove(self, key):
        # Implement remove operation
        pass
    
    # Add other required methods...

if __name__ == "__main__":
    # Add your test cases here
    hashmap = CustomHashMap()
    
    # Basic functionality tests
    print("Testing basic operations...")
    # Add your tests
    
    # Collision handling tests
    print("Testing collision handling...")
    # Add collision tests
    
    # Resizing tests
    print("Testing dynamic resizing...")
    # Add resizing tests
    
    # Performance tests
    print("Testing performance...")
    # Add performance tests
