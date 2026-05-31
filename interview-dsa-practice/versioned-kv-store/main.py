from typing import List, Dict, Tuple

class VersionedKVStore:
    def __init__(self):
        self.items: Dict[str, List[Tuple[int, str]]] = {}

    def set(self, key: str, timestamp: int, value: str):
        if key not in self.items:
            self.items[key] = []

        self.items[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.items:
            return ""
        
        vals = self.items[key]

        return self._search(vals, timestamp)
    
    def _search(self, items: List[Tuple[int, str]], timestamp: int) -> str:
        start = 0
        end = len(items) - 1

        index = -1

        while start <= end:
            mid = start + (end - start) // 2

            if items[mid][0] == timestamp:
                return items[mid][1]
            
            elif items[mid][0] < timestamp:
                start = mid + 1
                index = mid
            else:
                end = mid - 1

        if index == -1:
            return ""
        return items[index][1]
        