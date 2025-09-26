# Given a string and a pattern, find all anagrams of the pattern in the given string.

from typing import List, Dict

def find_all_anagrams(sentence: str, pattern: str) -> List[int]:
    wstart = 0
    result: List[int] = []
    freq: Dict[str, int] = {}
    matched = 0
    
    for letter in pattern:
        freq[letter] = freq.get(letter, 0) + 1
        
    for wend in range(len(sentence)):
        letter = sentence[wend]
        
        if letter in freq:
            freq[letter] = freq[letter] - 1
            
            if freq[letter] == 0:
                matched += 1
                
        if matched == len(freq):
            result.append(wstart)
            
        if wend >= len(pattern) - 1:
            left_char = sentence[wstart]
            
            if left_char in freq:
                if freq[left_char] == 0:
                    matched -= 1
                
                freq[left_char] = freq[left_char] + 1
            
            wstart += 1
    return result

print(find_all_anagrams("ppqp", "pq"))
print(find_all_anagrams("abbcabc", "abc"))