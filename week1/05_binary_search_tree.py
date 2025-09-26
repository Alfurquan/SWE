"""
Week 1 - Problem 5: Binary Search Tree Implementation
Difficulty: Medium | Time Limit: 30 minutes | Google L5 Fundamental

PROBLEM STATEMENT:
Implement a Binary Search Tree with basic operations

OPERATIONS:
- insert(val): Insert value into BST
- search(val): Return True if value exists
- delete(val): Remove value from BST
- inorder(): Return sorted list of values
- validate(): Check if tree maintains BST property

REQUIREMENTS:
- Maintain BST property (left < root < right)
- Handle duplicates (define behavior)
- Efficient deletion with proper restructuring
- Edge cases: empty tree, single node, etc.

REAL-WORLD CONTEXT:
Database indexing, file systems, expression parsing, autocomplete systems

FOLLOW-UP QUESTIONS:
- How to balance the tree (AVL, Red-Black)?
- Thread safety for concurrent operations?
- Persistence and recovery?
- Range queries and bulk operations?

EXPECTED INTERFACE:
bst = BST()
bst.insert(5)
bst.insert(3)
bst.insert(7)
print(bst.search(3))    # True
print(bst.inorder())    # [3, 5, 7]
bst.delete(3)
print(bst.validate())   # True
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
