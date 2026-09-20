# Problem: Minimum Walls to Remove
You're given an m x n grid where each cell is 0 (open) or 1 (a wall). You start at the top-left (0, 0) and want to reach the bottom-right (m-1, n-1), moving 4-directionally.

Moving into an open cell (0) costs 0.
Moving into a wall cell (1) costs 1 (you remove that wall).
Return the minimum number of walls you must remove to reach the destination.

Note: (0,0) and (m-1, n-1) are always 0, and you can always reach the destination by removing enough walls — so the answer always exists (no -1 case).

Example 1
```
Input:  grid = [[0,1,1],
                [1,1,0],
                [1,1,0]]
Output: 2
```

Example 2
```
Input:  grid = [[0,0,0],
                [0,1,0],
                [0,0,0]]
Output: 0
```

## Solution

This is a shortest path problem as we need to find the minimum no of walls to remove to reach the destination. We can use dijkstra algorithm here to solve it, with the grid modelled as a graph and path between two cells being the edge with weight 0 or 1. But here's the caveat, Dijsktra algorithm will gives a time complexity of O(ElogV), Where E = No of edges and V = no of cells in the grid. 

We can do better than this by using a modified version of BFS called 0-1 BFS which would help in solving the caveat that Dijkstra has. The plain BFS helps in finding shortest path in unweighted or 0 weighted graphs, but here since we can have weights as 0 or 1, we need 0-1 BFS, where we use a deque so that we can push cells both from front and back to it. The idea of 0-1 BFS is simple, always push edges with weight 1 from the back and edges with weight 0 from the front and we always pop from the front of the deque so that we explore edges with weight 0 first to minimize the cost.

Here is the high level algorithm

- Initialize, rows = len(grid), cols = len(grid[0])
- Initialize dirs: List[List[int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]
- Initalize a queue: Deque[Tuple[int, int, int]] = deque() // To hold row, col, cost
- Initialize a visited: Set[Tuple[int, int]] = set() // To track visited paths
- If grid[0][0] == 1
    - push (0, 0, 1) to the queue
- else
    - push (0, 0, 0) to the queue
- add (0,0) to visited
- while queue
    - pop row, col, cost from the queue front
    - if row == rows - 1 and col == cols - 1
        - return cost
    - for dir in dirs
        - nrow = row + dir[0]
        - ncol = col + dir[1]
        - if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols or visited[nrow][ncol]
            - continue
        - if grid[nrow][ncol] == 1
            - push (nrow, ncol, cost + 1) to back of queue
        - else
            - push (nrow, ncol, cost) to front of queue
        - add (nrow, ncol) to visited
- return 0

## Time complexity

- Since we visit each cell exactly once, time complexity would be O(rows * cols)

## Space complexity

- O(rows * cols) for queue and visited set
