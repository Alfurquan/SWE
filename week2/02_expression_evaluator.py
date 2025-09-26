"""
Week 2 - Problem 2: Expression Evaluator (Binary Tree)
Difficulty: Medium-Hard | Time Limit: 45 minutes | Google L5 Tree Applications

PROBLEM STATEMENT:
Build an expression evaluator using binary trees

OPERATIONS:
- parseExpression(expr): Parse infix expression into tree
- evaluate(): Calculate result of expression
- toInfix(): Convert back to infix notation
- toPostfix(): Convert to postfix notation

REQUIREMENTS:
- Support +, -, *, /, parentheses
- Handle operator precedence correctly
- Support floating point numbers
- Error handling for invalid expressions

ALGORITHM:
Shunting Yard algorithm for parsing, tree traversal for evaluation

REAL-WORLD CONTEXT:
Compilers, calculators, formula engines (Excel), query optimizers

FOLLOW-UP QUESTIONS:
- How to add new operators?
- Variable support?
- Function calls?
- Optimization techniques?

EXPECTED INTERFACE:
evaluator = ExpressionEvaluator()
tree = evaluator.parseExpression("3 + 4 * (2 - 1)")
print(evaluator.evaluate(tree))    # 7
print(evaluator.toPostfix(tree))   # "3 4 2 1 - * +"
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
