# The Car Rental Optimizer

You're building the assignment engine for a car rental fleet. Given N available cars and a list of rental requests (each with a pickup time, return time, and ID), assign cars to maximize utilization while using the minimum number of cars possible.

Each car can serve multiple non-overlapping requests. A car returned at time T is immediately available for a new pickup at time T.

Example:

```
N = 3
requests = [
  {id: 1, pickup: 0, return: 5},
  {id: 2, pickup: 2, return: 7},
  {id: 3, pickup: 5, return: 9}
]
```

Output

```
[
  {requestId: 1, carId: 0},
  {requestId: 2, carId: 1},
  {requestId: 3, carId: 0}
]
```

Requirements

Implement `assign_cars(n: int, requests: List[Request]) -> List[Assignment]`

- Minimize the number of cars used
- Each request must be served (assume N is always sufficient)
- If a car is available at the exact return time of its last request, it can take a new one
- Return the assignment mapping (request_id → car_id)

---

## Solution

### Approach

Data structures used:

- Min heap to store the request and the car assigned to it. The heap is sorted by the return time of the request. This allows us to efficiently find the next available car for a new request.

- List to store the result of the assignment.

Logic

- Sort the request by pickup time so that the requests are processed in the order they arrive.
- Initialize a min heap to keep track of the cars and their return times. Each entry in the heap will be a tuple of (return_time, car_id).
- Initialize a list of free car ids set to 0 to N-1, where N = no of cars
- For each request in the sorted list:
  - While the heap is not empty and the earliest return time in the heap is less than or equal to the current request's pickup time, pop from the heap and add it to the list of free cars. This means that car is now available for a new request.
  - If list of free cars is empty, then wait till the earliest return time in the heap, pop it, and add it to the list of free cars.
  - Pop a car_id from the list of free cars and assign it to the current request.
  - Push the current request's return time and assigned car_id into the heap.
  - Append the assignment to the result list.
- At the end return the assignment result back.

### Time complexity

- Sorting the request list of length N takes O(NlogN) time
- Processing each request takes O(logK) time where K is the number of cars used (which is at most N). Therefore, the overall time complexity is O(NlogN + NlogK) which simplifies to O(NlogN).

### Space complexity
- The space complexity is O(N) for storing the assignments and the heap, where N is the number of requests.
