from typing import List

class UF:
    def __init__(self, n: int):
        self.n = n
        self.rank = [0] * (n + 1)
        self.parent = [i for i in range(1, n + 1)]

    def find(self, node: int) -> int:
        if node == self.parent[node]:
            return node
        
        self.parent[node] = self.find(self.parent[node])
        return self.parent[node]
    
    def union(self, nodex: int, nodey: int) -> bool:
        parx = self.find(nodex)
        pary = self.find(nodey)

        if parx == pary:
            return False
        
        if self.rank[parx] < self.rank[pary]:
            self.parent[parx] = pary
        elif self.rank[pary] < self.rank[parx]:
            self.parent[pary] = parx
        else:
            self.parent[pary] = parx
            self.rank[parx] += 1

        self.n -= 1
        return True
    
class DataCenterFibreExpansion:
    def min_cost_to_expand_cable(self, n: int, existing_links: List[List[int]], possible_links: List[List[int]]) -> int:
        uf = UF(n)

        for link in existing_links:
            uf.union(link[0], link[1])

        possible_links.sort(key=lambda link: link[2])

        min_cost = 0

        for link in possible_links:
            if uf.union(link[0], link[1]):
                min_cost += link[2]

        return min_cost if uf.n == 1 else -1