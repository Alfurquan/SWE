# Problem: Number of Ways to Make Change
You're given an array coins of distinct positive integer denominations and an integer amount. Return the number of distinct combinations of coins that sum to amount. You have an unlimited supply of each coin.

Two combinations are different only if the multiset of coins differs — order does not matter. So 1 + 2 and 2 + 1 count as the same combination.

If no combination sums to amount, return 0.

Example 1
```
Input:  coins = [1, 2, 5], amount = 5
Output: 4
```

Example 2
```
Input:  coins = [2], amount = 3
Output: 0
```

## Solution

This is a dynamic programming problem, and I would approach it in the same mechanism.

- Base case

if index == len(coins)
    return 0

if amount == 0:
    return 1  // There is one way to make 0 amount, using no coins

- State

At each step of the algorithm, we need to maintain some state, here the state would be

state(index, amount): Where index = index in coins list, amount = amount left to be made

- Transition

At each step, we do this

total_ways = 0
if coins[index] <= amount:
    // We can either select or not select this coin at index i
    total_ways += solve(index, amount - coins[index]) + solve(index + 1, amount)
else:
    // We need to skip the coin at index i
    total_ways += solve(index + 1, amount)

- Return

We return total_ways

Here is the high level algorithm in recursive way. I am giving recursive implementation here, but while coding, can code iterative way as well.

- Initialize mem: Dict[Tuple[int, int], bool] // To hold answers for memoization
- Call result = solve(coins, 0, amount, mem)
- return result

```
solve(coins, index, amount, mem):
    if index == len(coins):
        return 0

    if amount == 0:
        return 1

    if (index, amount) in mem:
        return mem[(index, amount)]
    
    total_ways = 0

    if coins[index] <= amount:
        total_ways += solve(coins, index, amount - coins[index], mem) + solve(coins, index + 1, amount, mem)
    else:
        total_ways += solve(coins, index + 1, amount, mem)

    mem[(index, amount)] = total_ways
    return total_ways
```

## Time complexity

- We are calling solve n*amount times. Since we are storing the result in mem cache for (index, amount) state, each (index, amount) is computed just once.

So effectively the time complexity is O(n * amount), where n = no of coins, amount = amount

## Space complexity

- O(n*amount) for mem cache and recursion