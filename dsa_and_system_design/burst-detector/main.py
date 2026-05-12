from typing import Dict, Deque, Tuple
from sortedcontainers import SortedSet
from dataclasses import dataclass

@dataclass
class Log:
    api_key: str
    timestamp: int

class BurstDetector:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.request_log: Dict[str, Deque[int]] = {}
        self.old_expiry: Dict[str, int] = {}
        self.watermark = 0
        self.expiry_queue: SortedSet[Tuple[int, str]] = SortedSet()
        self.first_violator: str = None

    def process_log(self, log: Log) -> str:
        self.watermark = max(self.watermark, log.timestamp)

        # clean up api keys whoes expiry gone stale with current watermark
        while self.expiry_queue and self.expiry_queue[0][0] <= self.watermark:
            _, expired_key = self.expiry_queue.pop(0)
            self.old_expiry.pop(expired_key, None)
            self.request_log.pop(expired_key, None)

        if log.api_key not in self.request_log:
            self.request_log[log.api_key] = Deque()

        self.request_log[log.api_key].append(log.timestamp)

        if log.api_key in self.old_expiry:
            old_expiry_time = self.old_expiry.pop(log.api_key)
            self.expiry_queue.remove((old_expiry_time, log.api_key))
            expiry_time = log.timestamp + self.m
            self.expiry_queue.add((expiry_time, log.api_key))
            self.old_expiry[log.api_key] = expiry_time
        else:
            expiry_time = log.timestamp + self.m
            self.expiry_queue.add((expiry_time, log.api_key))
            self.old_expiry[log.api_key] = expiry_time

        # Sliding the window for the current api key and check if it has violated the threshold
        while self.request_log[log.api_key] and self.request_log[log.api_key][0] < log.timestamp - self.m:
            self.request_log[log.api_key].popleft()
        
        if len(self.request_log[log.api_key]) >= self.n and self.first_violator is None:
            self.first_violator = log.api_key
        
        return self.first_violator

    def get_first_violator(self) -> str:
        return self.first_violator
