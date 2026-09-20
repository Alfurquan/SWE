from typing import List, Dict, Tuple

class Delivery:
    def cheapest_route_rec(self, grid: List[List[int]]) -> int:
        mem: Dict[Tuple[int, int], int] = {}
        return self.solve(grid, 0, 0, len(grid), len(grid[0]), mem)

    def solve(self, grid: List[List[int]], row: int, col: int, rows: int, cols: int, mem: Dict[Tuple[int, int], int]) -> int:
        if row == rows - 1 and col == cols - 1:
            return grid[row][col]

        if row >= rows or col >= cols:
            return float('inf')

        if (row, col) in mem:
            return mem[(row, col)]

        mem[(row, col)] = grid[row][col] + min(self.solve(grid, row + 1, col, rows, cols, mem), self.solve(grid, row, col + 1, rows, cols, mem))

        return mem[(row, col)]

    def cheapest_route_iter(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])

        dp: List[List[int]] = [[0 for _ in range(cols)] for _ in range(rows)]

        dp[0][0] = grid[0][0]

        for row in range(1, rows):
            dp[row][0] = dp[row - 1][0] + grid[row][0]

        for col in range(1, cols):
            dp[0][col] = dp[0][col - 1] + grid[0][col]

        for row in range(1, rows):
            for col in range(1, cols):
                dp[row][col] = grid[row][col] + min(dp[row - 1][col], dp[row][col - 1])

        return dp[rows - 1][cols - 1]