from typing import List, Dict

class Node:
    def __init__(self):
        self.children: Dict[str, 'Node'] = {}
        self.end_of_word = False

    def add_child(self, letter: str):
        self.children[letter] = Node()

    def get_child(self, letter: str) -> 'Node':
        return self.children[letter]

    def has_child(self, letter: str) -> bool:
        return letter in self.children

    def get_children(self, letter: str) -> List['Node']:
        return self.children.values()

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

    def find_words(self, prefix: str) -> List[str]:
        node = self.find_last_node(prefix)
        words: List[str] = []
        self.collect_words(node, prefix, words)
        return words

    def find_last_node(self, prefix: str) -> Node:
        current = self.root

        for letter in prefix:
            if not current.has_child(letter):
                return None

            current = current.get_child(letter)

        return current

    def collect_words(self, node: Node, word: str, words: List[str]):
        if node is None:
            return

        if node.end_of_word:
            words.append(word)

        for letter in node.children:
            self.collect_words(node.get_child(letter), word + letter, words)
    