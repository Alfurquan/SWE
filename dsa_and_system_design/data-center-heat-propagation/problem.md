# Data Center Heat Propagation
You're monitoring a data center floor represented as an m x n grid. Each cell holds one of:

2 — an overheating rack (a heat source),
1 — a healthy rack,
0 — an empty floor tile (no rack).
Every minute, any healthy rack (1) that is 4-directionally adjacent (up/down/left/right) to an overheating rack becomes overheating itself. Empty tiles (0) never overheat and do not conduct heat.

Return the minimum number of minutes that must elapse until no healthy rack remains. If it's impossible for all healthy racks to overheat, return -1.

Example 1

```
Input:  grid = [[2,1,1],
                [1,1,0],
                [0,1,1]]
Output: 4
```

Example 2
```
Input:  grid = [[2,1,1],
                [0,1,1],
                [1,0,1]]
Output: -1
```

## Solution

This problem is a BFS problem as we need to find minimum no of minutes that must elapse until no healthy rack remains. Since we need minimum amount of time, BFS which traverses level by level helps us in achieving it.

Here its a multi source BFS as there are multiple overheating rack emitting heat, so we need to start BFS from all of them to traverse the grid and compute the minimum time.

We track the minutes elapse by traversing the grid using BFS level by level, at each level we increment time elapsed.

We count the no of healthy racks and after BFS completion we check if no of healthy reacks are not zero means there are still some healthy racks which could not be reached by BFS, so its an impossible case, and we return -1

Here is the high level approach

- Initialize, num_healthy = 0
- Initialize, dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]] for tracking 4-directional grid traverse
- Initialize queue to hold a tuple - (row, col) for the coordinates in the grid
- Loop over rows
    - Loop over cols
        - for each (row, col)
        - if grid[row][col] == 2:
            - push (row, col) to queue
        - elif grid[row][col] == 1:
            - num_healthy += 1

- Initialize, min_time = 0
- while queue and num_healthy > 0:
    - min_time += 1
    - size = len(queue)
    - for _ in range(size)
        - (row, col) = queue.popleft()
        - for dir in dirs
            - nrow = row + dir[0]
            - ncol = col + dir[1]
            - if nrow > rows or nrow < 0 or ncol >= cols or ncol < 0:
                - continue
            - if grid[nrow][ncol] == 1
                - queue.append((nrow, ncol))
                - grid[nrow][ncol] = 2
                - num_healthy -= 1

- return -1 if num_healthy > 0 else min_time

## Time complexity

- O(rows * cols) for looping over the grid to push to queue and determine num_healthy
- Also at worst case each (row, col) ges pushed and popped from the queue at most once, so while runs O(row * col) times

## Space complexity

- O(rows * cols) for the queue holding the (row, col) in the grid