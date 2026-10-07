from typing import Dict

class Node:
    def __init__(self, key: str, value: int):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity

        if capacity <= 0:
            raise Exception("Capacity must be greater than zero")

        self.items: Dict[str, Node] = {}
        self.head = Node("", -1)
        self.tail = Node("", -1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def get(self, key: str) -> int:
        if key not in self.items:
            return -1

        node = self.items[key]
        self._delete_node(node)
        self._add_node_to_head(node)
        return node.value

    def put(self, key: str, value: int):
        if key in self.items:
            node = self.items[key]
            node.value = value
            self._delete_node(node)
            self._add_node_to_head(node)
            return

        if self.size >= self.capacity:
            self._evict() 

        node = Node(key, value)
        self.items[key] = node
        self._add_node_to_head(node)
        self.size += 1

    def _delete_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_node_to_head(self, node: Node):
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        node.prev = self.head

    def _evict(self):
        node_to_evict = self.tail.prev
        key_to_evict = node_to_evict.key

        self._delete_node(node_to_evict)
        self.items.pop(key_to_evict)
        self.size -= 1

