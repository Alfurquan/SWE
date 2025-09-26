"""
Week 2 - Problem 1: Self-Balancing BST (AVL Tree)
Difficulty: Hard | Time Limit: 60 minutes | Google L5 Advanced Trees

PROBLEM STATEMENT:
Implement an AVL tree with automatic balancing

OPERATIONS:
- insert(val): Insert with automatic rebalancing
- delete(val): Delete with rebalancing
- search(val): Find value in tree
- getHeight(): Return tree height
- isBalanced(): Verify AVL property

REQUIREMENTS:
- Maintain AVL property (height difference ≤ 1)
- Implement rotations (left, right, left-right, right-left)
- O(log n) time complexity for all operations
- Handle all edge cases

REAL-WORLD CONTEXT:
Database indexing, file systems, real-time systems requiring guaranteed performance

FOLLOW-UP QUESTIONS:
- AVL vs Red-Black tree trade-offs?
- Concurrent access patterns?
- Bulk operations optimization?
- Memory usage analysis?

EXPECTED INTERFACE:
avl = AVLTree()
avl.insert(10)
avl.insert(5)
avl.insert(15)
avl.insert(3)  # May trigger rotation
print(avl.isBalanced())  # True
print(avl.getHeight())   # 2
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
