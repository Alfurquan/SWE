# Cache Eviction Strategies

Caching is a technique to make applications lightning fast, reduce database load, and improve user experience.

But, cache memory is limited - you can’t store everything.
So, how do you decide which items to keep and which ones to evict when space runs out?
This is where cache eviction strategies come into play. They determine which items are removed to make room for new ones.

## Least recently used (LRU)

LRU evicts the item that hasn’t been used for the longest time.
The idea is simple: if you haven’t accessed an item in a while, it’s less likely to be accessed again soon.

### How it works ?

- Access Tracking: LRU keeps track of when each item in the cache was last accessed. This can be done using various data structures, such as a doubly linked list or a combination of a hash map and a queue.

- Cache Hit (Item Found in Cache): When an item is accessed, it is moved to the most recently used position in the tracking data structure (e.g., moving it to the front of a list).

- Cache Miss (Item Not Found in Cache):

If the item isn’t in the cache and the cache has free space, it is added directly.
If the cache is full, the least recently used item is evicted to make space for the new item.

- Eviction: The item that has been accessed least recently (tracked at the beginning of the list) is removed from the cache.

## Least frequently used (LFU)

LFU evicts the item with the lowest access frequency. It assumes that items accessed less frequently in the past are less likely to be accessed in the future.

Unlike LRU, which focuses on recency, LFU emphasizes frequency of access.

### How it works ?

- Track Access Frequency: LFU maintains a frequency count for each item in the cache, incrementing the count each time the item is accessed.

- Cache Hit (Item Found in Cache): When an item is accessed, its frequency count is increased.

- Cache Miss (Item Not Found in Cache):
If the cache has available space, the new item is added with an initial frequency count of 1.
If the cache is full, the item with the lowest frequency is evicted to make room for the new item. If multiple items share the same lowest frequency, a secondary strategy (like LRU or FIFO) resolves ties.

- Eviction: Remove the item with the smallest frequency count.

## First in first out (FIFO)

FIFO evicts the item that was added first, regardless of how often it’s accessed.

FIFO operates under the assumption that items added earliest are least likely to be needed as the cache fills up.

### How it works ?

- Item Insertion: When an item is added to the cache, it is placed at the end of the queue.

- Cache Hit (Item Found in Cache): No changes are made to the order of items. FIFO does not prioritize recently accessed items.

- Cache Miss (Item Not Found in Cache):
If there is space in the cache, the new item is added to the end of the queue.
If the cache is full, the item at the front of the queue (the oldest item) is evicted to make space for the new item.

- Eviction: The oldest item, which has been in the cache the longest, is removed to make room for the new item.

## Time to Live (TTL)

TTL is a cache eviction strategy where each cached item is assigned a fixed lifespan. Once an item’s lifespan expires, it is automatically removed from the cache, regardless of access patterns or frequency.

This ensures that cached data remains fresh and prevents stale data from lingering in the cache indefinitely.

### How it works ?

- Item Insertion: When an item is added to the cache, a TTL value (e.g., 10 seconds) is assigned to it. The expiration time is usually calculated as current time + TTL.

- Cache Access (Hit or Miss): When an item is accessed, the cache checks its expiration time:
If the item is expired, it is removed from the cache, and a cache miss is recorded.
If the item is valid, it is served as a cache hit.

- Eviction: Expired items are automatically removed either during periodic cleanup or on access.
