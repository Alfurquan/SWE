from typing import Dict, Optional

class Node:
    def __init__(self):
        self.children: Dict[str, 'Node'] = {}
        self.end_of_word = False

    def add_child(self, child: str):
        self.children[child] = Node()

    def has_child(self, child: str) -> bool:
        return child in self.children

    def get_child(self, child: str) -> 'Node':
        return self.children[child]

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        current = self.root

        for letter in word:
            if not current.has_child(letter):
                current.add_child(letter)

            current = current.get_child(letter)

        current.end_of_word = True

    def search(self, word) -> bool:
        node = self._walk(word)

        return node is not None and node.end_of_word

    def starts_with(self, word) -> bool:
        return self._walk(word) is not None

    def _walk(self, word: str) -> Optional[Node]:
        current = self.root

        for letter in word:
            if not current.has_child(letter):
                return None

            current = current.get_child(letter)

        return current