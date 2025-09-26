# Given a string, find the length of the longest substring in it 
# with no more than K distinct characters.

from typing import Dict

def longest_sub_with_no_more_than_k(input: str, k: int):
    wstart = 0
    max_length = 0
    freq: Dict[str, int] = {}
    
    for wend in range(len(input)):
        letter = input[wend]
        if letter not in freq:
            freq[letter] = 1
        else:
            freq[letter] += 1
        
        while len(freq) > k:
            left_char = input[wstart]
            
            freq[left_char] = freq[left_char] - 1
            if freq.get(left_char) == 0:
                freq.pop(left_char)
            
            wstart += 1
        max_length = max(max_length, wend - wstart + 1)
    
    return max_length
    
print(longest_sub_with_no_more_than_k("cbbebi", 3))

