from typing import List, Deque, Tuple
from collections import deque

class Solution:
    dirs: List[List[int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    def get_max_cooling(self, grid: List[List[int]]) -> List[List[int]]:
        if not grid:
            return []
        
        rows = len(grid)
        cols = len(grid[0])

        queue: Deque[Tuple[int, int, int]] = deque()
        result: List[List[int]] = [[grid[row][col] for col in range(cols)] for _ in range(rows)]
        
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] > 0:
                    queue.append((row, col, grid[row][col]))

        while queue:
            row, col, cooling = queue.popleft()

            for dir in self.dirs:
                nrow = row + dir[0]
                ncol = col + dir[1]

                if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols:
                    continue
                
                if grid[row][col] == 0:
                    if cooling - 1 > result[nrow][ncol]:
                        result[nrow][ncol] = cooling - 1
                        queue.append((nrow, ncol, cooling - 1))

        return result
