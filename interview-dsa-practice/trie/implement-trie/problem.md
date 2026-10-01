# Problem: Implement a Prefix Search Engine
Build a Trie class supporting three operations for a word-lookup service:

insert(word) — add word to the trie.
search(word) — return True if word was inserted (exact match), else False.
starts_with(prefix) — return True if any inserted word begins with prefix, else False.

Example 

```
trie = Trie()
trie.insert("apple")
trie.search("apple")       -> True
trie.search("app")         -> False    # "app" was never inserted as a full word
trie.starts_with("app")    -> True     # but it IS a prefix of "apple"
trie.insert("app")
trie.search("app")         -> True     # now it's a full word
```