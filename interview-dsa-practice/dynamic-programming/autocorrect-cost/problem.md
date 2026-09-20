# Problem: Autocorrect Cost
You're building the autocorrect engine for a keyboard. Given a typed word and a dictionary word, you want to know the minimum number of single-character edits to transform the typed word into the dictionary word, so you can rank suggestions by how "close" they are.

The allowed edits, each costing 1:

- Insert a character,
- Delete a character,
- Replace a character.

Return the minimum number of edits to transform word1 into word2.

Example 1
```
Input:  word1 = "horse", word2 = "ros"
Output: 3
```

Example 2
```
Input:  word1 = "intention", word2 = "execution"
Output: 5
```

Example 3
```
Input:  word1 = "", word2 = "abc"
Output: 3
```

## Solution

This is a dynamic programming problem. Basically we need to trasnform typed workd to dictionary word, at each character, we can either insert, delete or replace a character. So I will approach it as a dynamic programming problem here as it satisfies both the conditions

- Solution at each step can be broken down into substeps which overlap (Overlapping subproblems)
- Optimal answer for the problem can be formed from the optimal answers to the subproblems

So here is how we can define the parts of this problem

- Base case

Lets assume m = len(typed_word), n = len(dictionary_word)

if m == 0 and n == 0:
    return 0

if m == 0:
    return n // We insert all the n chars of dictionary word

if n == 0:
    return m // We delete all the m chars of typed word

- State

At each step, we maintain this state

state(m, n) // where m and n denotes the no of leftover chars in typed and dictionary words

- Transition

At each step, we do this transition

if typed_wprd[m - 1] == dictionary_word[n - 1]:
    result = solve(typed_word, dictionary_word, m - 1, n - 1)
else:
    result = 1 + min(min(
        solve(typed_word, dictionary_word, m - 1, n), // Delete
        solve(typed_word, dictionary_word, m, n - 1), // Insert
    ),
    solve(typed_word, dictionary_word, m - 1, n - 1)) // replace

Here is the high level algorithm for the approach

- Initialize mem: Dict[Tuple[int, int], int] = {} // mem cache
- return solve(typed_word, dict_word, len(typed_word), len(dict_word), mem)

```
solve(typed_word, dict_word, m, n, mem):
    if m == 0 and n == 0:
        return 0
    
    if m == 0:
        return n
    
    if n == 0:
        return m
    
    if (m,n) in mem:
        return mem[(m, n)]
    
    min_result = 0
    if typed_word[m - 1] == dict_word[n - 1]:
        min_result = solve(typed_word, dict_word, m - 1, n - 1, mem)
    else:
        min_result = 1 + min(min(
        solve(typed_word, dict_word, m - 1, n), // Delete
        solve(typed_word, dict_word, m, n - 1), // Insert
    ),
    solve(typed_word, dict_word, m - 1, n - 1)) // replace

    mem[(m, n)] = min_result
    return min_result
```

## Time complexity 

- O(m * n), where m = len(typed_word), n = len(dict_word). As each m,n pair is computed exactly once and we store the result in mem cache

## Space complexity

- O(m * n) for mem cache.