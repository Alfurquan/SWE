"""
Week 2 - Problem 6: Text Justification Algorithm
Difficulty: Medium-Hard | Time Limit: 45 minutes | Google L5 Dynamic Programming

PROBLEM STATEMENT:
Implement text justification with optimal line breaks

OPERATIONS:
- justify(words, max_width): Justify text to given width
- calculateCost(line): Calculate "badness" of a line
- findOptimalBreaks(words, width): Find optimal line breaks
- formatOutput(justified_lines): Format final output

REQUIREMENTS:
- Minimize total "cost" of all lines
- Handle edge cases (single word longer than width)
- Support different cost functions
- Efficient dynamic programming solution

ALGORITHM:
Dynamic programming with cost optimization

REAL-WORLD CONTEXT:
Word processors, PDF generation, newspaper layout, web browsers

FOLLOW-UP QUESTIONS:
- How to handle different fonts/character widths?
- Real-time justification for editors?
- Multi-language support?
- Integration with line breaking algorithms?

EXPECTED INTERFACE:
justifier = TextJustifier()
words = ["This", "is", "an", "example", "of", "text", "justification."]
justified = justifier.justify(words, max_width=16)
print(justified)
# ["This    is    an",
#  "example  of text",
#  "justification.  "]
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
