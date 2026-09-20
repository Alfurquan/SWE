from typing import List, Tuple, Dict

class AutoCorrect:
    def min_moves_rec(self, typed_word: str, dict_word: str) -> int:
        mem: Dict[Tuple[int, int], int] = {}
        return self.solve(typed_word, dict_word, len(typed_word), len(dict_word), mem)

    def solve(self, typed_word: str, dict_word: str, m: int, n: int, mem: Dict[Tuple[int, int], int]) -> int:
        if m == 0 and n == 0:
            return 0

        if m == 0:
            return n

        if n == 0:
            return m

        if (m,n) in mem:
            return mem[(m, n)]

        if typed_word[m - 1] == dict_word[n - 1]:
            mem[(m,n)]  = self.solve(typed_word, dict_word, m - 1, n - 1, mem)
        else:
            mem[(m, n)] = 1 + min(min(
                self.solve(typed_word, dict_word, m - 1, n, mem),
                self.solve(typed_word, dict_word, m, n - 1, mem)
            ),
            self.solve(typed_word, dict_word, m - 1, n - 1, mem)
            )

        return mem[(m, n)]

    def min_moves_iter(self, typed_word: str, dict_word: str) -> int:
        m = len(typed_word)
        n = len(dict_word)

        dp: List[List[int]] = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

        for i in range(1, n + 1):
            dp[0][i] = i

        for j in range(1, m + 1):
            dp[j][0] = j

        dp[0][0] = 0

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if typed_word[i - 1] == dict_word[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(min(
                        dp[i - 1][j], dp[i][j - 1]
                    ),
                    dp[i - 1][j - 1]
                    )

        return dp[m][n]