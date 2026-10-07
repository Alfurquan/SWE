# Problem: Dual Watershed Drainage
You're given an m x n grid heights where heights[r][c] is the elevation of a cell. There's an ocean on the top and left edges (the "North Sea") and an ocean on the bottom and right edges (the "South Sea").

Rainwater on a cell can flow to a 4-directionally adjacent cell only if that neighbor's elevation is less than or equal to the current cell's elevation. Water can flow off the edge of the grid into whichever ocean borders that edge.

Return a list of all cells [r, c] from which rainwater can flow to both the North Sea and the South Sea.

Example 1
```
Input: heights = [[1,2,2,3,5],
                  [3,2,3,4,4],
                  [2,4,5,3,1],
                  [6,7,1,4,5],
                  [5,1,1,2,4]]
Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
```

Example 2
```
Input: heights = [[1]]
Output: [[0,0]]
```

## Solution

I would model this problem as a graph where each cell in the grid represents a vertex and the cells are connected to 4-directionally adjacent cells via edges.

Now instead of starting from each cell and checking if the water can flow till the oceans which would be costly and slow - O((m*n)^2), I would invert it and start traversing from both the oceans and cover all the cells to which water can flow from the oceans. Once I have both the list, I would check cells which are common and return them as the result.

Here is a high level algorithm for the approach

- Initialize row = len(grid), cols = len(grid[0])
- Initilaize dirs: List[List[int]] = [[-1, 0], [0, 1], [0, -1], [1, 0]] for four bi directionally connected cells
- Initialize result: List[List[int]] = []
- Initialize north_sea_cells: Set[Tuple[int, int]] = set(), south_sea_cells: Set[Tuple[int, int]] = set()
- for each row in rows
    - traverse(grid, row, 0, north_sea_cells, rows, cols, dirs)

- for each col in cols:
    - traverse(grid, 0, col, north_sea_cells, rows, cols, dirs)

- for each row in rows
    - traverse(grid, row, cols - 1, south_sea_cells, rows, cols, dirs)

- for each col in cols:
    - traverse(grid, rows - 1, col, south_sea_cells, rows, cols, dirs)

- for row in rows
    - for col in cols
        - if (row, col) in south_sea_cells and (row, col) in north_sea_cells:
            result.append([row, col])

return result

Below is the traverse method

```
traverse(grid, row, col, visited_cells, rows, cols, dirs):
    visited_cells.add((row, col))

    for dir in dirs:
        nrow = row + dir[0]
        ncol = col + dir[1]

        if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols or (nrow, ncol) in visited_cells:
            continue
        
        if grid[nrow][ncol] >= grid[row][col]:
            traverse(grid, nrow, ncol, visited_cells, rows, cols, dirs)
```

## Time complexity

- Since we traverse each cell in the grid exactly once, the time complexity is O(m * n), where m = no of rows, n = no of cols

## Space complexity

- O(m * n) for visited cell tracking and result storing.


