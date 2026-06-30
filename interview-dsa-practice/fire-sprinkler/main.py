from typing import List, Optional

class SprinklerNode:
    def __init__(self, node_id: int, requirement: int, left=None, right=None):
        self.node_id = node_id
        self.requirement = requirement
        self.left = left
        self.right = right

class Solution:
    def compute_under_supplied_nodes(self, root: Optional[SprinklerNode], volume: float) -> List[SprinklerNode]:
        if not root:
            return []
        
        result: List[SprinklerNode] = []

        self._traverse(root, volume, result)

        return result

    def _traverse(self, root: Optional[SprinklerNode], volume: float, result: List[SprinklerNode]):
        if not root:
            return
        
        if volume < root.requirement:
            result.append(root)
        
        remaining_volume = max(0.0, volume - root.requirement)

        if root.left is None and root.right is None:
            return

        if root.left and root.right:
            pass_down_volume = remaining_volume / 2.0
        else:
            pass_down_volume = remaining_volume / 1.0

        self._traverse(root.left, pass_down_volume, result)
        self._traverse(root.right, pass_down_volume, result)
        
