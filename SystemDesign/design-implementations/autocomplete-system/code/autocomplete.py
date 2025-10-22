from trie import Trie
from typing import List, Dict, Tuple
import heapq
from trie_optimized import Trie as OptimizedTrie

class AutoCompleteSystem:
    def __init__(self):
        self.trie = Trie()
        self.freq: Dict[str, int] = {}

    def insert(self, query: str, frequency: int):
        # O(L), L = length of query
        self.trie.insert(query)
        self.freq[query] = self.freq.get(query, 0) + frequency

    def get_suggestions(self, prefix: str, k: int) -> List[str]:
        # O(NlogK), N = no of matching words for prefix, would be inefficient for large N
        # For better optimizations, we will be precomputing and storing it in node
        words = self.trie.find_words(prefix)
        heap: List[Tuple[int, str]] = []

        for word in words:
            heapq.heappush(heap, (self.freq[word], word))
            if len(heap) > k:
                heapq.heappop(heap)

        result: List[str] = []

        while heap:
            result.append(heapq.heappop(heap)[1])

        return list(reversed(result))

class OptimizedAutoCompleteSystem:
    def __init__(self, k: int = 50):
        self.trie = OptimizedTrie(k)
        self.freq: Dict[str, int] = {}
        self.k = k

    def insert(self, query: str, frequency: int):
        # O(L), L = length of query
        self.freq[query] = self.freq.get(query, 0) + frequency
        self.trie.insert(query, self.freq[query])

    def get_suggestions(self, prefix: str) -> List[str]:
        # O(1) to get top k suggestions from trie node
        return self.trie.get_top_k_suggestions(prefix)