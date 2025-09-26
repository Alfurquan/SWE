from typing import List

class MaxHeap:
    def __init__(self, size: int):
        self.size = size
        self.items = [None] * size
        self.heapsize = 0
        
    def insert(self, item: int):
        if self.heapsize >= self.size:
            print(f"Cannot insert {item} as heap is full")
            return
        
        index = self.heapsize
        self.items[index] = item
        self.bubble_up()
        self.heapsize = self.heapsize + 1
        
    def get_max(self) -> int:
        return self.items[0]
    
    def extract_max(self) -> int:
        if self.heapsize == 0:
            print("Heap is empty")
            return
        
        item = self.items[0]
        self.items[0] = self.items[self.heapsize - 1]
        self.bubble_down()
        self.heapsize -= 1
        return item
    
    def bubble_down(self):
        index = 0
        while index < self.heapsize and not self.is_valid_parent(index):
            larger_index = self.larger_child_index(index)
            self.swap(larger_index, index)
            index = larger_index
    
    def bubble_up(self):
        index = self.heapsize
        
        while index > 0 and self.items[index] >= self.parent(index):
            self.swap(index, self.parent_index(index))
            index = self.parent_index(index)
        
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
    
    def parent(self, index: int) -> int:
        return self.items[self.parent_index(index)]
    
    def larger_child_index(self, index: int) -> int:
        if not self.has_right_child(index):
            return self.left_child_index(index)
        
        return self.left_child_index(index) if self.left_child(index) > self.right_child(index) else self.right_child_index(index)
    
    def is_valid_parent(self, index: int) -> bool:
        if not self.has_left_child(index):
            return True
        
        if not self.has_right_child(index):
            return self.items[index] >= self.left_child(index)
        
        return self.items[index] >= self.left_child(index) and self.items[index] >= self.right_child(index)
    
    def swap(self, index1: int, index2):
        temp = self.items[index1]
        self.items[index1] = self.items[index2]
        self.items[index2] = temp
        

def heapify(numbers: List[int]) -> List[int]:
    n = len(numbers)
    for index in range(n // 2 - 1, -1, -1):
        heapify_util(numbers, index)
    return numbers

def heapify_util(numbers: List[int], index: int):
    left_index = 2 * index + 1
    
    larger_index = index
    if left_index < len(numbers) and numbers[left_index] > numbers[larger_index]:
        larger_index = left_index
        
    right_index = 2 * index + 2
    
    if right_index < len(numbers) and numbers[right_index] > numbers[larger_index]:
        larger_index = right_index
    
    if index != larger_index:
        temp = numbers[index]
        numbers[index] = numbers[larger_index]
        numbers[larger_index] = temp
        heapify_util(numbers, larger_index)

def heap_sort(numbers: List[int]) -> List[int]:
    result = []
    heap = MaxHeap(len(numbers))
    for number in numbers:
        heap.insert(number)
        
    for _ in range(len(numbers)):
        result.append(heap.extract_max())
    return list(reversed(result))
    
      
heap = MaxHeap(5)
heap.insert(3)
heap.insert(10)
heap.insert(20)
heap.insert(100)
heap.insert(30)
heap.insert(200)
print(heap.get_max())
print(heap.extract_max())
print(heap.get_max())
heap.insert(200)
print(heap.get_max())
print("---")
print(heap.extract_max())
print(heap.extract_max())
print(heap.extract_max())
print(heap.extract_max())
print(heap.extract_max())
print(heap.extract_max())
print("------------------Heapify-------------------------")
print(heap_sort([3, 4, 1, 100, 2]))

    