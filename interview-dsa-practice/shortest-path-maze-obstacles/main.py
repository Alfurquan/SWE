from typing import List, Tuple, Set, Deque
from collections import deque

class MazeSolver:
    def shortest_path(self, grid: List[List[int]], k: int) -> int:
        rows = len(grid)
        cols = len(grid[0])

        if grid[0][0] == 1:
            k -= 1
        
        visited: Set[Tuple[int, int, int]] = set()
        queue: Deque[Tuple[int, int, int, int]] = deque()
        dirs: List[List[int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        queue.append((0, 0, 0, k))
        visited.add((0, 0, k))

        while queue:
            row, col, dist, obstacles = queue.popleft()

            if row == rows - 1 and col == cols - 1:
                return dist

            for dir in dirs:
                nrow = row + dir[0]
                ncol = col + dir[1]
                obs = obstacles

                if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols:
                    continue

                if grid[nrow][ncol] == 0 and obs >= 0 and (nrow, ncol, obs) not in visited:
                    queue.append((nrow, ncol, dist + 1, obs))
                    visited.add((nrow, ncol, obs))
                elif grid[nrow][ncol] == 1 and obs - 1 >= 0 and (nrow, ncol, obs - 1) not in visited:
                    queue.append((nrow, ncol, dist + 1, obs - 1))
                    visited.add((nrow, ncol, obs - 1))
        return -1