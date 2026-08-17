# Top-K Most Viewed Videos in a Stream

Scenario: You are building the real-time analytics backend for a video platform (like YouTube). View events arrive as a continuous stream. At any point, the system needs to efficiently answer: "What are the top K videos by view count?"

## Problem

Design a class TopKVideoTracker that supports the following operations:

```python
class TopKVideoTracker:
    def __init__(self, k: int):
        # Initialize tracker for top-k videos
        pass

    def record_view(self, video_id: str) -> None:
        # Record a single view event for a video
        pass

    def get_top_k(self) -> List[Tuple[str, int]]:
        # Return the current top-k videos as (video_id, view_count)
        # sorted by view_count descending. Break ties by lexicographic order of video_id.
        pass

    def reset(self, video_id: str) -> None:
        # Simulate a time-window reset: set a video's count to 0
        # (e.g., for sliding window aggregation)
        pass
```

---

## Solution

Here is a high level approach for this problem which I can think of.

### Data structures

- video_to_count: Dict[str, int] — video_id → current view count
- count_to_videos: Dict[int, SortedSet[str]] — count → sorted set of video_ids with that count (sorted handles tie-breaking)
- active_counts: SortedList[int] — sorted collection of counts that have at least one video (handles sparse bucket traversal)

### Algorithm

record_view(video_id) — O(log M) where M = unique active counts

- Look up old_count = video_to_count.get(video_id, 0)
- Set new_count = old_count + 1
- Update video_to_count[video_id] = new_count
- If old_count > 0: remove video_id from count_to_videos[old_count]. If that set becomes empty, remove old_count from both count_to_videos and active_counts.
- Add video_id to count_to_videos[new_count] (create the set if needed). If new_count is new, add it to active_counts.

- get_top_k() - O(K + log M)
    - Iterate active_counts from the highest value downward.
    - At each count, iterate the sorted set in lexicographic order, collecting (video_id, count).
    - Stop once you've collected K items.
    - Return the collected list.

- reset(video_id) — O(log M)
    - Look up old_count = video_to_count.get(video_id, 0). If 0, do nothing.
    - Remove video_id from count_to_videos[old_count]. If that set becomes empty, remove old_count from both count_to_videos and active_counts.
    - Remove video_id from video_to_count (or set to 0 — your choice; removing saves space).

### Space complexity

- O(N) for video_to_count
- O(M), M = total no of unique counts