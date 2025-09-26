"""Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:

- LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
- int get(int key) Return the value of the key if the key exists, otherwise return -1.
- void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.
The functions get and put must each run in O(1) average time complexity.
"""
from typing import Dict

class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.next: 'Node' = None
        self.prev: 'Node' = None

class LRUCache:
    
    def __init__(self, capacity: int):
        self.size = 0
        self.capacity = capacity
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.map: Dict[int, Node] = {}
        
    def put(self, key: int, value: int):
        if key in self.map:
            node = self.map[key]
            node.value = value
            self.delete_node(node)
            self.add_node_to_head(node)
            return
        
        node = Node(key, value)
        self.map[key] = node
        
        if self.size == self.capacity:
            self.evict()
        
        self.add_node_to_head(node)
        self.size += 1
    
    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        
        node = self.map[key]
        self.delete_node(node)
        self.add_node_to_head(node)
        return node.value
    
    def add_node_to_head(self, node: Node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        
    def evict(self):
        self.map.pop(self.tail.prev.key)
        self.delete_node(self.tail.prev)
        self.size -= 1
    
    def delete_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev
        
cache = LRUCache(5)
cache.put(1, 100)
cache.put(2, 200)
cache.put(3, 300)
cache.put(4, 400)
cache.put(5, 500)
cache.put(1, 600)
cache.put(6, 700)
print(cache.get(1))
print(cache.get(6))
print(cache.get(2))
print(cache.get(3))