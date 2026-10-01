# Problem: Counting Safe Delivery Routes
The delivery drone is back on the m x n city grid, starting at top-left (0,0), reaching bottom-right (m-1, n-1), moving only right or down.

But now some cells contain no-fly zones (obstacles). The grid holds:

- 0 — a cell the drone can fly over,
- 1 — a no-fly zone (blocked; the drone cannot enter it).

Return the number of distinct routes from top-left to bottom-right that avoid all no-fly zones. If the start or end cell is itself blocked, there are 0 routes.

Example 1
```
Input:  grid = [[0, 0, 0],
                [0, 1, 0],
                [0, 0, 0]]
Output: 2
```

Example 2
```
Input:  grid = [[0, 1],
                [0, 0]]
Output: 1
```

## Solution

This is a dynamic programming problem where we need to return the number of distinct routes from top-left to bottom-right that avoid all no fly zones.

It satisfies both the constraints of a dynamic programming problem - 

- Optimal substructure: The answer to the whole problem can be derived from smaller subproblems. Here the num of distinct routes to each bottom-right from top-left can be derived from the num of distinct ways to reach a cell (x,y) from top-left and no of distinct ways to reach bottom-right from cell (x,y).

- Overlapping subproblems: The subproblems are overlapping as the same cell (x,y) can be on different paths in the route from top left to bottom right.

Here is the high level algorithm

- Initialize mem: Dict[Tuple[int, int], int] = {}  //mem cache
- return solve(grid, 0, 0, len(grid), len(grid[0]), mem)

```
solve(grid, row, col, rows, cols, mem):
    if row >= rows or col >= cols:
        return 0

    if grid[row][col] == 1:
        return 0

    if row == rows - 1 and col == cols - 1:
        return 1
    
    if (row, col) in mem:
        return mem[(row, col)]

    mem[(row, col)] = solve(grid, row, col + 1, rows, cols, mem) + solve(grid, row + 1, col, rows, cols, mem)

    return mem[(row, col)]
```

## Time complexity

- Since each (row, col) is computed exactly once, time complexity here is O(m * n), where m = no of rows and n = no of cols

## Space complexity

- O(m * n) for mem cache