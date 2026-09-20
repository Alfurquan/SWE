# Problem: Cheapest Delivery Route
A delivery drone flies over a city represented as an m x n grid. Each cell grid[i][j] holds the energy cost to fly over that cell. The drone starts at the top-left (0, 0) and must reach the bottom-right (m-1, n-1).

The drone can only move right or down at each step (it always makes forward progress toward the destination).

Return the minimum total energy cost of a path from top-left to bottom-right (summing the cost of every cell visited, including start and end).

Example 1
```
Input:  grid = [[1, 3, 1],
                [1, 5, 1],
                [4, 2, 1]]
Output: 7
```

Example 2
```
Input:  grid = [[1, 2, 3],
                [4, 5, 6]]
Output: 12
```

## Solution

This is a dynamic programming problem, where we need to find the minimum total energy for a drone to reach bottom right from top-left.

It satisfies the two constraints for a dynamic programming problem

- Optimal substructure: The final answer (Min energy cost) of path from top-left to bottom right can be derived from smaller subproblems. That is, min energy cost from path A -> B is derived from min energy cost from path A -> C and C -> B.

- Overlapping subproblems: There are many subproblems which will overlap as the drone can visit the same cell multiple times from different cells, so the computations involving that cell would be done multiple times and would overlap.

Here is how I will approach this problem

- Base case

if row == m - 1 and col == n - 1:
    return grid[row][col]

- State

At each step we maintain the cell (row, col) we are at

- Transition

At each step we can either go right or dowm

min_cost = grid[row][col] + min(solve(grid, row + 1, col), solve(grid, row, col + 1))

Here is the high level algorithm for the approach

- Initialize mem: Dict[Tuple[int, int], int] = {} // mem cache
- return solve(grid, 0, 0, len(grid), len(grid[0]), mem)

```
solve(grid, row, col, m, n, mem)

if row == m - 1 and col == n - 1:
    return grid[row][col]

if row >= m or col >= n:
    return max_value

if (row, col) in mem:
    return mem[(row, col)]

mem[(row, col)] = grid[row][col] + min(solve(grid, row + 1, col, mem), solve(grid, row, col + 1, mem))

return mem[(row, col)]
```

## Time complexity

- Since each (row, col) is computed exactly once, the time complexity = O(m * n), where m = no of rows, n = no of cols

## Space complexity

- O(m * n) for mem cache