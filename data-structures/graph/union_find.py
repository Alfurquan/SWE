from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.n = n
        self.parent = list(range(n))
        self.rank = [0] * n  
        
        for i in range(n):
            self.parent[i] = i
            self.rank[i] = 0
            
    def find(self, x: int):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]
            
    def union(self, x: int, y: int) -> bool:
        par_x = self.find(x)
        par_y = self.find(y)
        
        # Already connected
        if par_x == par_y:
            return False
        
        if self.rank[par_x] < self.rank[par_y]:
            self.parent[par_x] = par_y
        elif self.rank[par_x] > self.rank[par_y]:
            self.parent[par_y] = par_x
        else:
            self.parent[par_y] = par_x
            self.rank[par_x] += 1
            
        return True
            