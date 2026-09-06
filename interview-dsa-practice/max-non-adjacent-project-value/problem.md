# Maximum Non-Adjacent Project Value
You're a program manager choosing which projects to greenlight this quarter. You're given an array values where values[i] is the profit (which can be negative — some projects lose money) of project i. The projects are laid out in a line.

Company policy: you cannot greenlight two adjacent projects (indices i and i+1 can't both be chosen), because they'd compete for the same resources.

Choose any subset of non-adjacent projects to maximize total profit. You may also choose no projects at all (profit 0).

Return the maximum total profit achievable.

Example 1

```
Input:  values = [3, 2, 7, 10]
Output: 13
```

Example 2

```
Input:  values = [5, 1, 1, 5]
Output: 10
```

Example 3

```
Input:  values = [-2, -3, -1, -5]
Output: 0
```

## Solution

This problem is a dp problem as we maintain a state, at each step we need to determine something based on state from previous step and the overall goal is to optimize something (max/min) or count something. Here we need to maximize the total profit achievable.

Here the dp state is the maximum profit achievable at that state considering previous states.

Recurrance relation would be 

max_profit[i] = max(max_profit[i - 1], max_profit[i - 2] + values[i])

Base case would be

max_profit[0] = values[0]
max_profit[1] = max(values[0], values[1])

Also if all values are negative, then we return 0 as no profit achievable.

Here is the algorithm at a high level

- Initialize max_profit = [0] * (n), n = len(values)
- count_neg = 0
- for profit in values
    if profit < 0
        - count_neg +=1
- if n == 0 or count_neg == n
    - return 0
- max_profit[0] = values[0]
- max_profit[1] = max(values[0], values[1])
- for index in range(2, n)
    - max_profit[index] = max(max_profit[index - 1], max_profit[index - 2] + values[index])
- return max_profit[n - 1]

## Time complexity

- O(N), for looping over all elements

## Space complexity

- O(N) for holding max_profit at all index
