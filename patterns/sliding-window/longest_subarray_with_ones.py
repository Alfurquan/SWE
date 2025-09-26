# Given an array containing 0s and 1s, 
# if you are allowed to replace no more than ‘k’ 0s with 1s, 
# find the length of the longest contiguous subarray having all 1s.

from typing import List

def max_length_subarray_with_ones(nums: List[int], k: int) -> int:
    wstart = 0
    zero_count = 0
    max_length = 0
    
    for wend in range(len(nums)):
        if nums[wend] == 0:
            zero_count += 1
            
        while zero_count > k:
            if nums[wstart] == 0:
                zero_count -= 1
            
            wstart += 1
        
        max_length = max(max_length, wend - wstart + 1)
    
    return max_length

print(max_length_subarray_with_ones([0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1], 2))
print(max_length_subarray_with_ones([0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1], 3))