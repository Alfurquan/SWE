from typing import List

class CombinationSum:
    def get_comn_sum(self, nums: List[int], target: int) -> List[List[int]]:
        if not nums:
            return []

        result: List[List[int]] = []
        self.compute(nums, 0, 0, target, [], result)
        return result

    def compute(self, nums: List[int], index: int, curr_sum: int, target_sum: int, path: List[int], result: List[List[int]]):
        if curr_sum == target_sum:
            result.append(path.copy())
            return

        for i in range(index, len(nums)):
            if curr_sum + nums[i] <= target_sum:
                path.append(nums[i])
                self.compute(nums, i, curr_sum + nums[i], target_sum, path, result)
                path.pop()

# Time complexity = The recurstion depth would be O(T/min(nums)), where T = target sum and each depth can span to n branches so total
# no of nodes would be O(n^d) where d is the depth = T / min(nums)

# Space complexity = O(d), where d is the recursion depth.
