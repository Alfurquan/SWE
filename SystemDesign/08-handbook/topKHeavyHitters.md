# Top K Problem - Heavy Hitters

## Introduction

The “Top K Problem” is a classic and frequently encountered challenge in system design interviews. It revolves around identifying the k most frequent or largest elements from a given dataset. This dataset can be static and finite, or more commonly in modern systems, a continuous, unbounded stream of data. The “Heavy Hitters” variant specifically refers to finding elements that appear with a frequency above a certain threshold, often implying a significant proportion of the total data.

## Defining the problem scope

At its core, the Top K Problem asks us to find the `k` elements with the highest frequency or value. However, the context in which this problem arises significantly impacts the optimal solution.

Key dimensions:

### Data source

- Static data: The entire dataset is available at once. This simplifies the problem as we can process all data without worrying about future arrivals. Examples include finding the top 10 most common words in a book or the top 5 highest scores in a game’s leaderboard.

- Streaming data: Data arrives continuously and often at a high velocity. We cannot store the entire stream, and processing must be done in a single pass or with limited memory. This is the more challenging and common scenario in real-world distributed systems. Examples include finding trending topics on Twitter, top viewed videos on YouTube, or most frequent IP addresses accessing a server.

### Constraints

- Memory: How much memory is available? For massive datasets or streams, storing all elements and their counts might be impossible.
- Time: What are the latency requirements? Can we afford to sort the entire dataset, or do we need real-time updates?
- Accuracy: Is an exact answer required, or is an approximate answer acceptable? For many streaming applications, a small margin of error is tolerable if it significantly reduces resource consumption.

## Core concepts and building blocks

Before diving into specific algorithms, let’s review some fundamental concepts.

### Frequency counting

The most basic operation is to count the occurrences of each item. A hash map (or dictionary) is the go-to data structure for this.

- Key: The item itself (e.g., word, IP address).
- Value: The frequency count.

```python
frequency_map = {}
for item in data_stream:
    if item in frequency_map:
        frequency_map[item] += 1
    else:
        frequency_map[item] = 1
```

This approach works well for static data or streams where the number of unique items is small enough to fit in memory.

### Data streams

A data stream is an ordered sequence of items that arrives continuously. Key characteristics:

- Unbounded: The stream has no defined end.
- High Velocity: Items arrive rapidly.
- Single Pass: Algorithms typically process each item once due to memory constraints.
- Limited Memory: We cannot store the entire stream.

### Approximate Solutions

When dealing with massive data streams and strict memory constraints, exact solutions become infeasible. Approximate algorithms provide a trade-off: they use significantly less memory and time but might return results with a small error margin. For many applications (e.g., trending topics), this approximation is perfectly acceptable.

## Exact solutions for static or small datasets

For scenarios where the entire dataset can be held in memory, or the stream is small enough to be fully processed, exact solutions are preferred.

### Hash Map + Sorting

Approach

- Iterate through the dataset and use a hash map to store the frequency of each item.
- Once all items are processed, extract the entries (item, count) from the hash map.
- Sort these entries in descending order based on their counts.
- Take the top k elements from the sorted list.

Time Complexity

- Counting frequencies: O(n), where n is the number of items.
- Sorting: O(m log m), where m is the number of unique items.
- Overall: O(n + m log m)

Space Complexity

- O(m) for the hash map.

Pros

- Simple and straightforward.
- Exact results.

Cons

- Not suitable for large datasets or streams due to memory and time constraints.
- Sorting step can be expensive if the number of unique items is large.

### Min-Heap

This is a more efficient approach when k is much smaller than the total number of unique items.

Approach

- Use a hash map to count frequency of each item.
- Create a min-heap of size k. The heap will store (item, count) pairs, ordered by count.
- For each entry in the hash map:
  - If the heap has less than k elements, add the new entry.
  - If the heap is full and the new entry’s count is greater than the smallest count in the heap (the root), pop the root and insert the new entry.
- After processing all entries, the heap contains the top k items.

Time Complexity

- Counting frequencies: O(n)
- Heap operations: O(m log k), where m is the number of unique items.
- Overall: O(n + m log k)

Space Complexity

- O(m) for the hash map and O(k) for the heap.
- Overall: O(m + k)

Pros

- More efficient than sorting when k << m.
- Exact results.

Cons

- Still requires storing all unique items in memory.
- Heap operations add some overhead.

