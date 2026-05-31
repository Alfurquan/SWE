from typing import Dict, Deque
from dataclasses import dataclass
from collections import deque
import time

@dataclass
class Request:
    user_id: str

class RateLimiter:
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests: Dict[str, Deque[float]] = {}

    def allow_request(self, request: Request) -> bool:
        user_id = request.user_id
        current_time = time.time()

        if user_id not in self.requests:
            self.requests[user_id] = deque()
        
        while self.requests[user_id] and current_time - self.requests[user_id][0] > self.window_size:
            self.requests[user_id].popleft()

        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        self.requests[user_id].append(current_time)
        return True
   