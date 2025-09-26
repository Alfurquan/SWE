import threading
import time
from collections import defaultdict

class TokenBucket:
    def __init__(self, refill_rate: int, capacity: int):
        self.lock = threading.Lock()
        self.refill_rate = refill_rate
        self.capacity = capacity
        self.tokens = defaultdict(lambda: {'tokens': capacity, 'last_checked': time.time()})
        
    def allow_request(self, key: str) -> bool:
        with self.lock:
            now = time.time()
            bucket = self.buckets[key]
            time_passed = now - bucket['last_checked']
            refill = time_passed * self.refill_rate
            bucket['tokens'] = min(self.capacity, bucket['tokens'] + refill)
            bucket['last_checked'] = now
            
            if bucket['tokens'] >= 1:
                bucket['tokens'] -= 1
                return True
            
            return False
            
                