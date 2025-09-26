import threading
import time
from collections import defaultdict, deque

class SlidingWindowCounter:
    def __init__(self, window_size: int, max_request: int):
        self.lock = threading.Lock()
        self.window_size = window_size
        self.max_request = max_request
        self.user_requests = defaultdict(lambda: {'current_window': time.time(), 'current_count': 0, 'previous_count': 0})
        
    def allow_request(self, user_ip: str) -> bool:
        with self.lock:
            now = time.time()
            window = now // self.window_size
            user_request = self.user_requests[user_ip]

            if window != user_request['current_window']:
                user_request['previous_count'] = user_request['current_count']
                user_request['current_count'] = 0
                user_request['current_window'] = window
            
            window_elapsed = (now % self.window_size) / self.window_size
            threshold = user_request['previous_count'] * (1 - window_elapsed) + user_request['current_count']

            if threshold < self.max_request:
                user_request['current_count'] += 1
                return True

            return False
            
