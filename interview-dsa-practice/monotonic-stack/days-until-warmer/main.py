from typing import List, Deque
from collections import deque

class DaysWarmer:
    def get_results(self, temperatures: List[int]) -> List[int]:
        result: List[int] = [0] * len(temperatures)
        stack: Deque[int] = deque()

        for index in range(len(temperatures)):
            while stack and temperatures[stack[0]] < temperatures[index]:
                indx = stack.popleft()
                result[indx] = index - indx

            stack.appendleft(index)

        return result