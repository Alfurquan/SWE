from collections import deque
from typing import Deque, Dict, Tuple, List
from sortedcontainers import SortedSet

class TrendingTopics:
    def __init__(self, k: int, window_size: int):
        self.k = k
        self.window_size = window_size
        self.counts: Dict[str, int] = {}
        self.topics: Deque[Tuple[int, str]] = deque()
        self.trending_set: SortedSet[Tuple[int, str]] = SortedSet()
        self.watermark = 0

    def process_topic(self, topic: str, timestamp: int):
        self.watermark = max(self.watermark, timestamp)

        # Cleanup as window slides
        while self.topics and self.topics[0][0] <= (self.watermark - self.window_size):
            _, old_topic = self.topics.popleft()
            old_count = self.counts[old_topic]
            new_count = old_count - 1
            self.trending_set.remove((old_count, old_topic))

            if new_count > 0:
                self.counts[old_topic] = new_count
                self.trending_set.add((new_count, old_topic))
            else:
                self.counts.pop(old_topic)

        # Addition logic
        self.topics.append((timestamp, topic))
        
        if topic not in self.counts:
            self.counts[topic] = 1
            self.trending_set.add((1, topic))
            return
        
        old_count = self.counts[topic]
        self.trending_set.remove((old_count, topic))
        self.counts[topic] = self.counts.get(topic, 0) + 1
        self.trending_set.add((old_count + 1, topic))

    def get_trending(self) -> List[str]:
        limit = min(self.k, len(self.trending_set))
        return [self.trending_set[-1 - i] for i in range(limit)]