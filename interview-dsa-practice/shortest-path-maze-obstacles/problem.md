# Problem: Shortest Path Through a Maze with Limited Drilling
You're given an m x n grid where each cell is either 0 (open) or 1 (a wall). You start at the top-left (0, 0) and want to reach the bottom-right (m-1, n-1), moving 4-directionally (up/down/left/right).

You have a drill that can eliminate up to k walls over the course of your journey. Passing through a wall consumes one drill charge; passing through an open cell is free.

Return the length of the shortest path (number of steps) from (0,0) to (m-1, n-1) such that you eliminate at most k walls along the way. If there's no such path, return -1.

Example 1
```
Input:  grid = [[0,0,0],
                [1,1,0],
                [0,0,0],
                [0,1,1],
                [0,0,0]],  k = 1
Output: 6
```

Example 2
```
Input:  grid = [[0,1,1],
                [1,1,1],
                [1,0,0]],  k = 1
Output: -1
```

Example 3
```
Input:  grid = [[0]],  k = 0
Output: 0
```

## Solution

We will use BFS here to solve the problem as we need to find the shortest path from from (0,0) to (m - 1, n - 1) and BFS helps will help us to traverse the grid in level by level fashion and in finding the shortest path from one point to the other. We are not using Dijkstra here as the cost involved in moving from one point to the other is just 1 so using it here would be an overkill. BFS works best to find shortest path from one point to the other with unit cost.

We would use BFS but will tweak the state a bit for it. Instead of just storing the (row, col), we would store (row, col, dist, obs_remaining), where row = row, col = col, dist = dist of (row, col) from (0, 0) and obs_remaining is the no of obstacles left that we can removed.

Also in order to avoid visiting the same cell with the same state we would track visited state as (row, col, obs_remaining)

Here is the high level algorithm

- Initialize queue: Deque[Tuple[int, int, int, int]] = deque
- Initialize visited: Dict[Tuple[int, int, int], bool] = {}
- Initialize dirs: List[List[int, int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]
- if grid[0][0] == 1
    - k -= 1
- Push (0, 0, 0, k) to the queue
- visited[(0, 0, k)] = true
- while queue
    - pop row, col, dist, obstacles from queue
    - if row == rows - 1 and col == cols - 1
        - return dist
    - for dir in dirs
        - obs = obstacles
        - nrow = row + dir[0]
        - ncol = col + dir[1]
        - if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols
            - continue
        - if grid[nrow][ncol] == 0 and obs >= 0 and (nrow, ncol, obs) not in visited
            - push nrow, ncol, dist + 1, obs to queue
            - visited[(nrow, ncol, obs)] = true
        - elif grid[nrow][ncol] == 1 and obs - 1 >= 0 and (nrow, ncol, obs - 1) not in visited:
            - push nrow, ncol, dist + 1, obs - 1 to queue
            - visited[(nrow, ncol, obs - 1)] = true

- return -1

## Time complexity

- We visit each state exactly once, since there are m rows and n cols, and k obstacles, the time complexity here would O(k * m * n)

## Space complexity

- O(k * m * n) for queue and visited dict.