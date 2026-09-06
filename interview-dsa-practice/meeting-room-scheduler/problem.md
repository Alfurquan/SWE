# Problem: Meeting Room Scheduler

You're building the backend for a room-booking system at a large office. You're given a list of meeting time intervals where intervals[i] = [start_i, end_i] (using a 24-hour integer clock, e.g. 930 for 9:30, or just treat them as generic integers).

## Part 1
Given the list of intervals, determine the minimum number of meeting rooms required so that no two overlapping meetings share a room.

Note: A meeting that ends at time t and another that starts at time t do not conflict (end is exclusive).

Example

```
Input:  intervals = [[0, 30], [5, 10], [15, 20]]
Output: 2
```

```
Input:  intervals = [[7, 10], [2, 4]]
Output: 1
```

## Solution

Here is how I would approach this problem. So just re iterating, we have a list of intervals which are not sorted. We need to determine the minimum number of meeting rooms required so that no two overlapping meetings share a room.

First of here is the data structure I would use for this problem

- Min Heap: I would use a min heap to store all active meetings ordered by end time. This is to make sure we always get the meeting finishing first at the top of the heap.

High level approach

- Sort the list by start time to make the intervals appear in order of start time
- Initialize max_rooms = 0, min_heap = []
- Loop over the intervals, for each interval i = [si, ei]
    - While min_heap is not empty and min_heap[0][1] <= si
        - pop items from min_heap
    - push interval i to the min_heap
    - max_rooms = max(max_rooms, len(min_heap))
- Return max_rooms

### Time complexity

Sorting the list - O(NlogN), N = no of intervals
Min heap operations - O(logN), loop and min heap operations take O(NlogN)

### Space complexity

O(N), N = no of intervals.

## Part 2 — The Follow-up
Now the interviewer leans in:

```
"Great. The facilities team loves this. But now they don't just want the count — they want the actual room assignments. Modify your solution so that each meeting is assigned a specific room number (0-indexed), reusing rooms whenever possible. Return a list where result[i] is the room number assigned to intervals[i] (in the original input order)."
```

Example

```
Input:  intervals = [[0, 30], [5, 10], [15, 20]]
Output: [0, 1, 1]
```

## Solution

Here is how I will approach this problem and tweak my earlier solution.

- Instead of sorting the original list, I would store the original list into another List of objects of type lets say MeetingInterval which has the original Meeting along with the index of the meeting. This index would be used to map the room to the meeting in the final result. Lets call this list as meeting_intervals.
- We also add the _lt_ magic function to the MeetingInterval class with logic same as Meeting in the original answer.
- Sort the meeting_intervals by meeting.start_time
- Initialize a counter, busy_room_count = 0, min_heap = [], free_rooms = [0], here free_rooms will be a heap of free_rooms
- Initialize a List to hold meeting room assignments result = [0] * n, where n = len(meeting_intervals)
- Loop over meeting_intervals, for each interval i = [si, ei, index]:
    - while min_heap is not empty and min_heap[0].end_time <= si:
        - pop from min_heap, get the assigned room number, say room_i
        - busy_room_count -= 1
        - Add room_i to the free_rooms

    if free_rooms heap is empty:
        - push busy_room_count to the free_rooms heap
    - pop lowest free room from the free_rooms heap, lets say room_i
    - push interval i and the room_i in the min_heap
    - result[index] = room_i
    - busy_room_count += 1
- return result

## Time complexity

Here again sorting would take O(NlogN) time. Also looping and heap operations would take O(NlogN) time

## Space complexity

O(N) for heap, result list

