# Given a string and a pattern, 
# find the smallest substring in the given string which has all the characters of the given pattern.

from typing import Dict
import sys

def minimum_window_substring(sentence: str, pattern: str) -> str:
    wstart = 0
    freq: Dict[str, int] = {}
    matched = 0
    substring_start = 0
    min_length = sys.maxsize
    
    for letter in pattern:
        freq[letter] = freq.get(letter, 0) + 1
        
    for wend in range(len(sentence)):
        letter = sentence[wend]
        
        if letter in freq:
            freq[letter] = freq[letter] - 1
            
            if freq[letter] == 0:
                matched += 1 
                
        while matched == len(freq):
            if min_length > wend - wstart + 1:
                min_length = wend - wstart + 1
                substring_start = wstart
            
            left_letter = sentence[wstart]
            if left_letter in freq:
                if freq[left_letter] == 0:
                    matched -= 1
                
                freq[left_letter] += 1
            
            wstart += 1
    
    return "" if min_length == sys.maxsize else sentence[substring_start : substring_start + min_length]


print(minimum_window_substring("aabdec", "abc"))