from typing import List

class MyHeap:
    def __init__(self):
        self.heapsize = 0
        self.items: List[int] = []

    def push(self, item: int) -> None:
        self.items.append(item)
        self._bubble_up()
        self.heapsize += 1
        
    def pop(self) -> int:
        if self.heapsize == 0:
            return -1
        
        root = self.items[0]
        self.items[0] = self.items[self.heapsize - 1]
        self._bubble_down_from(0)
        self.heapsize -= 1
        return root

    def peek(self) -> int:
        if self.heapsize == 0:
            return -1
        
        return self.items[0]
    
    def heapify(self, nums: List[int]) -> List[int]:
        self.items = nums[:]
        self.heapsize = len(nums)
        for index in range(self.heapsize // 2, -1, -1):
            self._bubble_down_from(index)

        return self.items
    
    def _bubble_up(self) -> None:
        index = self.heapsize
        while index > 0 and self.items[index] <= self.items[self._parent_index(index)]:
            self._swap(index, self._parent_index(index))
            index = self._parent_index(index)
            
    def _bubble_down_from(self, index: int) -> None:
        while index < self.heapsize and not self._is_valid_parent(index):
            smallest_child_index = self._get_smallest_child_index(index)
            self._swap(index, smallest_child_index)
            index = smallest_child_index

    def _swap(self, first_index: int, second_index: int) -> None:
        tmp = self.items[first_index]
        self.items[first_index] = self.items[second_index]
        self.items[second_index] = tmp
    
    def _left_child_index(self, index : int) -> int:
        return 2 * index + 1
    
    def _right_child_index(self, index: int) -> int:
        return 2 * index + 2
    
    def _parent_index(self, index: int) -> int:
        return (index - 1) // 2
    
    def _has_left_child(self, index: int) -> bool:
        return self._left_child_index(index) < self.heapsize
    
    def _has_right_child(self, index: int) -> bool:
        return self._right_child_index(index) < self.heapsize
    
    def _left_child(self, index: int) -> int:
        return self.items[self._left_child_index(index)]
    
    def _right_child(self, index: int) -> int:
        return self.items[self._right_child_index(index)]
    
    def _is_valid_parent(self, index: int) -> bool:
        if not self._has_left_child(index):
            return True
        
        if not self._has_right_child(index):
            return self.items[index] < self._left_child(index)
        
        return self.items[index] < self._left_child(index) and self.items[index] < self._right_child(index)
    
    def _get_smallest_child_index(self, index: int) -> int:
        if not self._has_right_child(index):
            return self._left_child_index(index)
        
        return self._left_child_index(index) if self._left_child(index) < self._right_child(index) else self._right_child_index(index)
    
if __name__ == '__main__':
    heap = MyHeap()
    heap.push(100)
    heap.push(200)
    heap.push(20)
    heap.push(30)
    heap.push(10)
    heap.push(5)
    print(heap.peek())
    heap.pop()
    print(heap.peek())
    heap.pop()
    print(heap.peek())
    heap.pop()
    print(heap.peek())
    heap.pop()
    print(heap.peek())
    heap.pop()
    print(heap.peek())
    print(heap.heapify([4, 6, 9, 3, 2, 8, 3]))