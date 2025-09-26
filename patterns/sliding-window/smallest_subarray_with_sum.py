# Given an array of positive numbers and a positive number ‘S’, 
# find the length of the smallest contiguous subarray 
# whose sum is greater than or equal to ‘S’.
# Return 0, if no such subarray exists.

from typing import List
import sys

def smallest_sum_subarray(nums: List[int], s: int) -> int:
    wstart = 0
    min_length = sys.maxsize
    wsum = 0
    
    for wend in range(len(nums)):
        wsum += nums[wend]
        while wsum >= s:
            min_length = min(min_length, wend - wstart + 1)
            wsum -= nums[wstart]
            wstart += 1
            
    return 0 if min_length == sys.maxsize else min_length

print(smallest_sum_subarray([2, 1, 5, 2, 3, 2], 7))
print(smallest_sum_subarray([2, 1, 5, 2, 8], 7))
print(smallest_sum_subarray([3, 4, 1, 1, 6], 8))