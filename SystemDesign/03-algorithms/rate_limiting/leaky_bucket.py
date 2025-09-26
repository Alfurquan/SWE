import threading
import time
from collections import defaultdict, deque

class LeakyBucket:
    def __init__(self, leak_rate: int, capacity: int):
        self.lock = threading.Lock()
        self.leak_rate = leak_rate
        self.capacity = capacity
        self.buckets = defaultdict(lambda: {'tokens': deque(), 'last_leak': time.time()})
        
    def allow_request(self, key: str) -> bool:
        with self.lock:
            bucket = self.buckets[key]
            now = time.time()
            time_passed = now - bucket['last_leak']
            leaked = int(time_passed * self.leak_rate)
            
            if leaked > 0:
                for _ in range(min(self.capacity, leaked)):
                    bucket['tokens'].popleft()
                    
                bucket['last_leak'] = now
                
            if len(bucket['tokens']) < self.capacity:
                bucket['tokens'].append(now)
                return True
            
            return False
