from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def find_route(self, root: Optional[TreeNode], source: int, destination: int) -> str:
        if not root:
            return ""
        
        lca_node = self._find_lca(root, source, destination)

        lca_source: List[str] = []
        lca_dest: List[str] = []

        self._traverse(lca_node, source, lca_source)
        self._traverse(lca_node, destination, lca_dest)

        u_moves = "U" * len(lca_source)
        down_moves = "".join(reversed(lca_dest))
        return u_moves + down_moves
    
    def _find_lca(self, root: Optional[TreeNode], start: int, dest: int) -> Optional[TreeNode]:
        if not root:
            return None
        
        if root.val == start or root.val == dest:
            return root
        
        left_res = self._find_lca(root.left, start, dest)
        right_res = self._find_lca(root.right, start, dest)

        if left_res is not None and right_res is not None:
            return root
        
        return left_res if left_res is not None else right_res
    
    def _traverse(self, node: Optional[TreeNode], value: int, order: List[str]) -> bool:
        if not node:
            return False
        
        if node.val == value:
            return True
        
        if self._traverse(node.left, value, order):
            order.append("L")
            return True
        
        if self._traverse(node.right, value, order):
            order.append("R")
            return True

        return False