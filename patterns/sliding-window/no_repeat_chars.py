# Given a string, find the length of the longest substring which has no repeating characters.

from typing import Dict

def longest_len_substring(input: str) -> int:
    max_length = 0
    wstart = 0
    char_to_index_map: Dict[str, int] = {}    
    
    for wend in range(len(input)):
        letter = input[wend]
        if letter in char_to_index_map:
            wstart = max(wstart, char_to_index_map[letter] + 1)
            
        max_length = max(max_length, wend - wstart + 1)
        char_to_index_map[letter] = wend
        
    return max_length

print(longest_len_substring("abccde"))