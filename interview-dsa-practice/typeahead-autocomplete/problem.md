# Typeahead Autocomplete Engine

We are building the backend for a search bar autocomplete feature. You need to design an AutocompleteSystem class that provides historical search suggestions as the user types, character by character.

## Requirements:

- Initialization: The system is initialized with a list of historical sentences and a corresponding list of times (frequencies) indicating how many times each sentence has been searched in the past.

- The input(c: str) -> List[str] method: * This method takes a single character c as input.

- Special Character #: If c == '#', it means the user has pressed "Enter" and finished typing their search query. You must save the completed sentence to your historical data (or increment its frequency if it already exists), clear the current input state for the next user, and return an empty list [].

- Normal Character: For any other character, append it to the sequence typed so far. Then, return a list of the top 3 historical sentences that start with the exact prefix typed so far.

## Ranking Rules for the Top 3:

- Sentences must be ordered by their historical frequency in descending order.

- If two sentences have the exact same frequency, tie-break them by lexicographical (alphabetical) order (e.g., "apple" comes before "banana").

## Example walkthrough

```python
# Initialize with some historical data
# "i love you" (5 times), "island" (3 times), "ironman" (2 times), "i love leetcode" (2 times)
system = AutocompleteSystem(
    ["i love you", "island", "ironman", "i love leetcode"], 
   
)

system.input("i") 
# Prefix: "i"
# Matches: "i love you" (5), "island" (3), "i love leetcode" (2), "ironman" (2)
# "i love leetcode" and "ironman" tie on frequency (2). "i love leetcode" wins alphabetically.
# Returns: ["i love you", "island", "i love leetcode"]

system.input(" ") 
# Prefix: "i "
# Matches: "i love you" (5), "i love leetcode" (2)
# Returns: ["i love you", "i love leetcode"]

system.input("a") 
# Prefix: "i a"
# Matches: None.
# Returns: []

system.input("#") 
# User presses enter. "i a" is saved to history with frequency 1.
# State resets.
# Returns: []
```

---

## Approach

### Data Structures

#### Trie

To efficiently store and retrieve sentences based on their prefixes, we can use a Trie (Prefix Tree). Each node in the Trie will represent a character and will have a dictionary of child nodes.

#### Dictionary for Frequencies

We will maintain a dictionary to keep track of the frequency of each sentence. This will allow us to quickly update frequencies when a new sentence is added or an existing sentence is searched again.

#### Heap

To retrieve the top 3 sentences based on frequency and lexicographical order, we can use a min-heap. The heap will store tuples of (-frequency, sentence) to ensure that the highest frequency sentences are at the top of the heap. In case of ties in frequency, the lexicographical order will be maintained automatically since Python's tuple comparison will first compare frequencies and then sentences.

### Logic

- When initializing the AutocompleteSystem, we will insert each historical sentence into the Trie and update their frequencies in the dictionary.
- We keep a string variable called prefix to store the current input from the user.
- When the input method is called with a character:
  - If the character is '#', we will add the current prefix to the Trie and update its frequency in the dictionary. Then, we will reset the prefix and return an empty list.
  - If the character is not '#', we will append it to the prefix and search for sentences in the Trie that match this prefix. We will use a heap to find the top 3 sentences based on their frequencies and lexicographical order, and return them as a list.

### Time Complexity

- Inserting a sentence into the Trie takes O(m) time, where m is the length of the sentence.
- Searching for sentences with a given prefix takes O(p + k log k) time, where p is the length of the prefix and k is the number of sentences that match the prefix (since we need to build a heap of size k).

### Space Complexity

- The space complexity is O(n * m) for storing n sentences of average length m in the Trie, and O(n) for the frequency dictionary. The heap will take O(k) space where k is the number of sentences that match the prefix.
