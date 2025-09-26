class QuadTreeNode:
    def __init__(self, x_min, y_min, x_max, y_max, capacity=4):
        self.bounds = (x_min, y_min, x_max, y_max)
        self.capacity = capacity
        self.points = []
        self.children = None
        
    def insert(self, point) -> bool:
        x, y = point
        x_min, y_min, x_max, y_max = self.bounds
        
        if not (x_min <= x < x_max and y_min <= y < y_max):
            return False
        
        if len(self.points) < self.capacity and self.children is None:
            self.points.append(point)
            return True
        
        if self.children is None:
            self.subdivide()
            
        for child in self.children:
            if child.insert(point):
                return True
        
        return False
    
    def subdivide(self):
        x_min, y_min, x_max, y_max = self.bounds
        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2
        
        self.children = [
            QuadTreeNode(x_min, y_min, x_mid, y_mid, self.capacity),  # SW
            QuadTreeNode(x_mid, y_min, x_max, y_mid, self.capacity),  # SE
            QuadTreeNode(x_min, y_mid, x_mid, y_max, self.capacity),  # NW
            QuadTreeNode(x_mid, y_mid, x_max, y_max, self.capacity)  # NE
        ]
        
        for point in self.points:
            for child in self.children:
                if child.insert(point):
                    break
        
        self.points = []
        
    def query_range(self, x_min, y_min, x_max, y_max):
        results = []
        bx_min, by_min, bx_max, by_max = self.bounds

        if bx_max < x_min or bx_min > x_max or by_max < y_min or by_min > y_max:
            return results
        
        for point in self.points:
            x, y = point
            if x_min <= x < x_max and y_min <= y < y_max:
                results.append(point)
            
        if self.children:
            for child in self.children:
                results.extend(child.query_range(x_min, y_min, x_max, y_max))
                
        return results
    
qt = QuadTreeNode(0, 0, 100, 100)
qt.insert((10, 10))
qt.insert((50, 50))
qt.insert((75, 80))
qt.insert((20, 30))
qt.insert((60, 60))
print(qt.query_range(0, 0, 50, 50)) 