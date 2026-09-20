from typing import List, Dict, Tuple

class CoinChange:
    def num_ways_rec(self, coins: List[int], amount: int) -> int:
        mem: Dict[Tuple[int, int], int] = {}
        return self.solve(coins, 0, amount, mem)

    def solve(self, coins: List[int], index: int, amount: int, mem: Dict[Tuple[int, int], int]) -> int:
        if index == len(coins):
            return 0

        if amount == 0:
            return 1

        if (index, amount) in mem:
            return mem[(index, amount)]

        total_ways = 0

        if coins[index] <= amount:
            total_ways += self.solve(coins, index, amount - coins[index], mem) + self.solve(coins, index + 1, amount, mem)
        else:
            total_ways += self.solve(coins, index + 1, amount, mem)

        mem[((index, amount))] = total_ways
        return total_ways

    def num_ways_iter(self, coins: List[int], amount: int) -> int:
        dp: List[List[int]] = [[0 for _ in range(amount + 1)] for _ in range(len(coins) + 1)]

        for i in range(1, amount + 1):
            dp[0][i] = 0

        for i in range(1, len(coins) + 1):
            dp[i][0] = 1

        dp[0][0] = 1

        for i in range(1, len(coins) + 1):
            for j in range(1, amount + 1):
                if coins[i - 1] <= j:
                    dp[i][j] += dp[i][j - coins[i - 1]] + dp[i - 1][j]
                else:
                    dp[i][j] = dp[i - 1][j]

        return dp[len(coins)][amount]