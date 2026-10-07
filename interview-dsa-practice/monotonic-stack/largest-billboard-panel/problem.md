# Problem: Largest Billboard Panel
You're installing a rectangular billboard against a row of buildings of varying heights. Given an array heights where heights[i] is the height of the i-th building (all buildings have width 1 and sit side by side), find the area of the largest rectangle that fits entirely within the building silhouette.

Formally: find the largest rectangle that can be formed using contiguous bars, where the rectangle's height is limited by the shortest bar it spans.

Example 1
```
Input:  heights = [2, 1, 5, 6, 2, 3]
Output: 10
```

Example 2
```
Input:  heights = [2, 4]
Output: 4
```

Example 3
```
Input:  heights = [1, 1, 1, 1]
Output: 4
```

## Solution

I would use a monotonic stack pattern to approach and solve this problem. Sorry I cannot think of a single pass solution now, so I would go ahead and do the double pass approach for now.

We would use the monotonic stack to find the previous shorter and next shorter bars for each bar in two passes.

Here is the high level algorithm for the approach

- Initialize max_area = 0
- Initialize left_min_index: List[int] = [-1] * len(heights) //index of leftmost shortest bar for each bar
- Initialize right_min_index: List[int] = [len(heights)] * len(heights) //index of rightmost shortes bar for each bar
- Initialize stack: Deque[int] = deque()
- for each index in range(len(heights)):
    while stack and heights[index] < heights[stack[0]]:
        indx = stack.popleft()
        right_min_index[indx] = index

    stack.appendleft(index)
- stack = deque()
- for each index in range(len(heights) - 1, -1, -1):
    while stack and heights[index] < heights[stack[0]]:
        indx = stack.popleft()
        left_min_index[indx] = index

- for index in range(len(heights)):
    left_min = left_min_index[index]
    right_min = right_min_index[index]
    
    area = heights[index] * (right_min - left_min - 1)
    max_area = max(max_area, area)

return max_area

## Time complexity

- O(N), where N = no of items in heights array

## Space complexity

- O(N) for stack, left_min and right_min arrays
