from typing import Dict, Deque
from collections import deque, defaultdict
from dataclasses import dataclass
import time
from threading import Lock

@dataclass
class Request:
    user_id: str
    timestamp: float

@dataclass
class TokenBucket:
    tokens: float
    last_checked: float

@dataclass
class LeakyBucket:
    water: float
    last_leaked: float

@dataclass
class UserWindow:
    window: int
    count: int

@dataclass
class UserSlidingWindow:
    window_start: int
    previous_count: int
    current_count: int

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.users_requests: Dict[str, Deque[float]] = defaultdict(deque)
        self.lock = Lock()

    def is_allowed(self, request: Request) -> bool:
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            user_request_queue = self.users_requests[user_id]

            while user_request_queue and timestamp - user_request_queue[0] >= self.window_size:
                user_request_queue.popleft()

            if len(user_request_queue) < self.max_requests:
                user_request_queue.append(timestamp)
                return True

            return False

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.user_buckets: Dict[str, TokenBucket] = {}
        self.lock = Lock()

    def is_allowed(self, request: Request) -> bool:
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            if user_id not in self.user_buckets:
                self.user_buckets[user_id] = TokenBucket(tokens = self.capacity, last_checked=timestamp)

            user_bucket = self.user_buckets[user_id]

            elapsed = timestamp - user_bucket.last_checked
            refilled = elapsed * self.refill_rate

            user_bucket.tokens = min(self.capacity, user_bucket.tokens + refilled)
            user_bucket.last_checked = timestamp

            if user_bucket.tokens >= 1:
                user_bucket.tokens -= 1
                return True

            return False

class LeakyBucketRateLimiter:
    def __init__(self, capacity: int, leak_rate: float):
            self.capacity = capacity
            self.leak_rate = leak_rate
            self.user_buckets: Dict[str, LeakyBucket] = {}
            self.lock = Lock()
    
    def is_allowed(self, request: Request) -> bool:
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            if user_id not in self.user_buckets:
                self.user_buckets[user_id] = LeakyBucket(water=0.0, last_leaked=timestamp)

            user_bucket = self.user_buckets[user_id]

            elapsed = timestamp - user_bucket.last_leaked
            leaked = elapsed * self.leak_rate

            user_bucket.water = max(0.0, user_bucket.water - leaked)
            user_bucket.last_leaked = timestamp

            if user_bucket.water + 1 <= self.capacity:
                user_bucket.water += 1
                return True

            return False


class FixedWindowCounterRateLimiter:
    def __init__(self, window_size: int, max_requests: int):
            self.window_size = window_size
            self.max_requests = max_requests
            self.user_windows: Dict[str, UserWindow] = {}
            self.lock = Lock()
    
    def is_allowed(self, request: Request) -> bool:
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            if user_id not in self.user_windows:
                self.user_windows[user_id] = UserWindow(window=0, count = 0)

            user_window = self.user_windows[user_id]

            curr_window = timestamp // self.window_size

            if user_window.window != curr_window:
                user_window.window = curr_window
                user_window.count = 0

            if user_window.count < self.max_requests:
                user_window.count += 1
                return True

            return False

class SlidingWindowCounterRateLimiter:
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.user_windows: Dict[str, UserSlidingWindow] = {}
        self.lock = Lock()

    def is_allowed(self, request: Request):
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            if user_id not in self.user_windows:
                self.user_windows[user_id] = UserSlidingWindow(
                    window_start= (timestamp // self.window_size) * self.window_size,
                    current_count=0,
                    previous_count=0
                )

            user_window = self.user_windows[user_id]

            current_window_start = (timestamp // self.window_size) * self.window_size

            if current_window_start != user_window.window_start:
                if user_window.window_start + self.window_size == current_window_start:
                    user_window.previous_count = user_window.current_count
                else:
                    user_window.previous_count = 0

                user_window.window_start = current_window_start
                user_window.current_count = 0

            elapsed = timestamp - user_window.window_start
            weight = (self.window_size - elapsed) / self.window_size

            estimated_count = user_window.previous_count * weight + user_window.current_count

            if estimated_count + 1 <= self.max_requests:
                user_window.current_count += 1
                return True

            return False

        
