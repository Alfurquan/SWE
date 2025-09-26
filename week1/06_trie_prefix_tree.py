"""
Week 1 - Problem 6: Trie (Prefix Tree) Implementation
Difficulty: Medium | Time Limit: 25 minutes | Google L5 String Processing

PROBLEM STATEMENT:
Implement a Trie (prefix tree) for efficient string operations

OPERATIONS:
- insert(word): Add word to trie
- search(word): Return True if word exists
- startsWith(prefix): Return True if any word starts with prefix
- delete(word): Remove word from trie
- getAllWords(): Return all words in trie

REQUIREMENTS:
- Support lowercase English letters
- Efficient prefix matching
- Handle edge cases (empty strings, etc.)
- Memory efficient implementation

REAL-WORLD CONTEXT:
Autocomplete systems, spell checkers, IP routing tables, contact search

FOLLOW-UP QUESTIONS:
- How to support case-insensitive search?
- Memory optimization techniques?
- Supporting Unicode characters?
- Fuzzy matching implementation?

EXPECTED INTERFACE:
trie = Trie()
trie.insert("apple")
trie.insert("app")
print(trie.search("app"))        # True
print(trie.search("appl"))       # False
print(trie.startsWith("app"))    # True
trie.delete("app")
print(trie.getAllWords())        # ["apple"]
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
