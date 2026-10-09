# Problem: Swipe-Type Path Validator

You're building the swipe-typing feature for a phone keyboard. The keyboard is an m x n grid of letters board. A user "swipes" a word by moving their finger from letter to letter, where each consecutive letter must be in a cell 4-directionally adjacent (up/down/left/right) to the previous one.

Given a target word, return True if the word can be formed by such a swipe path. Each cell may be used at most once within a single swipe (the finger can't revisit the same key in one word).

Example 1
```
Input:
  board = [["A","B","C","E"],
           ["S","F","C","S"],
           ["A","D","E","E"]]
  word = "ABCCED"
Output: True
```

Example 2
```
Input:  board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
Output: False
```

## Solution

I would use backtracking here to solve the problem. Basically the idea here is that we loop over all the cells in the board and if any char matches char at index 0 of the word, we start the recursion from that cell and use index of the word to drive the recursion, we try to answer if we can form the word using the recursion

Here is a high level algorithm of the approach

- Initialize rows = len(board), cols = len(board[0])
- Initialize dirs: List[List[int]] = [[-1, 0], [1, 0], [0, 1], [0, -1]]
- return False if board is None or rows = 0
- for row in range(rows):
    - for col in range(cols):
        - visited: Set[Tuple[int, int]] = set()
        - if board[row][col] == word[0]:
            - if can_form(board, word, row, col, 0, visited, dirs):
                - return True

- return False

```python
def can_form(board, word, row, col, index, visited, dirs):
    rows = len(board)
    cols = len(board[0])

    if index == len(word) - 1:
        return True
    
    visited.add((row, col))
    for dir in dirs:
        nrow = row + dir[0]
        ncol = col + dir[1]

        if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols or (nrow, ncol) in visited:
            continue

        if board[nrow][ncol] == word[index + 1]:
            if can_form(board, word, nrow, ncol, index + 1, visited, dirs):
                return True

    visited.remove((row, col))
    return False
```

## Time complexity

- We are looping over all the cells in the board and then recursing over each cell in worst case. In each recursion we look at 4 directions. Recursion depth is defined by the length of the word. So the time complexity here is T(n) = O(M*N * 4^L), where M = no of rows, N = no of cols, L = length of the word

## Space complexity

- O(L) for recursion and O(M*N) for visited tracking set.