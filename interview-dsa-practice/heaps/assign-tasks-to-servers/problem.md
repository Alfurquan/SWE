# Problem: Assign Tasks to Servers
You have servers and tasks.

- servers[i] is the weight of server i (lower weight = preferred).
- tasks[j] is the time (number of seconds) task j takes to run.
Tasks arrive one per second: task j becomes available at second j. Tasks must be assigned in order (task 0, then 1, ...). At each second, you assign as many waiting tasks as there are free servers.

Assignment rule: a waiting task goes to the free server with the smallest weight; ties broken by smallest index. If no server is free when a task is waiting, it waits until one frees up (a server frees when its task completes).

When a server finishes a task at time t, it becomes free and can pick up a waiting task at time t.

Return an array ans where ans[j] is the index of the server that task j is assigned to.

Example 1
```
Input:  servers = [3, 3, 2], tasks = [1, 2, 3, 2, 1, 2]
Output: [2, 2, 0, 2, 1, 2]
```

Example 2
```
Input:  servers = [5, 1, 4, 3, 2], tasks = [2, 1, 2, 4, 5, 2, 1]
Output: [1, 4, 1, 4, 1, 3, 2]
```

## Problem

I would solve this problem using two min heaps, one would store free servers ordered by weight and index and another would store tasks in progress in server ordered by end time. Min heap will be used as it gives O(1) time to find min and O(logN) time to pop min element from a set of elements, in our use case since we want to find min weight server and tasks finsihing first, min heap is the ideal choice for both.

Here is the high level algorithm for the approach - 

- Initialize free_servers: List[Tuple[int, int]] = [] // (weight, index) min heap for free servers ordered by their weights and index
- Initilaize busy_servers: List[Tuple[int, int]] // (end_time, server_index), min heap for busy servers ordered by end time and server index
- Initialize result: List[int] = [0] * len(tasks)
- for index in range(len(servers)):
    - heapq.heappush(free_servers, (servers[index], index))
- time = 0
- for index in range(len(tasks)):
    - time = max(time, index)

    // Wait till a server becomes free, advance time to next server becoming free
    - if len(free_servers) == 0:
        time = busy_servers[0][0]

    - while busy_servers and busy_servers[0][0] <= time:
        - _, server = heapq.heappop(busy_servers)
        - heapq.heappush(free_servers, (servers[server], server))

    - server_wt, server_index = heapq.heappop(free_servers)
    - result[index] = server_index
    - heapq.heappush(busy_servers, (time + tasks[index], server_index))

- return result

## Time complexity

- O(NlogN), N = for looping over N tasks and logN for heap push and pop operations

## Space complexity

- O(N) for two heaps and results array.
