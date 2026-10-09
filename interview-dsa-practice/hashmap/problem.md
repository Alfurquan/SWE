# Problem: 

Given an integer array nums (values can be negative, zero, or positive) and an integer k, return the number of contiguous subarrays whose elements sum to exactly k.

Example 1
```
Input:  nums = [1, 1, 1], k = 2
Output: 2
```

Example 2
```
Input:  nums = [1, 2, 3], k = 3
Output: 2
```

## Solution 

I would use a hashmap to solve this problem. I would store the sum and the freq of it. Then as I traverse the array, I would try to find the number of times I have seen sum - k in the dict. Basically we are using prefix sum here.

Here is the high level algorithm for the approach

- Initialize count = 0
- Initialize curr_sum = 0
- Initialize sum_map: Dict[int, int] = {}
- for num in nums:
    curr_sum += num

    if curr_sum == k:
        count += 1

    if (curr_sum - k) in sum_map:
        count += sum_map[curr_sum - k]

    sum_map[curr_sum] = sum_map.get(curr_sum, 0) + 1

- return count

## Time complexity

- O(N) for loop and O(1) for dict operations

## Space complexity

- O(N) for dictionary.
