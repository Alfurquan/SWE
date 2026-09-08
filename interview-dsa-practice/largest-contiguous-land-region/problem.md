# Problem : Largest Contiguous Land Region
A satellite scan of terrain is given as an m x n grid of 0s and 1s, where 1 is land and 0 is water. A region is a group of 1s connected 4-directionally (up/down/left/right).

Return the area of the largest region (the number of 1 cells in it). If there's no land at all, return 0.

Example 1

```
Input:  grid = [[0,0,1,0,0],
                [0,1,1,1,0],
                [0,0,1,0,0],
                [1,1,0,0,1]]
Output: 5
```

Example 2

```
Input:  grid = [[0,0],
                [0,0]]
Output: 0
```

## Solution

We can solve this problem using both BFS and DFS. I will chose DFS here because it lets us search deeper in a path in the graph until the path exhaust and we can bracktrack and try other paths. This will help us count the no of connected lands in a path in a better way.

Here is a high level algorithm

- Initialize rows = len(grid), cols = len(grid[0])
- Initializse visited: List[List[bool]] to false for all rows and cols. This is used to track all visited cells, so that we do not count same cell twice
- Initialize max_area = 0
- Loop over rows, for each row
    - for each col
        - if grid[row][col] == 1
            - area = call_dfs(grid, row, col, rows, cols, visited)
            - max_area = max(area, max_area)
- return max_area

call_dfs(grid, row, col, rows, cols, visited)
    - if row < 0 or row >= rows or col < 0 or col >= cols
        - return 0
    - if visited[row][col] or grid[row][col] == 0
        - return 0
    - visited[row][col] = True
    - return 1 + call_dfs(grid, row + 1, col, rows, cols, visited) + call_dfs(grid, row, col + 1, rows, cols, visited) + call_dfs(grid, row - 1, col, rows, cols, visited) + call_dfs(row, col - 1, rows, cols, visited)

## Time complexity

- Since each cell in the grid is traversed exactly once, and there are rows * cols cells in the grid
T(N) = O(rows * cols)

## Space complexity

- O(rows * cols) for storing visited list and recursing stack as well.
    
