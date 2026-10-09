from typing import List, Set, Tuple, Dict

class Node:
    def __init__(self):
        self.children: Dict[str, 'Node'] = {}
        self.end_of_word = False

    def add_child(self, child: str):
        self.children[child] = Node()

    def has_child(self, child: str) -> bool:
        return child in self.children

    def get_child(self, child: str) -> 'Node':
        return self.children.get(child, None)

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str):
        current = self.root

        for letter in word:
            if not current.has_child(letter):
                current.add_child(letter)

            current = current.get_child(letter)

        current.end_of_word = True


class SwipeTypePathValidator:
    def is_path_possible(self, board: List[List[str]], word: str) -> bool:
        dirs: List[List[int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        rows = len(board)

        if board is None or rows == 0:
            return False

        cols = len(board[0])

        for row in range(rows):
            for col in range(cols):
                if board[row][col] == word[0]:
                    visited: Set[Tuple[int, int]] = set()
                    if self.can_form(board, word, row, col, 0, visited, dirs):
                        return True

        return False

    def get_all_possible_words(self, board: List[List[str]], words: List[str]) -> List[str]:
        rows = len(board)
        cols = len(board[0])
        dirs: List[List[int]] = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        result: Set[str] = set()

        trie = Trie()

        for word in words:
            trie.insert(word)

        for row in range(rows):
            for col in range(cols):
                if trie.root.has_child(board[row][col]):
                    visited: Set[Tuple[int, int]] = set()
                    self.get_words(board, trie.root.get_child(board[row][col]), board[row][col], row, col, visited, dirs, result)

        return list(result)

    def get_words(self, board: List[List[str]], node: Node, word: str, row: int, col: int, visited: Set[Tuple[int, int]], dirs: List[List[int]], result: Set[str]):
        rows = len(board)
        cols = len(board[0])
        
        if node.end_of_word:
            result.add(word)

        visited.add((row, col))

        for direction in dirs:
            nrow = row + direction[0]
            ncol = col + direction[1]

            if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols or (nrow, ncol) in visited:
                continue

            if node.has_child(board[nrow][ncol]):
                self.get_words(board, node.get_child(board[nrow][ncol]), word + board[nrow][ncol], nrow, ncol, visited, dirs, result)

        visited.remove((row, col))


    def can_form(self, board: List[List[str]], word: str, row: int, col: int, index: int, visited: Set[Tuple[int, int]], dirs: List[List[int]]) -> bool:
        rows = len(board)
        cols = len(board[0])

        if index == len(word) - 1:
            return True

        visited.add((row, col))

        for direction in dirs:
            nrow = direction[0] + row
            ncol = direction[1] + col

            if nrow < 0 or nrow >= rows or ncol < 0 or ncol >= cols or (nrow, ncol) in visited:
                continue

            if board[nrow][ncol] == word[index + 1]:
                if self.can_form(board, word, nrow, ncol, index + 1, visited, dirs):
                    return True

        visited.remove((row, col))
        return False