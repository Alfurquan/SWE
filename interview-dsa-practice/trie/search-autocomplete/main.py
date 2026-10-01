from typing import Dict, Optional, List, Tuple

class Node:
    def __init__(self):
        self.children: Dict[str, 'Node'] = {}
        self.end_of_word = False
        self.suggestions: List[str] = []

    def add_child(self, child: str):
        self.children[child] = Node()

    def has_child(self, child: str) -> bool:
        return child in self.children

    def get_child(self, child: str) -> 'Node':
        return self.children[child]

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str):
        current = self.root

        for letter in word:
            if not current.has_child(letter):
                current.add_child(letter)

            current = current.get_child(letter)

            if len(current.suggestions) < 3:
                current.suggestions.append(word)

        current.end_of_word = True

    def get_suggestions(self, prefix: str) -> List[str]:
        node = self._walk(prefix)

        return [] if node is None else node.suggestions

    def _walk(self, word: str) -> Optional[Node]:
        current = self.root

        for letter in word:
            if not current.has_child(letter):
                return None

            current = current.get_child(letter)

        return current

class Autocomplete:
    def __init__(self, products: List[str], freqs: List[int]):
        self.trie = Trie()
        product_freq: List[Tuple[str, int]] = []

        for index in range(len(products)):
            product_freq.append((products[index], freqs[index]))

        product_freq.sort(key=lambda product: (-product[1], product[0]))

        for product, freq in product_freq:
            self.trie.insert(product)

    def get_suggestions(self, search_word: str) -> List[List[str]]:
        result: List[List[str]] = []
        prefix = ""

        for letter in search_word:
            prefix += letter
            result.append(self.trie.get_suggestions(prefix))

        return result

