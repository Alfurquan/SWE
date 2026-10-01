# Problem: Search Autocomplete with Top-K Suggestions

Build an autocomplete system. You're given a list of products (strings) and their search frequencies. As a user types a searchWord character by character, after each character you must return up to 3 product suggestions that have the typed string as a prefix.

Ranking of suggestions for a given prefix:

1. Higher frequency first.
2. Ties broken lexicographically (alphabetical order).

Return a list of lists: result[i] is the suggestions after typing the first i+1 characters of searchWord

Example

```
products = ["bag", "bagel", "ban"], frequencies = [1, 1, 1], searchWord = "ba"
Typing 'b'  -> ["bag", "bagel", "ban"]    # all freq 1, so alphabetical
Typing 'ba' -> ["bag", "bagel", "ban"]
```

---

## Solution

For this problem, I would use a trie data structure to store the words, and then as the user types the prefix, would use it to find the top 3 words by frequency and ties being broken lexicographically.

This would be my approach

- Initialize a trie
- Initialize a dict for freq mapping, each word to its frequency
- Insert the words in the trie
- Initialize a empty prefix string
- Initialize a list of list to hold the results, lets call it results
- Loop over the characters in the user typed word, for each character ch,
    - add ch to prefix string
    - get all words starting with ch
    - sort the words by freq desc and lexicographically asc and add to the list by taking top 3
- return results

## Time complexity

- O(N * L) for building the trie, where N = no of words, L = largest length of a word
- O(N * KlogK), where N = no of chars in user typed prefix, klogK for sorting

## Space complexity

- O(N * L) for trie

## Optimization

- We can remove the requirement for sorting, and reduce the time and space complexity by precomputing the top k at each node.
- While inserting a word, at each node store the top 3 words by frequency can be formed by the prefix till the node
- The trade off here is that it makes insert operation costly by search and autocomplete operations becomes faster with a time complexity of O(N * L + K), where N = no of characters in user typed word, L = length of the word, K = 3.
