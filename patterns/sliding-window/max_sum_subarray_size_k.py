# Given an array of positive numbers and a positive number ‘k’, 
# find the maximum sum of any contiguous subarray of size ‘k’.

from typing import List


def maximum_sum_subarray(nums: List[int], k: int) -> int:
    max_sum = 0
    if k > len(nums) or k <= 0:
        return 0
    
    wsum = 0
    wstart = 0
    
    for wend in range(len(nums)):
        wsum += nums[wend]
        if wend >= k - 1:
            max_sum = max(max_sum, wsum)
            wsum -= nums[wstart]
            wstart += 1
    
    return max_sum


print(maximum_sum_subarray([2, 1, 5, 1, 3, 2], 3))
print(maximum_sum_subarray([2, 3, 4, 1, 5], 100))

# Analysis
# TC - O(N): N: length of the array
# SC - O(1)