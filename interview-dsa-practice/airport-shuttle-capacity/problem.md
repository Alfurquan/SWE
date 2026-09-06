# Problem: Airport Shuttle Capacity
You operate a single shuttle at an airport that runs along a fixed route with numbered stops 0, 1, 2, .... The shuttle has a fixed passenger capacity.

You're given a list of ride requests where trips[i] = [num_passengers, pickup_stop, dropoff_stop], meaning num_passengers want to board at pickup_stop and get off at dropoff_stop. The shuttle only ever drives forward (stop numbers strictly increase), and a passenger occupies a seat over the interval [pickup_stop, dropoff_stop) — i.e., they free their seat exactly at the dropoff stop, so someone else can board there.

Return True if it's possible to complete all the given trips without ever exceeding capacity at any point along the route; otherwise return False.

Example 1

```
Input:  trips = [[2, 1, 5], [3, 3, 7]], capacity = 4
Output: False
```

## Solution

### How it relates to earlier problem

It relates in the sense that we a have list of something, here it is list of trip, there it was meeting and we need to determine something from it.

Difference, in the earlier problem it was determining the min number of meeting rooms needed. Here it is about determining if its possible to complete all the trips.

### Approach

Here is my high level approach for the problem. The data structure which I would use here is a min heap to store all active trips ordered by when then trip will get over. 

Reason to use a min heap: I have used min heap here as it gives O(1) time complexity to find the minimum element in a list, here it will be the trip finishing first and O(logN) time to pop and insert items to it.

Here is the high level algorithm

- Sort trip by pickup stop
- Initialize current_capacity = capacity
- Initialize active_trips = [], here active_trips would be the min heap which would store a tuple - [drop_stop, num_pass]
- Loop over the trips list, for each trip t = [ni, pi, di]
    - while active_trips and active_trips[0][0] <= pi
        - pop from active_trips, increment current_capacity by num_pass from popped entry
    - If ni > current_capacity
        return False
    - current_capacity -= ni
    - Push [di, ni] to active_trips
- return True

### Time complexity

- Heap operations take O(logN) time, where N = no of trips, now looping over the trips and doing heap operations take O(NlogN) time. Also sorting takes O(NlogN) time.

### Space complexity

- O(N) to store the active trips

## Part 2 — The Follow-up

"The shuttle operator now says: 'False isn't actionable. Tell me the single busiest stretch.' Return the maximum number of passengers on board at any point during the route, given all trips are accepted (ignore capacity for this part). If there are ties, that's fine — just return the peak count."

Example

```
Input:  trips = [[2, 1, 5], [3, 3, 7], [1, 4, 6]]
Output: 6
```

### Approach

- Sort the trips list by pickup point so that the trips are ordered by pickup point
- Initialize max_passengers = 0, active_passengers = 0, active_trips = [], active trips will be a min heap which will hold the tuple of form [drop, num_pass] ordered by drop.
- Loop over trips, for each trip ti = [ni, pi, di]
    - while active_trips and active_trips[0][0] <= pi
        - pop from active_trips
        - decrement active_passengers by the num_pass from the popped trip
    - push ti to active_trips
    - active_passengers += ni
    - max_passengers = max(max_passengers, active_passengers)
- return max_passengers

### Time complexity

- O(NlogN), for sorting, loop and heap operations

### Space complexity

- O(N), N = No of trips
