# Sliding window pattern

In many problems dealing with an array (or a LinkedList), we are asked to find or calculate something among all the contiguous subarrays (or sublists) of a given size. For example, take a look at this problem:

```shell
Given an array, find the average of all contiguous subarrays of size ‘K’ in it.
```

A brute-force algorithm will be to calculate the sum of every 5-element contiguous subarray of the given array and divide the sum by ‘5’ to find the average.

The inefficiency is that for any two consecutive subarrays of size ‘5’, the overlapping part (which will contain four elements) will be evaluated twice.

The efficient way to solve this problem would be to visualize each contiguous subarray as a sliding window of ‘5’ elements. This means that when we move on to the next subarray, we will slide the window by one element. So, to reuse the sum from the previous subarray, we will subtract the element going out of the window and add the element now being included in the sliding window. This will save us from going through the whole subarray to find the sum and, as a result, the algorithm complexity will reduce to O(N)

```python
def calculate_average(nums: List[int], k: int) -> List[int]:
    if k > len(nums) or k <= 0:
        return []

    result: List[int] = []
    wstart: int = 0
    wsum: int = 0

    for wend in range(len(nums)):
        wsum += nums[wend]

        if wend >= k - 1:
            result.append(wsum / k)
            wsum -= nums[wstart]
            wstart += 1

    return result
```

