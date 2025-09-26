# Given a string and a pattern, find out if the string contains any permutation of the pattern.

from typing import Dict

def string_contains_pattern(sentence: str, pattern: str) -> bool:
    wstart = 0
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
            return True
         
        if wend >= len(pattern) - 1:
            left_letter = sentence[wstart]
            
            if left_letter in freq:
                if freq[left_letter] == 0:
                    matched -= 1
                
                freq[left_letter] = freq.get(left_letter) + 1
            
            wstart += 1
            
        
            
    return False

print(string_contains_pattern("oidbcaf", "abc"))
print(string_contains_pattern("odicf", "dc"))