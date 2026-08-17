from sortedcontainers import SortedList, SortedSet
from typing import Dict, List, Tuple, Deque
from collections import deque


class TopKVideoViews:
    def __init__(self, k: int):
        self.k = k
        self.video_to_count: Dict[str, int] = {}
        self.count_to_videos: Dict[int, SortedSet[str]] = {}
        self.active_counts: SortedList[int] = SortedList()

    def record_view(self, video_id: str):
        old_count = self.video_to_count.get(video_id, 0)
        new_count = old_count + 1

        self.video_to_count[video_id] = new_count

        if old_count > 0:
            self.count_to_videos[old_count].remove(video_id)
            if len(self.count_to_videos[old_count]) == 0:
                self.count_to_videos.pop(old_count)
                self.active_counts.remove(old_count)

        if new_count not in self.count_to_videos:
            self.count_to_videos[new_count] = SortedSet()
        
        self.count_to_videos[new_count].add(video_id)
        
        if new_count not in self.active_counts:
            self.active_counts.add(new_count)

    def get_top_k(self) -> List[Tuple[str, int]]:
        result = []
        
        for count in reversed(self.active_counts):
            videos = self.count_to_videos[count]
            for video_id in videos:
                result.append((video_id, count))
                if len(result) == self.k:
                    return result
        return result

    def reset(self, video_id: str):
        old_count = self.video_to_count.get(video_id, 0)
        if old_count == 0:
            return

        self.video_to_count.pop(video_id)
        if old_count in self.count_to_videos:
            self.count_to_videos[old_count].remove(video_id)
            if len(self.count_to_videos[old_count]) == 0:
                self.count_to_videos.pop(old_count)
                self.active_counts.remove(old_count)


class TopKVideoViewsWindowed:
    def __init__(self, k: int, window_seconds: int):
        self.k = k
        self.window_seconds = window_seconds
        self.video_to_count: Dict[str, int] = {}
        self.count_to_videos: Dict[int, SortedSet[str]] = {}
        self.active_counts: SortedList[int] = SortedList()
        self.active_views: Deque[Tuple[int, str]] = deque()

    def record_view(self, video_id: str, timestamp: int) -> None:
        self._expire_old_views(timestamp)
        
        old_count = self.video_to_count.get(video_id, 0)
        new_count = old_count + 1

        self.video_to_count[video_id] = new_count

        if old_count > 0:
            self.count_to_videos[old_count].remove(video_id)
            if len(self.count_to_videos[old_count]) == 0:
                self.count_to_videos.pop(old_count)
                self.active_counts.remove(old_count)

        if new_count not in self.count_to_videos:
            self.count_to_videos[new_count] = SortedSet()
        
        self.count_to_videos[new_count].add(video_id)

        if new_count not in self.active_counts:
            self.active_counts.add(new_count)

        self.active_views.append((timestamp, video_id))


    def get_top_k(self, timestamp: int) -> List[Tuple[str, int]]:
        self._expire_old_views(timestamp)

        result: List[Tuple[str, int]] = []

        for count in reversed(self.active_counts):
            for video in self.count_to_videos[count]:
                result.append((video, count))

                if len(result) == self.k:
                    return result
        
        return result

    def _expire_old_views(self, timestamp: int):
        while self.active_views and timestamp - self.active_views[0][0] >= self.window_seconds:
            _, video_id = self.active_views.popleft()

            old_count = self.video_to_count[video_id]
            new_count = old_count - 1

            self.count_to_videos[old_count].remove(video_id)
            if len(self.count_to_videos[old_count]) == 0:
                self.count_to_videos.pop(old_count)
                self.active_counts.remove(old_count)

            if new_count == 0:
                self.video_to_count.pop(video_id)
                continue

            self.video_to_count[video_id] = new_count

            if new_count not in self.count_to_videos:
                self.count_to_videos[new_count] = SortedSet()
            
            self.count_to_videos[new_count].add(video_id)

            if new_count not in self.active_counts:
                self.active_counts.add(new_count)