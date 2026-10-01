from typing import List, Tuple, Dict

class DeliveryRoutes:
    def num_safe_routes_rec(self, grid: List[List[int]]) -> int:
        mem: Dict[Tuple[int, int], int] = {}
        return self.solve(grid, 0, 0, len(grid), len(grid[0]), mem)

    def solve(self, grid: List[List[int]], row: int, col: int, rows: int, cols: int, mem: Dict[Tuple[int, int], int]) -> int:
        if row >= rows or col >= cols:
            return 0

        if grid[row][col] == 1:
            return 0

        if row == rows - 1 and col == cols - 1:
            return 1

        if (row, col) in mem:
            return mem[(row, col)]

        mem[(row, col)] = self.solve(grid, row + 1, col, rows, cols, mem) + self.solve(grid, row, col + 1, rows, cols, mem)

        return mem[(row, col)]

    def num_safe_routes_iter(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])

        dp: List[List[int]] = [[0 for _ in range(cols)] for _ in range(rows)]

        if grid[0][0] != 1:
            dp[0][0] = 1

        for row in range(1, rows):
            if grid[row][0] == 1:
                dp[row][0] = 0
            else:
                dp[row][0] = dp[row - 1][0]

        for col in range(1, cols):
            if grid[0][col] == 1:
                dp[0][col] = 0
            else:
                dp[0][col] = dp[0][col - 1]

        for row in range(1, rows):
            for col in range(1, cols):
                if grid[row][col] == 1:
                    dp[row][col] = 0
                else:
                    dp[row][col] = dp[row - 1][col] + dp[row][col - 1] 

        return dp[rows - 1][cols - 1]