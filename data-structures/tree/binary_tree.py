class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.leftChild = None
        self.rightChild = None
        
class BinarySearchTree:
    def __init__(self):
        self.root: TreeNode = None
    
    def insert(self, value: int):
        node = TreeNode(value)
        current = self.root
        prev = None
        while current:
            prev = current
            if value < current.val:
                current = current.leftChild
            else:
                current = current.rightChild
                
        if prev is None:
            self.root = node
        else:
            if value < prev.val:
                prev.leftChild = node
            else:
                prev.rightChild = node
        
    def find(self, value: int) -> bool:
        current = self.root
        
        while current:
            if value < current.val:
                current = current.leftChild
            elif value > current.val:
                current = current.rightChild
            else:
                return True
            
        return False
    
    
if __name__ == '__main__':
    tree = BinarySearchTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(5)
    print(tree.find(2))
    print(tree.find(5))
        