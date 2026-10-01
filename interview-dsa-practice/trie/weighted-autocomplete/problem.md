# Design Autocomplete with a Weighted Trie

Build an autocomplete service backed by a Trie storing a dynamic dictionary of (word, weight) pairs, supporting four operations:

- insert(word, weight) — add a word with the given weight (overwrite if it already exists).
- update(word, newWeight) — change an existing word's weight (no-op if absent).
- delete(word) — remove a word (no-op if absent).
- topK(prefix, k) — return the k highest-weight words sharing prefix, ties broken lexicographically (smaller string first). Fewer than k matches → return all. Empty prefix matches every word.
topK is the hot path (far more frequent than mutations) — so it's fine to do extra work on mutations to keep queries cheap.

Driver
Implement solution(operations) that replays the operations and returns the outputs of each topK call in order.

Example 1

```
insert('cat',5), insert('car',3), insert('cart',8), insert('dog',2),
topK('ca',2)        -> ['cart','cat']      # cart:8, cat:5, car:3
update('car',9),
topK('ca',2)        -> ['car','cart']      # car:9, cart:8, cat:5
delete('cart'),
topK('ca',2)        -> ['car','cat']       # car:9, cat:5
```

Example 2

```
topK('ca', 3)  on empty dictionary -> []
```

## Solution

The data structure which I will use to solve this problem would be a trie. A trie stores a string character by character, sharing common prefixes and is effiecient in prefix matching. 

In order to optimize the topK suggestions, we would precompute and store it at each node, instead of computing it at query time. This would incur some storage cost but would make the topK query calls faster.

Here is what each Node in the trie would store

- children: Dict[str, Node]
- end_of_word: bool
- scores: Dict[str, int]  // (word, score)

We have options to consider to store the top k
- We can use an ordered dict to store the topK at each node ordered by weight. In this case if the weight changes, we will need to reorder the dict
- We can store the topK as a map of word, weights and then at query time use heap to compute the topK and return it.

Here is the high level algorithm for the approach

insert(word, weight)
- Insert the word character by character in trie, at each trie node in the path along the word, store the word with the weight

update(word, weight)
- Update all the trie node with the word to its new weight

delete(word)
- Remove word from the topK dict at each node in the path from root for all chars in the word
- mark end_of_word as false for this word at the last char node

topK(prefix, k)
- Walk at the path from root to the last node of the prefix
- Get the word, weight dict and use a heap to get the top K words and return it.

If we want to keep topK faster, instead of using heap to get topK at query time, we would need to maintain sorted order list of words, weight rather than using a dict of word to weight. This would have have extra cost during insert, update and delete as we would need to sort the list to keep it in order

## Time complexity

- insert: O(L), if using dict to store topK at each node
- update: O(L), if using dict to store topK at each node
- delete: O(L), if using dict to store topK at each node
- topK: O(L) + MlogK, logK for heap operations for M words

If we want to keep sorted list at each node then

- insert: O(L + MlogM), for M words at each node
- update: O(L + MlogM)
- delete: O(L + MlogM)
- topK: O(L + K)

## Space complexity

- O(N * L) for trie


