# Problem: Partition Into Two Equal Halves
You're given an array nums of positive integers. Return True if you can split the array into two subsets whose sums are equal, otherwise False. Every element must go into exactly one of the two subsets.

Example 1
```
Input:  nums = [1, 5, 11, 5]
Output: True
```

Example 2
```
Input:  nums = [1, 2, 3, 5]
Output: False
```

## Solution

This is a dynamic programming problem where we need to split the array into two subsets whose sums are equal. Actually this problem boils down to finding a subset whose sum is sum / 2 where sum = total sum of all the elements of the array. If sum % 2 is not equal to zero (sum is odd), then this is not event possible and we return false

Here is how I would layout and approach this problem

- Base case

sum == 0
    return True

index == len(nums)
    return False

- State

state(index, sum) : Represents the index in the nums array where we are and the sum to form

- Transition

At each step we do this

if nums[index] <= sum:
    return solve(nums, index + 1, sum - nums[index]) or solve(nums, index + 1, sum) // Take or skip num at index

Here is the algorithm for the approach

- Initialize mem: Dict[Tuple[int, int], bool] // mem cache to hold results
- calculate total_sum = sum(nums)
- if total_sum % 2 != 0
    - return False
- return solve(nums, 0, sum / 2, mem)

```
solve(nums, index, sum, mem)    
    if sum == 0:
        return True

    if index == len(nums):
        return False

    if (index, sum) in mem:
        return mem[(index, sum)]
    
    result = False

    if nums[index] <= sum:
        result = solve(nums, index + 1, sum - nums[index]) or solve(nums, index + 1, sum)
    else:
    result = solve(nums, index + 1, sum)
    
    mem[(index, sum)] = result
    return result
```

## Time complexity

- Since we compute each index,sum exactly once, time complexity here would O(n * sum), where n = total no of elements in nums and sum is the total sum of elements / 2

## Space complexity

- O(n * sum) for storing mem cache.
