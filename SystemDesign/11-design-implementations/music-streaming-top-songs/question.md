# 🎧 Music Streaming Service — Phase 1 (Coding)

You are designing a small in-memory service for a music streaming platform.

Implement two operations:

- addSong(songId: str, playCount: int)
- Adds playCount plays to the given songId.

If the song doesn’t exist, create it with that count.
If it already exists, increment its count.

```python
def getTopK(k: int) -> List[str]
```

- Returns the k song IDs with the highest total play counts,
ordered from highest to lowest.
- If there are fewer than k songs, return all of them in order.

Example:

```python
addSong("a", 10)
addSong("b", 5)
addSong("a", 3)
getTopK(1) -> ["a"]
getTopK(2) -> ["a", "b"]
```

Constraints:

- Up to millions of songs.
- addSong and getTopK may be called concurrently.
- playCount ≥ 0.
- You must define how to break ties deterministically.

## 🎧 Music Streaming Service — Phase 2 (System Design)

Now scale this to a global service with millions of users and billions of play events per day.

Design a distributed system that:

Ingests song play events in real time.
Maintains up-to-date play counts.
Serves getTopK(k) queries globally and per-region/genre.
Supports near-real-time updates (low latency).
Handles failures gracefully and remains highly available.

---