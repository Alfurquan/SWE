from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.n = n
        self.rank: List[int] = [0] * (n)
        self.parent: List[int] = [i for i in range(n)]

    def find(self, x) -> int:
        if x == self.parent[x]:
            return x
        
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        parx = self.find(x)
        pary = self.find(y)

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

class Network:
    def min_cost_to_connect(self, points: List[List[int]]) -> int:
        n = len(points)

        if n == 1:
            return 0

        result: List[List[int]] = []

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                result.append([i, j, dist])

        result.sort(key=lambda point: point[2])

        uf = UnionFind(n)
        total_cost = 0

        for point in result:
            if uf.n == 1:
                break
            if uf.union(point[0], point[1]):
                total_cost += point[2]

        return total_cost