from typing import Dict, Deque
from collections import deque
from dataclasses import dataclass

@dataclass
class Request:
    user_id: str
    timestamp: int


class SlidingWindowRateLimiter:
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.users_requests: Dict[str, Deque[int]] = {}

    def is_allowed(self, request: Request) -> bool:
        user_id = request.user_id
        timestamp = request.timestamp

        if user_id not in self.users_requests:
            self.users_requests[user_id] = deque()

        user_request = self.users_requests[user_id]

        while user_request and timestamp - user_request[0] >= self.window_size:
            user_request.popleft()

        if len(user_request) >= self.max_requests:
            return False
        
        user_request.append(timestamp)
        return True

