"""
Design and implement a data structure for a Least Frequently Used (LFU) cache.

Implement the LFUCache class:

- LFUCache(int capacity) Initializes the object with the capacity of the data structure.
- int get(int key) Gets the value of the key if the key exists in the cache. Otherwise, returns -1.
- void put(int key, int value) Update the value of the key if present, or inserts the key if not already present. When the cache reaches its capacity, it should invalidate and remove the least frequently used key before inserting a new item. For this problem, when there is a tie (i.e., two or more keys with the same frequency), the least recently used key would be invalidated.

To determine the least frequently used key, a use counter is maintained for each key in the cache. 
The key with the smallest use counter is the least frequently used key.
When a key is first inserted into the cache, its use counter is set to 1 (due to the put operation). 
The use counter for a key in the cache is incremented either a get or put operation is called on it.

The functions get and put must each run in O(1) average time complexity.
"""
from typing import Dict, Deque
import sys
from collections import deque

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.frequencies: Dict[int, Deque[int]] = {}
        self.frequency: Dict[int, int] = {}
        self.map: Dict[int, int] = {}
        self.min_frequency = sys.maxsize
    
    def put(self, key: int, value: int):
        if key in self.map:
            self.map[key] = value
            self.key_accessed(key)
            return
        
        if self.size >= self.capacity:
            self.evict()
            
        self.map[key] = value
        self.frequency[key] = 1
        if 1 not in self.frequencies:
            self.frequencies[1] = deque()
        
        self.frequencies[1].append(key)
        self.min_frequency = 1
        self.size += 1

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        
        val = self.map[key]
        self.key_accessed(key)
        return val
    
    def evict(self):
        key_to_evict = self.frequencies[self.min_frequency].popleft()
        
        if len(self.frequencies[self.min_frequency]) == 0:
            self.min_frequency += 1
        
        self.frequency.pop(key_to_evict)
        self.map.pop(key_to_evict)
        self.size -= 1
    
    def key_accessed(self, key: int):
        freq = self.frequency[key]
        self.frequencies[freq].remove(key)

        if freq == self.min_frequency and len(self.frequencies[freq]) == 0:
            self.min_frequency += 1

        new_freq = freq + 1
        if new_freq not in self.frequencies:
            self.frequencies[new_freq] = deque()
        
        self.frequencies[new_freq].append(key)
        self.frequency[key] = new_freq
        
        
cache = LFUCache(5)
cache.put(1, 100)
cache.put(2, 200)
cache.put(3, 300)
print(cache.get(1))
print(cache.get(4))
cache.put(4, 400)
cache.put(5, 500)
print(cache.get(4))
print(cache.get(5))
print(cache.get(1))
cache.put(6, 600)
print(cache.get(6))
print(cache.get(1))
print(cache.get(2))

## LFU → need 3 maps: key→val, key→freq, freq→list (LRU within). Maintain minFreq.”