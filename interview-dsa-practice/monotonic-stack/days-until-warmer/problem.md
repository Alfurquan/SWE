# Problem: Days Until Warmer
You're building a weather feature. Given a list temperatures where temperatures[i] is the temperature on day i, return an array answer where answer[i] is the number of days you have to wait after day i to get a warmer temperature. If no future day is warmer, answer[i] = 0.

Example 1

```
Input:  temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
Output: [1, 1, 4, 2, 1, 1, 0, 0]
```

Example 2

```
Input:  temperatures = [30, 20, 10]
Output: [0, 0, 0]
```

## Solution

I would be using a monotonic stack to solve this problem where I would be storing the index of the list as I keep traversing it from left to right. As I find temperatures greater than top of stack one, I pop top of stack and compute the index difference between them to be the result for top of stack index. Monotonic stack helps here as it helps in popping elements in O(1) as soon as we find a temperature greater than it.

Here is the algorithm for the approach

- Initialize result = [0] * len(temperatures)
- Initialize stack: Deque[int] = deque()
- for index in range(len(temperature)):
    - while stack and temperatures[stack[0]] < temperatures[index]:
        indx = stack.popleft()
        result[indx] = index - indx
    - stack.appendleft(index)
- return result

## Time complexity

- The loop runs over all items in the list, so its O(N), now each item is pushed and popped exactly once from the stack, so the amortized time complexity here is O(N), where N = no of items in the temperatures list

## Space complexity

- O(N) for stack and results list.