## Approximate solutions for large-scale streaming data

When dealing with high-volume, unbounded data streams where memory is a critical constraint, we must resort to approximate algorithms. These algorithms aim to identify heavy hitters with high probability and bounded error, using sub-linear space (often poly-logarithmic or even constant space relative to the stream size).

### Count-Min Sketch

The Count-Min Sketch is a probabilistic data structure used for estimating frequencies of items in a data stream. It’s particularly good for point queries (estimating the frequency of a specific item) and finding heavy hitters.

How it works

- Data structure: A 2D array (matrix) of counters, with dimensions w (width) and d (depth). Each row corresponds to a different hash function.
- Hash functions: d independent hash functions, h_1, h_2, ..., h_d, each mapping an item to an index within [0, w-1].
- Update: For each item x, for each hash function h_i, increment the counter at position (i, h_i(x)).
- Query: To estimate the frequency of an item x, compute the minimum value among the counters at positions (i, h_i(x)) for all i.

Finding Heavy Hitters with Count-Min Sketch: After processing the stream, iterate through all items (or a sample of items) and query their estimated frequencies. If an item’s estimated frequency exceeds a certain threshold, it’s considered a heavy hitter. A common strategy is to maintain a small min-heap of potential heavy hitters alongside the sketch.

### Lossy Counting Algorithm

Lossy Counting is another popular algorithm for finding frequent items (heavy hitters) in data streams with bounded error. It’s designed to be more accurate than Count-Min Sketch for finding items above a specific frequency threshold.

How it works

- Buckets: The stream is divided into “windows” or “buckets” of size W = 1/ε, where ε is the maximum allowed error.
- Data structure: A list of (item, frequency, delta) tuples. delta represents the maximum possible error in the frequency count for that item.
- Processing: For each incoming item x:
  - If x is already in the list, increment its frequency.
  - If x is new, add (x, 1, current_bucket_id - 1) to the list.
  - At the end of each bucket (every W items):
    Scan the list. For any (item, frequency, delta) where frequency + delta <= current_bucket_id, remove it. This “pruning” step removes items that are unlikely to be heavy hitters.

Finding Heavy Hitters: After processing the entire stream, any item (item, frequency, delta) in the list where frequency >= (s - ε) * N (where s is the support threshold, ε is the error, and N is the total stream length) is reported as a heavy hitter.

## System Design Considerations for Distributed Top K

When the data stream is so massive that it cannot be processed by a single machine, we need to consider distributed approaches.

### Sharding and Partitioning

The most common strategy is to distribute the incoming data across multiple worker nodes.

- Hash-based Sharding: Items are hashed, and the hash value determines which worker node processes the item. This ensures that all occurrences of a specific item go to the same worker, allowing that worker to maintain an accurate local count for that item.

Challenge: Skewed data (some items are much more frequent than others) can lead to hot spots where certain worker nodes are overloaded.

- Random Sharding: Items are randomly distributed. This balances the load but means that occurrences of the same item can be spread across multiple workers, making global frequency counting difficult.

### Aggregation and Merging

Regardless of sharding strategy, a central aggregator or a multi-stage aggregation process is often needed.

- Local Top K: Each worker node computes its local Top K items using one of the in-memory algorithms (e.g., Min-Heap).
- Global Aggregation: The local Top K lists (or sketches) are sent to a central aggregator. The aggregator then merges these lists/sketches to compute the global Top K.
- Merging Min-Heaps: If each worker sends its local min-heap, the aggregator can merge them by putting all elements into a single large min-heap of size k (or larger, then prune).
- Merging Count-Min Sketches: Multiple Count-Min Sketches can be merged by simply adding their corresponding counters element-wise. This is a powerful feature of CM sketches.

### Windowing

For continuous streams, we often want to find Top K items within a specific time window (e.g., “top 10 trending topics in the last hour”).

#### Sliding Windows

- Tumbling Windows: Non-overlapping, fixed-size windows (e.g., process data for 10:00-10:05, then 10:05-10:10).
- Hopping Windows: Overlapping, fixed-size windows that “hop” forward by a smaller interval (e.g., process data for 10:00-10:10, then 10:01-10:11).

#### Data Structures for Windows

- Count-Min Sketch with Expiration: More complex, but can be adapted to decay counts over time.
- Bucketing by Time: Store counts in buckets corresponding to time intervals. When a window slides, old buckets are discarded, and new ones are added.