from typing import List

def largest_rect(heights: List[int]) -> int:
    left_min: List[int] = [-1] * len(heights)
    right_min: List[int] = [len(heights)] * len(heights)

    max_area = 0
    stack: List[int] = []

    for index in range(len(heights)):
        while stack and heights[stack[-1]] > heights[index]:
            right_min[stack.pop()] = index

        stack.append(index)

    stack = []

    for index in range(len(heights) - 1, -1, -1):
        while stack and heights[stack[-1]] > heights[index]:
            left_min[stack.pop()] = index

        stack.append(index)

    for index in range(len(heights)):
        area = heights[index] * (right_min[index] - left_min[index] - 1)
        max_area = max(max_area, area)

    return max_area