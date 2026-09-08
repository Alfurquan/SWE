# Problem: Streaming Median Tracker
You're building a real-time analytics service that ingests a stream of latency measurements. At any moment, an on-call engineer may ask for the median latency seen so far.

Design a data structure that supports two operations:

add_num(num) — ingest an integer num from the stream.
find_median() — return the median of all numbers ingested so far.
Median rule: if the count of numbers is odd, the median is the middle value. If it's even, it's the average of the two middle values (return a float).

Example

```
tracker = StreamingMedian()
tracker.add_num(1)
tracker.find_median()   -> 1.0
tracker.add_num(2)
tracker.find_median()   -> 1.5      # (1 + 2) / 2
tracker.add_num(3)
tracker.find_median()   -> 2.0      # middle of [1,2,3]
```

## Solution

In this problem we need to support two operations - `add_num` to add a integer num from the stream and `find_median` to return the median of all numbers ingested so far.

A naive approach would be to keep appending the numbers to a list as they appear and then on `find_median` sort the list and return the median.

This would be slow because a sort operation would cost O(NlogN), N = no of integers in the list. As N keeps growing, the time complexity for finding the median would be too high.

Alternative and better approach would be to think of the stream of numbers as they appear and try to store them in sorted order. If the numbers are already in sorted order, find_median will just need to return the middle value if N is odd, or average of middle two values if N is even.

Now here's the crux, how can we store the numbers in sorted order efficiently, one way would be to think of the sorted list in two halves, one stores all the numbers less than the median and the other stores all the numbers greater than the median. Here median would be either the max value of the first half or min value of the second halg or average of both of them.

The data structure that we would use here would be a `min_heap` and a `max_heap`. The reason for choosing heap here is that it keeps elements in order, and pushing and popping from it takes O(logN). But peek is O(1) which will make `find_median` calls faster.

The `min_heap` will store the second half while the `max_heap` will store the first half. Also while storing numbers in the heap, we would need to keep the heaps balanced. Here we always keep 1 more element in the max_heap at a point in time.

Here is the high level algorithm for the approach

1. `add_num(num)`
- if len(ma_heap) == 0 or num <= max_heap[0]
    - push num to max_heap
- else
    - push num to min_heap
- if len(min_heap) + 1 < len(max_heap)
    - pop num from max_heap
    - push num to min_heap
- elif len(max_heap) < len(min_heap)
    - pop num from min_heap
    - push num to max_heap

2. `find_median()`
- if len(min_heap) + len(max_heap) % 2 == 0
    - return (peek(min_heap) + peek(max_heap)) / 2
- return peek(max_heap)

## Time complexity

- `add_num`: O(logN), N = no of integers in the heap

- `find_median`: O(1), where peek in heap takes O(1)