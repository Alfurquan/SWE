# Problem: Diff Tool — Longest Unchanged Sequence
You're building the diff engine for a version-control system. A file is represented as a list of lines (strings). Given the old version and the new version of a file, you want to find how many lines are "unchanged" between them.

A line is part of the unchanged set if it appears in both versions in the same relative order (not necessarily contiguous). Formally: return the length of the longest sequence of lines that appears in both old and new in the same order.

Example 1
```
Input:
  old = ["import os", "def main():", "    x = 1", "    return x", "main()"]
  new = ["import os", "import sys", "def main():", "    x = 2", "    return x"]
Output: 3
```

Example 2
```
Input:
  old = ["a", "b", "c"]
  new = ["x", "y", "z"]
Output: 0
```

Example 3
```
Input:
  old = ["a", "b", "c", "a"]
  new = ["a", "c", "a", "b"]
Output: 3
```

## Solution

This is a dynamic programming problem where we need to find the length of longest common subsequence between old and new version of the file.

Here is how I would approach this problem

Let m = len of old version of file, n = len of new version of file

- Base case

if m <= 0 or n <= 0:
    return 0

- State

state(m, n): Where m and n are the length of old and new version of the file at each step.

- Transition

At each step we do this

if old[m - 1] == new[n - 1]:
    result = 1 + solve(old, new, m - 1, n - 1)
else:
    result = max(solve(old, new, m - 1, n), solve(old, new, m, n - 1))

Here is the high level algorithm of the approach

- Initialize mem: Dict[Tuple[int, int]] = {} // mem cache
- return solve(old, new, len(old), len(new), mem)

```
solve(old, new, m, n, mem):
    if m <= 0 or n <= 0:
        return 0

    if (m, n) in mem:
        return mem[(m,n)]
    
    result = 0
    if old[m - 1] == new[n - 1]:
        result = 1 + solve(old, new, m - 1, n - 1, mem)
    else:
        result = max(solve(old, new, m - 1, n), solve(old, new, m, n - 1))
    
    mem[(m, n)] = result
    return result
```

## Time complexity

- Since we are computing the result for each (m,n) pairs exactly once, time complexity is O(m * n), where m = len of old version and n = len of new version

## Space complexity

- O(m * n) for mem cache