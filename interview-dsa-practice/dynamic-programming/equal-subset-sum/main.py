from typing import List, Tuple, Dict

class SubsetSum:
    def is_possible_rec(self, nums: List[int]) -> bool:
        total_sum = sum(nums)

        if total_sum % 2 != 0:
            return False

        mem: Dict[Tuple[int, int], bool] = {}

        return self.solve(nums, 0, total_sum // 2, mem)

    def solve(self, nums: List[int], index: int, sum: int, mem: Dict[Tuple[int, int], bool]) -> bool:
        if sum == 0:
            return True

        if index == len(nums):
            return False

        if (index, sum) in mem:
            return mem[(index, sum)]

        result = False

        if nums[index] <= sum:
            result = self.solve(nums, index + 1, sum - nums[index], mem) or self.solve(nums, index + 1, sum, mem)
        else:
            result = self.solve(nums, index + 1, sum, mem)

        mem[(index, sum)] = result
        return result

    def is_possible_iter(self, nums: List[int]) -> bool:
        total_sum = sum(nums)
        
        if total_sum % 2 != 0:
            return False

        target = total_sum // 2

        dp: List[bool] = [False] * (target + 1)
        dp[0] = True

        for num in nums:
            for curr_sum in range(target, num - 1, -1):
               dp[curr_sum] = dp[curr_sum] or dp[curr_sum - num]

        return dp[target]