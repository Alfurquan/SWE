# Problem: Minimum Meeting Cancellations
You manage a single conference room. You're given a list of meeting requests intervals, where intervals[i] = [start_i, end_i]. Two meetings conflict if they overlap (a meeting ending exactly when another starts does not conflict — end is exclusive).

Since only one meeting can run at a time, you must cancel some meetings so that the remaining ones are all non-overlapping. Return the minimum number of meetings you must cancel.

Example 1
```
Input:  intervals = [[1,2], [2,3], [3,4], [1,3]]
Output: 1
```
Example 2
```
Input:  intervals = [[1,2], [1,2], [1,2]]
Output: 2
```

Example 3
```
Input:  intervals = [[1,2], [2,3]]
Output: 0
```

## Solution

As I get from the problem, we need to find the count of non overlapping intervals, lets say if its count, then the answer would be total - count.

For this we would sort by end time in asc order, as we would iterate over the meetings array and then compare the start time of the next meeting with the end of last non overlapping meeting. 

Here is the high level algorithm of the approach

- Initialize count = 1
- Sort meetings by end time
- Initialize end = meetings[0][1]
- for index in range(1, len(meetings)):
    - meeting = meetings[index]
    - if meeting[0] >= end:
        count += 1
        end = meeting[1]

- return len(meetings) - count

## Time complexity

- O(NlogN) for sorting

## Space complexity

- O(1)
