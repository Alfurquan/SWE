from typing import Dict, List

class Node:
    def __init__(self, letter: str):
        self.letter = letter
        self.children: Dict[str, 'Node'] = {}
        self.end_of_word: bool = False
        
    def add_child(self, ch: str):
        self.children[ch] = Node(ch)
        
    def get_child(self, ch: str) -> "Node":
        return self.children.get(ch, None)

    def has_child(self, ch: str) -> bool:
        return ch in self.children
    
    def get_children(self) -> List['Node']:
        return list(self.children.values())
    
class Trie:
    def __init__(self):
        self.root = Node('')
        
    def insert(self, word: str):
        current = self.root
        for letter in word:
            if not current.has_child(letter):
                current.add_child(letter)
                
            current = current.get_child(letter)
            
        current.end_of_word = True
    
    def is_word_present(self, word: str) -> bool:
        current = self.root
        for letter in word:
            if not current.has_child(letter):
                return False
                
            current = current.get_child(letter)
            
        return current.end_of_word
    
    def get_words(self, prefix: str) -> List[str]:
        last_node = self._get_last_node(prefix)
        
        words: List[str] = []
        
        self.find_words(last_node, prefix, words)
        
        return words
    
    def find_words(self, node: Node, word: str, words: List[str]):
        if node is None:
            return
        
        if node.end_of_word:
            words.append(word)
            
        for child in node.get_children():
            self.find_words(child, word + child.letter, words)
        
    
    def _get_last_node(self, prefix: str) -> Node:
        current = self.root
        
        for letter in prefix:
            if not current.has_child(letter):
                return None
            
            current = current.get_child(letter)
            
        return current
            