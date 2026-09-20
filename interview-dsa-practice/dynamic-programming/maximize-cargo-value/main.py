from typing import List, Dict, Tuple

class Item:
    def __init__(self, value: int, weight: int):
        self.value = value
        self.weight = weight

class Cargo:
    def max_value_rec(self, weights: List[int], values: List[int], weight: int) -> int:
        items: List[Item] = []

        for i in range(len(values)):
            items.append(Item(values[i], weights[i]))

        mem: Dict[Tuple[int, int], int] = {}
        return self.solve(items, 0, weight, mem)

    def solve(self, items: List[Item], index: int, weight: int, mem: Dict[Tuple[int, int], int]) -> int:
        if index == len(items):
            return 0

        if weight == 0:
            return 0

        if (index, weight) in mem:
            return mem[(index, weight)]

        max_value = 0

        if items[index].weight <= weight:
            max_value = max((items[index].value + self.solve(items, index + 1, weight - items[index].weight, mem)),
                            self.solve(items, index + 1, weight, mem))
        else:
            max_value = self.solve(items, index + 1, weight, mem)

        mem[((index, weight))] = max_value
        return max_value

    def max_value_iter(self, weights: List[int], values: List[int], weight: int) -> int:
        items: List[Item] = []
        
        for i in range(len(values)):
            items.append(Item(values[i], weights[i]))

        dp: List[int] = [0] * (weight + 1)

        for index in range(len(items)):
            for wt in range(weight, items[index].weight - 1, -1):
                dp[wt] = max(dp[wt], items[index].value + dp[wt - items[index].weight])

        return dp[weight]