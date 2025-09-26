import threading
import time
from collections import defaultdict, deque

class SlidingWindowLog:
    def __init__(self, window_size: int, max_request: int):
        self.lock = threading.Lock()
        self.window_size = window_size
        self.max_request = max_request
        self.users_request = defaultdict(lambda: {'request_log': deque()})
        
    def allow_request(self, user_ip: str) -> bool:
        with self.lock:
            user = self.users[user_ip]
            current_time = time.time()
            
            while user['request_log'] and current_time - user['request_log'][0] >= self.window_size:
                user['request_log'].popleft()
                
            if len(user['request_log']) < self.max_request:
                user['request_log'].append(current_time)
                return True

            return False
            
