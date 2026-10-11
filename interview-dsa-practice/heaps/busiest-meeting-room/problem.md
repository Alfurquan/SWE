# Problem: Busiest Meeting Room

You have n meeting rooms numbered 0 to n - 1. You're given meetings where meetings[i] = [start_i, end_i] (half-open: a meeting occupies [start, end)). All start_i are distinct.

Meetings are assigned to rooms by these rules, processed in order of start time:

Each meeting is held in the lowest-numbered available room.
If no room is free, the meeting is delayed until a room frees up. It keeps its original duration, and is assigned to the room that frees up first (ties broken by lowest room number). A delayed meeting's start shifts later, but its length stays the same.
Return the number of the room that held the most meetings. If there's a tie, return the lowest-numbered such room.

Example 1
```
Input:  n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]]
Output: 0
```

Example 2
```
Input:  n = 3, meetings = [[1,20],[2,10],[3,5],[4,9],[6,8]]
Output: 1
```

## Solution

Here is my approach for solving this problem. I would sort the meetings list by start time so that we process the meetings in order. I would use min heap here and two min heaps - 

- One min heap to track the lowest available room num for assigning meetings to
- One min heap to track the earliest meeting getting over

Used min heaps here as min heaps give O(1) complexity for finding min and O(logN) for extracting min object from a collection.

Here is the high level algorithm for the approach - 

- Initialize free_rooms: List[int] = [], appointments: List[Tuple[int, int]] = []
- for i in range(0, n):
    - heapq.heappush(free_rooms, i)
- Initialize count: List[int] = [0] * n  // For tracking count of meetings in a room
- Initialize best_room = 0
- meetings.sort(key=lambda meeting: meeting[0])  // Sort the meetings by start time
- for meeting in meetings:
    - while appointments and appointments[0][0] <= meeting[0]:
        - _, room = heapq.heappop(appointments)
        - heapq.heappush(free_rooms, room)
    
    - best_start_time = meeting[0]

    - if len(free_rooms) == 0:
        - end_time, room = heapq.heappop(appointments)
        - best_start_time = end_time
        - heapq.heappush(free_rooms, room)

    - room = heapq.heappop(free_rooms)
    - meeting_end_time = best_start_time + (meeting[1] - meeting[0])
    - heapq.heappush(appointments, (meeting_end_time, room))
    - count[room] += 1
    - if count[room] > count[best_room]:
        - best_room = room
    - elif count[room] == count[best_room]:
        - best_room = min(room, best_room)
- return best_room

## Time complexity 

- O(NlogN) for sorting the meeting list, O(NlogN), for looping and heap operations.

## Space complexity

- O(N) for heaps, counts list.


