from typing import List, Tuple, Deque
from collections import deque

class DataCenter:
    def min_time_heat_propagation(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])
        dirs: List[List[int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        queue: Deque[Tuple[int, int]] = deque()
        min_time = 0
        num_healthy = 0

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 2:
                    queue.append((row, col))
                elif grid[row][col] == 1:
                    num_healthy += 1

        while queue and num_healthy > 0:
            size = len(queue)
            min_time += 1
            for _ in range(size):
                row, col = queue.popleft()

                for dir in dirs:
                    nrow = row + dir[0]
                    ncol = col + dir[1]

                    if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols:
                        continue

                    if grid[nrow][ncol] == 1:
                        grid[nrow][ncol] = 2
                        queue.append((nrow, ncol))
                        num_healthy -= 1

        return -1 if num_healthy > 0 else min_time