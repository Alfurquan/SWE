from typing import List, Set, Tuple, Deque
from collections import deque

class DualWaterShedDrainage:
    def get_all_cells(self, grid: List[List[int]]) -> List[List[int]]:
        rows = len(grid)
        cols = len(grid[0])

        directions: List[List[int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        north_sea_cells: Set[Tuple[int, int]] = set()
        south_sea_cells: Set[Tuple[int, int]] = set()
        result: List[List[int]] = []
        

        for row in range(rows):
            self._traverse_iter(grid, row, 0, rows, cols, directions, north_sea_cells)

        for col in range(cols):
            self._traverse_iter(grid, 0, col, rows, cols, directions, north_sea_cells)

        for row in range(rows):
            self._traverse_iter(grid, row, cols - 1, rows, cols, directions, south_sea_cells)
        
        for col in range(cols):
            self._traverse_iter(grid, rows - 1, col, rows, cols, directions, south_sea_cells)

        for row in range(rows):
            for col in range(cols):
                if (row, col) in north_sea_cells and (row, col) in south_sea_cells:
                    result.append([row, col])

        return result


    def _traverse_iter(self, grid: List[List[int]], row: int, col: int, rows: int, cols: int, directions: List[List[int]], visited_cells: Set[Set[Tuple[int, int]]]):
        stack: Deque[Tuple[int, int]] = deque()
        stack.append((row, col))
        
        while stack:
            popped_row, popped_col = stack.popleft()
            visited_cells.add((popped_row, popped_col))
            
            for direction in directions:
                nrow = popped_row + direction[0]
                ncol = popped_col + direction[1]
                
                if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols or (nrow, ncol) in visited_cells:
                    continue
                
                if grid[nrow][ncol] >= grid[popped_row][popped_col]:
                    stack.appendleft((nrow, ncol))

