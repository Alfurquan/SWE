from typing import List, Tuple, Deque, Set
from collections import deque

class MinimumWalks:
    def get_min_walks(self, grid: List[List[int]]) -> int:
        queue: Deque[Tuple[int, int, int]] = deque()
        visited: Set[Tuple[int, int]] = set()
        directions: List[List[int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        rows = len(grid)
        cols = len(grid[0])

        if grid[0][0] == 1:
            queue.append((0, 0, 1))
        else:
            queue.appendleft((0, 0, 0))

        visited.add((0, 0))

        while queue:
            row, col, cost = queue.popleft()

            if row == rows - 1 and col == cols - 1:
                return cost

            for direction in directions:
                nrow = row + direction[0]
                ncol = col + direction[1]

                if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols or (nrow, ncol) in visited:
                    continue

                if grid[nrow][ncol] == 1:
                    queue.append((nrow, ncol, cost + 1))
                else:
                    queue.appendleft((nrow, ncol, cost))

                visited.add((nrow, ncol))

        return 0