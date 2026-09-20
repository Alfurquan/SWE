from typing import List, Tuple, Dict

class DiffTool:
    def longest_unchanged_seq_rec(self, old: str, new: str) -> int:
        mem: Dict[Tuple[int, int], int] = {}
        return self.solve(old, new, len(old), len(new), mem)

    def solve(self, old: str, new: str, m: int, n: int, mem: Dict[Tuple[int, int], int]) -> int:
        if m <= 0 or n <= 0:
            return 0

        if (m, n) in mem:
            return mem[(m, n)]

        result = 0
        if old[m - 1] == new[n - 1]:
            result = 1 + self.solve(old, new, m - 1, n - 1, mem)
        else:
            result = max(self.solve(old, new, m, n - 1, mem), self.solve(old, new, m - 1, n, mem))

        mem[(m, n)] = result
        return result

    def longest_unchanged_seq_iter(self, old: str, new: str) -> int:
        dp: List[List[int]] = [[0 for _ in range(len(new) + 1)] for _ in range(len(old) + 1)]

        for i in range(1, len(old) + 1):
            for j in range(1, len(new) + 1):
                if old[i - 1] == new[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[len(old)][len(new)]

