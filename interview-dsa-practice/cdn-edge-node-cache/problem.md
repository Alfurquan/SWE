# CDN Edge Node Cache (LFU Eviction Policy)

We are building the caching software for a Google Cloud Content Delivery Network (CDN) edge node. These nodes live close to users (e.g., inside local ISP datacenters) and cache heavy files (videos, images) to reduce latency.

Because edge nodes have strictly limited memory, they can only hold a maximum of capacity files. When the cache is full and a new file needs to be stored, the system must evict an existing file to make room.

To maximize our cache hit rate, we want to implement a Least Frequently Used (LFU) eviction policy with a tie-breaker.

## The Rules of the Cache:

Eviction Base: When the cache is full, evict the file that has the lowest total access frequency.

Eviction Tie-Breaker: If multiple files have the exact same lowest access frequency, evict the one that is the Least Recently Used (LRU) among them.

Every time a file is accessed (either read or overwritten), its access frequency increases by 1, and it becomes the most recently used file for that specific frequency tier.

## Task: Design and implement an LFUCache class with the following methods:

- __init__(self, capacity: int): Initializes the cache with a given integer capacity.

- get(self, file_id: str) -> str: Returns the content of the file_id if it exists in the cache, otherwise returns "" (empty string).

- put(self, file_id: str, content: str) -> None: Updates the content of file_id if it is present, or inserts a new (file_id, content) pair if not. If the cache is at capacity, it must trigger an eviction before inserting.

The Catch: Both get and put must execute in $O(1)$ average time complexity.

---

## Approach

### Data structures

- Dictionary (Hash Map): To store the mapping of file_id to its content, access frequency
- Min frequency variable: To keep track of the minimum access frequency in the cache
- List of Doubly Linked Lists: Each frequency will have its own doubly linked list to maintain the order of files with that frequency (for LRU tie-breaking)

### Logic

- Each time a file is accessed (via get or put), we will:
  - Update its access frequency
  - Move it to the appropriate frequency list
  - Update the minimum frequency if necessary

- When evicting, we will:
    - Look at the minimum frequency list
    - Evict the least recently used file from that list
    - Update the minimum frequency if that list becomes empty
    