# Problem: Maximize Scheduled Meetings
You have one conference room and a list of meeting requests, where meetings[i] = [start_i, end_i]. A meeting occupies the room for [start, end) — a meeting ending at time t and another starting at t don't conflict (end is exclusive).

You can only hold non-overlapping meetings in the single room. Return the maximum number of meetings you can schedule.

Example 1
```
Input:  meetings = [[1, 2], [2, 3], [3, 4], [1, 3]]
Output: 3
```

Example 2
```
Input:  meetings = [[1, 4], [2, 3], [3, 5]]
Output: 2
```

## Solution

Here is how I would approach this problem. I would use a greedy approach and a min heap to keep track of the meeting finishing at the earliest time. I would first sort the meetings by start time to process them in order. Then use a min heap to find the meeting finishing at the earliest time in O(1), pop them in O(logN). At any point in time, the size of the heap denotes the no of meetings that can be scheduled.

Here is the high level algorithm for the approach

- Initialize max_meetings = 0
- Intialize min_heap: List[Tuple[int, int]] = []
- Sort meetings by start time 
- for each meeting in meetings:
    - while min_heap and min_heap[0][0] <= meeting.start:
        - pop from min_heap
    - push meeting in min_heap
    - max_meetings = max(max_meetings, len(min_heap))
- return max_meetings

## Time complexity

- O(NlogN) for sorting and O(NlogN) for the heap and the loop

## Space complexity

- O(N) for the heap.
