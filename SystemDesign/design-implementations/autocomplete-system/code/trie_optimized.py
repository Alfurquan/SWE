from typing import List, Dict, Tuple

class Node:
    def __init__(self):
        self.children: Dict[str, 'Node'] = {}
        self.end_of_word = False
        self.top_k_completions: List[Tuple[int, str]] = []

    def add_child(self, letter: str):
        self.children[letter] = Node()

    def get_child(self, letter: str) -> 'Node':
        return self.children[letter]

    def has_child(self, letter: str) -> bool:
        return letter in self.children

    def get_children(self) -> List['Node']:
        return self.children.values()

class Trie:
    def __init__(self, k: int = 50):
        self.root = Node()
        self.k = k

    def insert(self, word: str, frequency: int):
        current = self.root
        
        for letter in word:
            if not current.has_child(letter):
                current.add_child(letter)

            self.update_top_k(current, word, frequency)
            current = current.get_child(letter)
            
        self.update_top_k(current, word, frequency)
        current.end_of_word = True

    def get_top_k_suggestions(self, prefix: str) -> List[str]:
        node = self.find_last_node(prefix)
        if node is None:
            return []
        return [word for freq, word in node.top_k_completions]
    
    def find_last_node(self, prefix: str) -> Node:
        current = self.root

        for letter in prefix:
            if not current.has_child(letter):
                return None

            current = current.get_child(letter)

        return current

    def update_top_k(self, node: Node, word: str, frequency: int):
        # Check if the word is already in top_k_completions
        for i, (freq, w) in enumerate(node.top_k_completions):
            if w == word:
                node.top_k_completions[i] = (freq + frequency, word)
                break
        else:
            node.top_k_completions.append((frequency, word))

        # Sort and keep only top k
        node.top_k_completions.sort(key=lambda x: (-x[0], x[1]))
        if len(node.top_k_completions) > self.k:
            node.top_k_completions.pop()