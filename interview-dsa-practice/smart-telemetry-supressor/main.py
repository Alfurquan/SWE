from typing import Dict, Deque, Tuple
from collections import deque

class TelemetrySuppressor:
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.last_seen: Dict[str, int] = {}

    def should_emit(self, error_code: str, timestamp: int) -> bool:
        if not error_code in self.last_seen or timestamp - self.last_seen[error_code] > self.window_size:
            self.last_seen[error_code] = timestamp
            return True
        
        return False
    
class MemoryEfficientTelemetrySuppressor:
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.last_seen: Dict[str, int] = {}
        self.queue: Deque[Tuple[int, str]] = deque()

    def should_emit(self, error_code: str, timestamp: int) -> bool:
        while self.queue and timestamp - self.queue[0][0] > self.window_size:
            expired_timestamp, expired_error_code = self.queue.popleft()

            if expired_timestamp == self.last_seen[expired_error_code]:
                self.last_seen.pop(expired_error_code)
        
        if error_code not in self.last_seen or (timestamp - self.last_seen[error_code]) > self.window_size:
            self.last_seen[error_code] = timestamp
            self.queue.append((timestamp, error_code))
            return True

        return False
 
suppressor = MemoryEfficientTelemetrySuppressor(10)
print(suppressor.should_emit("ERR_A", 1))
print(suppressor.should_emit("ERR_A", 5))
print(suppressor.should_emit("ERR_B", 11))
print(suppressor.should_emit("ERR_A", 12))
print(suppressor.should_emit("ERR_A", 15))