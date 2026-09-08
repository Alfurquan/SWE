from typing import List, Deque, Tuple
from collections import deque


class ContiguousIsland:
    def largest_island(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])

        visited: List[List[bool]] = [[False for _ in range(cols)] for _ in range(rows)]
        dirs: List[List[int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        max_area = 0
        stack: Deque[Tuple[int, int]] = deque()

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    stack.appendleft((row, col))
                    visited[row][col] = True
                    area = 1

                    while stack:
                        row, col = stack.popleft()

                        for dir in dirs:
                            nrow = row + dir[0]
                            ncol = col + dir[1]

                            if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols:
                                continue

                            if visited[nrow][ncol] or grid[nrow][ncol] == 0:
                                continue

                            stack.appendleft((nrow, ncol))
                            visited[nrow][ncol] = True
                            area += 1
                    
                    max_area = max(area, max_area)

        return max_area
