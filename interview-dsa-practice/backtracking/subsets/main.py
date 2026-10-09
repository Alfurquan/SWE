from typing import List

class Subsets:
    def get_all_subsets(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []
        self.compute(nums, 0, [], result)
        return result

    def compute(self, nums: List[int], index: int, path: List[int], result: List[List[int]]):
        result.append(path.copy())

        for i in range(index, len(nums)):
            path.append(nums[i])
            self.compute(nums, i + 1, path, result)
            path.pop()

# Time complexity = O(2^n), for a list with n elements there are 2^n subsets and we gather all of them
# Space complexity = O(2^n) for storing the results
