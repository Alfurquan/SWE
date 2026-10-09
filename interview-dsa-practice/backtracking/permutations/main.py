from typing import List

class Permutations:
    def get_all_permutations(self, nums: List[int]) -> List[List[int]]:
        if not nums:
            return []

        used: List[bool] = [False for _ in range(len(nums))]
        result: List[List[int]] = []

        self.compute(nums, used, [], result)
        return result

    def compute(self, nums: List[int], used: List[bool], path: List[int], result: List[List[int]]):
        if len(path) == len(nums):
            result.append(path.copy())
            return

        for index in range(len(nums)):
            if not used[index]:
                path.append(nums[index])
                used[index] = True
                self.compute(nums, used, path, result)
                path.pop()
                used[index] = False

# Time complexity = O(n!), for a list with n elements there are n! permutations
# Space complexity = O(n!) for storing all the permutations for n elements.

