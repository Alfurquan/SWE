from typing import List, Dict
import sys

class CoinChange:
    def min_coin_change_rec(self, coins: List[int], amount: int) -> int:
        mem: Dict[int, int] = {}
        result = self.solve(coins, amount, mem)
        return -1 if result == sys.maxsize else result

    def solve(self, coins: List[int], amount: int, mem: Dict[int, int]) -> int:
        if amount == 0:
            return 0

        if amount in mem:
            return mem[amount]

        min_coins = sys.maxsize
        for coin in coins:
            if coin <= amount:
                result = self.solve(coins, amount - coin, mem)
                if result != sys.maxsize:
                    min_coins = min(min_coins, 1 + result)

        mem[amount] = min_coins
        return min_coins

    def min_coin_change_iter(self, coins: List[int], amount: int) -> int:
        dp: List[int] = [sys.maxsize for _ in range(0, amount + 1)]

        dp[0] = 0

        for i in range(1, amount + 1):
            for j in range(len(coins)):
                if coins[j] <= i:
                    dp[i] = min(dp[i], 1 + dp[i - coins[j]])

        return -1 if dp[amount] == sys.maxsize else dp[amount]
    