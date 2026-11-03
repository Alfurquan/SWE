from typing import List

def buildings_with_ocean_view(heights: List[int]) -> List[int]:
    stack: List[int] = []

    for index in range(len(heights)):
        while stack and heights[stack[-1]] <= heights[index]:
            stack.pop()

        stack.append(index)

    return list(stack)