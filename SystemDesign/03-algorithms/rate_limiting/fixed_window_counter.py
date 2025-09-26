import threading
import time
from collections import defaultdict, deque

class FixedWindowCounter:
    def __init__(self, window_size: int, max_request: int):
        self.lock = threading.Lock()
        self.window_size = window_size
        self.max_request = max_request
        self.users = defaultdict(lambda: {'window': 0, 'count': 0})
        
    def allow_request(self, user_ip: str) -> bool:
        with self.lock:
            user = self.users[user_ip]
            current_time = time.time()
            current_window = int(current_time // self.window_size)
            
            if user['window'] != current_window:
                user['window'] = current_window
                user['count'] = 0
                
            if user['count'] < self.max_request:
                user['count'] += 1
                return True
            
            return False
            
