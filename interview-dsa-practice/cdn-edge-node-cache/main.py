from typing import Dict, Deque
from collections import OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.size = 0
        self.items: Dict[str, str] = {}
        self.counts: Dict[str, int] = {}
        self.freq_list: Dict[int, OrderedDict] = {}
    
    def get(self, file_id: str) -> str:
        if file_id not in self.items:
            return ""
        
        self._file_accessed(file_id)
        return self.items[file_id]

    def put(self, file_id: str, content: str) -> None:
        if self.capacity == 0:
            return

        if file_id in self.items:
            self.items[file_id] = content
            self._file_accessed(file_id)
            return
        
        if self.size >= self.capacity:
            self._evict()

        self.items[file_id] = content
        self.counts[file_id] = 1
        self.min_freq = 1
        
        if 1 not in self.freq_list:
            self.freq_list[1] = OrderedDict()
        
        self.freq_list[file_id] = True
        self.size += 1

    def _file_accessed(self, file_id: str):
        old_count = self.counts[file_id]

        new_count = old_count + 1

        if new_count not in self.freq_list:
            self.freq_list[new_count] = OrderedDict()

        self.freq_list[old_count].pop(file_id)

        if len(self.freq_list[old_count]) == 0:
            if old_count == self.min_freq:
                self.min_freq += 1
            self.freq_list.pop(old_count)

        self.counts[file_id] = new_count
        self.freq_list[new_count][file_id] = True

    def _evict(self):
        file_to_evict, _ = self.freq_list[self.min_freq].popitem(last=False)

        self.counts.pop(file_to_evict)
        self.items.pop(file_to_evict)

        if len(self.freq_list[self.min_freq]) == 0:
            self.min_freq += 1

        self.size -= 1


        