# Problem: Minimum Coins to Make Change
You're given an array coins of distinct positive integer denominations and an integer amount. Return the minimum number of coins needed to make up amount. You have an unlimited supply of each coin.

If the amount cannot be made with any combination of the coins, return -1.

Example 1
```
Input:  coins = [1, 2, 5], amount = 11
Output: 3
```

Example 2

```
Input:  coins = [2], amount = 3
Output: -1
```

## Solution

This is a dynamic programming problem. We need to minimize the no of coins to make up the amount. Also we can select a coin of a given denomination unlimited times.

Here is how I will approach this problem.

- First I will define the base case

base case

if amount == 0:
    return 0

- Next up, I will define the state represented in the problem

state[x] = min no of coins to make amount x

- Transition

At each state (coins, x), where coins = list of coins, x = amount
    - Loop over coin in coins
    - if coin <= amount
        - result = solve(coins, x - coin, mem)
        - min_coins = min(min_coins, 1 + result)

Here is the high level algorithm for the approach

- Initialize mem: Dict[int, int] = {}
- return solve(coins, amount, mem)

solve(coins, amount, mem):
    if amount == 0:
        return 0
    
    if amount in mem:
        return mem[amount]

    min_coins = sys.maxsize
    for coin in coins:
        if coin <= amount:
            result = solve(coins, amount - coin)
            if result != sys.maxsize:
                min_coins = min(min_coins, 1 + result)
    
    mem[amount] = min_coins
    return min_coins

## Time complexity

- The solve recursive function is called once for each amount, so it will run O(amount) time. For each call, we loop over the coins array, so if coins array has n elements, the time complexity = O(amount * n)

## Space complexity

- O(amount) for the mem dict and recursive stack.

