from typing import List, Dict, Tuple, Optional
import heapq
import string

class Node:
    def __init__(self):
        self.children: Dict[str, 'Node'] = {}
        self.end_of_word = False

    def add_child(self, child: str):
        self.children[child] = Node()
    
    def get_child(self, child: str) -> 'Node':
        return self.children[child]
    
    def has_child(self, child: str) -> bool:
        return child in self.children

class Trie:
    def __init__(self):
        self.root = Node()
    
    def insert(self, sentence: str):
        current = self.root

        for letter in sentence:
            if not current.has_child(letter):
                current.add_child(letter)
            
            current = current.get_child(letter)
        
        current.end_of_word = True

    def find_sentences(self, prefix: str) -> List[str]:
        last_node = self._find_last_node(prefix)

        if not last_node:
            return []
        
        result: List[str] = []
        self._find(last_node, prefix, result)

        return result
    
    def _find_last_node(self, prefix: str) -> Optional[Node]:
        current = self.root

        for letter in prefix:
            if not current.has_child(letter):
                return None
            
            current = current.get_child(letter)
        
        return current
    
    def _find(self, node: Node, word: str, result: List[str]):
        if not node:
            return
        
        if node.end_of_word:
            result.append(word)

        for letter, child in node.children.items():
            self._find(child, word + letter, result)
    
class Autocomplete:
    def __init__(self, sentences: List[str], frequencies: List[int]):
        self.trie = Trie()
        self.k = 3
        self.freq: Dict[str, int] = {}
        self.prefix = ""
        self._initialize(sentences, frequencies)

    def input(self, char: str) -> List[str]:
        if char == '#':
            self.trie.insert(self.prefix)
            self.freq[self.prefix] = self.freq.get(self.prefix, 0) + 1
            self.prefix = ""
            return []
        
        self.prefix += char
        sentences = self.trie.find_sentences(self.prefix)
        result: List[str] = []

        heap: List[Tuple[int, str]] = []

        heap = [(-self.freq[sentence], sentence) for sentence in sentences]
        heapq.heapify(heap)
        
        while heap:
            _, sentence = heapq.heappop(heap)

            result.append(sentence)
            if len(result) >= self.k:
                break
        
        return result

    def _initialize(self, sentences: List[str], frequencies: List[int]):
        for index in range(len(sentences)):
            sentence = sentences[index]
            self.trie.insert(sentence)
            self.freq[sentence] = frequencies[index]
