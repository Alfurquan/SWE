# The Infrastructure Scenario: Fire Sprinkler Matrix
We are designing a safety simulation for a high-density server warehouse. The water pipes are structured as a Binary Tree.

The root node is connected to the main water main reservoir. Each node in the tree represents a pipe junction that contains a high-pressure fire sprinkler head. Each sprinkler node has a unique integer ID and a specific water consumption requirement (the volume of water in liters per minute it needs to open up and successfully suppress a fire).

When a fire is detected, a specific volume of water, V (in liters), is pumped into the root of the tree.

The Rules of the Flow:
When water arrives at a node, that node absorbs whatever water it needs to meet its consumption requirement. If the volume of water arriving is less than or equal to what it needs, the node absorbs all of it, and nothing flows further down.

If there is leftover water, the remaining volume splits equally between its existing children (left and right).

If a node only has one child, 100% of the remaining water flows to that single child.

If it is a leaf node (no children), any leftover water simply collects at the leaf.

Task: Write a function that takes the root node of this pipe junction tree and the initial water volume V pumped into the system. Return a list of all router/sprinkler IDs that did not receive enough water to meet their required consumption.

Assume a node is defined as follows:

```python
class SprinklerNode:
    def __init__(self, node_id: int, requirement: int, left=None, right=None):
        self.node_id = node_id
        self.requirement = requirement
        self.left = left
        self.right = right
```

---

### Approach

To solve this problem we would use depth-first search (DFS) to traverse the tree. We will keep track of the water volume at each node and determine if it meets the requirement. If it does not, we will add the node's ID to a list of under-supplied sprinklers.

- We will start at the root node with the initial water volume V. For each node, we will calculate the water absorbed and the remaining water. We will then distribute the remaining water to the children nodes according to the rules specified.
- At each node,
    - If the water volume is less than or equal to the requirement, we will add the node's ID to the list of under-supplied sprinklers.
    - If there is leftover water, we will calculate how much water goes to each child and continue the DFS traversal down the tree.
- At the end of the traversal, we will return the list of under-supplied sprinkler IDs.