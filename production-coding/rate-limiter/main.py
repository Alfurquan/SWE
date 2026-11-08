from typing import Dict, Deque
from threading import Lock
from dataclasses import dataclass
from collections import deque

@dataclass
class TokenBucket:
    tokens: float
    last_refilled: float

@dataclass
class Request:
    user_id: str
    timestamp: float

@dataclass
class Response:
    allowed: bool
    retry_after: float

@dataclass
class LeakyBucket:
    requests: Deque[float]
    last_leaked: float

@dataclass
class UserFixedWindow:
    window: int
    count: int

@dataclass
class UserSlidingWindow:
    start: int
    current_count: int
    previous_count: int

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: int):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.lock = Lock()
        self.user_buckets: Dict[str, TokenBucket] = {}

    def is_allowed(self, request: Request) -> Response:
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            if user_id not in self.user_buckets:
                self.user_buckets[user_id] = TokenBucket(tokens=self.capacity, last_refilled=timestamp)

            user_bucket = self.user_buckets[user_id]
            elapsed = max(0, timestamp - user_bucket.last_refilled)
            user_bucket.tokens = min(self.capacity, user_bucket.tokens + elapsed * self.refill_rate)
            user_bucket.last_refilled = timestamp

            if user_bucket.tokens >= 1:
                user_bucket.tokens -= 1
                return Response(allowed=True, retry_after=0)

            retry_after = (1 - user_bucket.tokens) / self.refill_rate
            return Response(allowed=False, retry_after=retry_after)
            
class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.user_windows: Dict[str, Deque[float]] = {}
        self.lock = Lock()

    def is_allowed(self, request: Request) -> Response:
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            if user_id not in self.user_windows:
                self.user_windows[user_id] = deque()

            user_window = self.user_windows[user_id]

            while user_window and timestamp - user_window[0] >= self.window_size:
                user_window.popleft()

            if len(user_window) < self.max_requests:
                user_window.append(timestamp)
                return Response(allowed = True, retry_after = 0)

            retry_after = user_window[0] + self.window_size - timestamp
            return Response(allowed = False, retry_after = retry_after)

class FixedWindowRateLimiter:
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.user_windows: Dict[str, UserFixedWindow] = {}
        self.lock = Lock()

    def is_allowed(self, request: Request) -> Response:
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            if user_id not in self.user_windows:
                self.user_windows[user_id] = UserFixedWindow(window=0, count = 0)

            curr_window = timestamp // self.window_size

            user_window = self.user_windows[user_id]

            if user_window.window != curr_window:
                user_window.window = curr_window
                user_window.count = 0

            if user_window.count < self.max_requests:
                user_window.count += 1
                return Response(allowed = True, retry_after = 0)

            retry_after = ((curr_window + 1) * self.window_size) - timestamp
            return Response(allowed = False, retry_after = retry_after)

class SlidingWindowCounterRateLimiter:
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.user_windows: Dict[str, UserSlidingWindow] = {}
        self.lock = Lock()

    def is_allowed(self, request: Request) -> Response:
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            if user_id not in self.user_windows:
                self.user_windows[user_id] = UserSlidingWindow(start = 0, current_count=0, previous_count=0)

            curr_window_start = (timestamp // self.window_size) * self.window_size

            user_window = self.user_windows[user_id]

            if user_window.start != curr_window_start:
                if curr_window_start - user_window.start > self.window_size:
                    user_window.previous_count = 0
                else:
                    user_window.previous_count = user_window.current_count
                user_window.current_count = 0
                user_window.start = curr_window_start

            elapsed = timestamp - curr_window_start
            weight = (self.window_size - elapsed) / self.window_size

            estimated_count = user_window.previous_count * weight + user_window.current_count

            if estimated_count < self.max_requests:
                user_window.current_count += 1
                return Response(allowed = True, retry_after = 0)

            retry_after = self.window_size - elapsed
            return Response(allowed = False, retry_after = retry_after)

class LeakyBucketRateLimiter:
    def __init__(self, capacity: int, leak_rate: int):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.user_buckets: Dict[str, LeakyBucket] = {}
        self.lock = Lock()

    def is_allowed(self, request: Request) -> Response:
        with self.lock:
            user_id = request.user_id
            timestamp = request.timestamp

            if user_id not in self.user_buckets:
                self.user_buckets[user_id] = LeakyBucket(requests=deque(), last_leaked=timestamp)

            user_bucket = self.user_buckets[user_id]
            elapsed = max(0, timestamp - user_bucket.last_leaked)
            leaked = min(len(user_bucket.requests), int(elapsed * self.leak_rate))
            
            if leaked > 0:
                 user_bucket.last_leaked += leaked / self.leak_rate

            while leaked > 0:
                user_bucket.requests.popleft()
                leaked -= 1

            if len(user_bucket.requests) < self.capacity:
                user_bucket.requests.append(timestamp)
                return Response(allowed = True, retry_after = 0)

            retry_after = max(0, (1 / self.leak_rate) - (timestamp - user_bucket.last_leaked))
            return Response(allowed = False, retry_after = retry_after)