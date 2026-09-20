# Problem: Maximize Cargo Value
You're loading a delivery truck with a weight capacity of W. There are n packages; package i has weight weights[i] and value values[i]. Each package can be taken at most once (you either load it or leave it).

Return the maximum total value you can carry without exceeding the weight capacity W.

Example 1
```
Input:  weights = [1, 3, 4, 5], values = [1, 4, 5, 7], W = 7
Output: 9
```

Example 2
```
Input:  weights = [5], values = [10], W = 3
Output: 0
```

## Solution

This is a dynamic programming problem and can be solved using 0/1 knapsack algorithm. Here as well at each step we can either take a package or skip it.

Let us represent each item using a class `Item`

class Item:
    value: int
    weight: int

- Base case

if index == len(items):
    return 0

if W == 0:
    return 0

- State

state(index, weight): where index represent the index of the current item and weight represent the current weight

- Transition

At each step, we can either pick or skip an item and each item can be taken at most once, so

if items[index].weight <= weight:
    max_value = max((items[index].value + solve(items, index + 1, weight - items[index])), solve(items, index + 1, weight))
else:
    max_value = solve(items, index + 1, weight)

Here is the high level algorithm for the approach

- Initialize mem: Dict[Tuple[int, int], int] = {} // mem cache
- Form items: List[Item] from weights and values list
- return solve(items, 0, weight, mem)

```
solve(items, index, weight, mem):
    if index == len(items):
        return 0

    if weight == 0:
        return 0

    if (index, weight) in mem:
        return mem[(index, weight)]

    max_value = 0
    if items[index].weight <= weight:
        max_value = max((items[index].value + solve(items, index + 1, weight - items[index].weight, mem)), solve(items, index + 1, weight, mem))
    else:
        max_value = solve(items, index + 1, weight, mem)

    mem[(index, weight)] = max_value
    return max_value
```

## Time complexity

- O(N*Weight), where N = no of items, Weight = weight of cargo. Each item and weight combination is computed just once.

## Space complexity

- O(N*Weight) for mem dict.