from typing import List

class MinHeap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.heapsize = 0
        self.items: List[int] = [None] * self.capacity
        
    def insert(self, item: int):
        if self.heapsize == self.capacity:
            print("Heap is full")
            return
        
        self.items[self.heapsize] = item
        self.bubble_up()
        self.heapsize += 1
    
    def extract_min(self) -> int:
        if self.heapsize == 0:
            print("Heap is empty")
            return
        
        item = self.items[0]
        self.items[0] = self.items[self.heapsize - 1]
        self.bubble_down()
        self.heapsize -= 1
        return item
    
    def get_min(self) -> int:
        if self.heapsize == 0:
            print("Heap is empty")
            return
        return self.items[0]
    
    def bubble_up(self):
        index = self.heapsize
        while index > 0  and self.items[index] <= self.items[self.parent_index(index)]:
            self.swap(index, self.parent_index(index))
            index = self.parent_index(index)
    
    def bubble_down(self):
        index = 0
        while index < self.heapsize and not self.is_valid_parent(index):
            smaller_child_index = self.smaller_child_index(index)
            self.swap(index, smaller_child_index)
            index = smaller_child_index
            
    
    def swap(self, index1: int, index2: int):
        tmp = self.items[index1]
        self.items[index1] = self.items[index2]
        self.items[index2] = tmp
    
    def left_child_index(self, index: int) -> int:
        return 2 * index + 1
    
    def right_child_index(self, index: int) -> int:
        return 2 * index + 2
    
    def left_child(self, index: int) -> int:
        return self.items[self.left_child_index(index)]
    
    def right_child(self, index: int) -> int:
        return self.items[self.right_child_index(index)]
    
    def has_left_child(self, index: int) -> bool:
        return self.left_child_index(index) < self.heapsize
    
    def has_right_child(self, index: int) -> bool:
        return self.right_child_index(index) < self.heapsize
    
    def parent_index(self, index: int) -> int:
        return (index - 1) // 2
    
    def is_valid_parent(self, index: int) -> bool:
        if not self.has_left_child(index):
            return True
        
        if not self.has_right_child(index):
            return self.items[index] < self.left_child(index)
        
        return self.items[index] < self.left_child(index) and self.items[index] < self.right_child(index)
    
    
    def smaller_child_index(self, index: int) -> int:
        if not self.has_right_child(index):
            return self.left_child_index(index)
        
        return self.left_child_index(index) if self.left_child(index) < self.right_child(index) else self.right_child_index(index)
    
    
heap = MinHeap(5)
heap.insert(100)
heap.insert(200)
heap.insert(20)
heap.insert(30)
heap.insert(10)
heap.insert(5)
print(heap.get_min())
heap.extract_min()
print(heap.get_min())
heap.extract_min()
print(heap.get_min())
heap.extract_min()
print(heap.get_min())
heap.extract_min()
print(heap.get_min())
heap.extract_min()
print(heap.get_min())