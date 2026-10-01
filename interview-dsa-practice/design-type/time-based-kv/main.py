from typing import Dict, List, Tuple

class TimeBasedKV:
    def __init__(self):
        self.items: Dict[str, List[Tuple[int, str]]] = {}

    def set_value(self, key: str, value: str, timestamp: int):
        if key not in self.items:
            self.items[key] = []

        self.items[key].append((timestamp, value))

    def get_value(self, key: str, timestamp: int) -> str:
        if key not in self.items:
            return ""

        item_list = self.items[key]

        low = 0
        high = len(item_list) - 1
        result = ""
        
        while low <= high:
            mid = low + (high - low) // 2

            if item_list[mid][0] <= timestamp:
                result = item_list[mid][1]
                low = mid + 1
            else:
                high = mid - 1

        return result