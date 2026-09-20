from typing import List, Deque, Dict
from collections import deque, defaultdict

class UnionFind:
    def __init__(self, n: int):
        self.rank: List[int] = [0] * (n + 1)
        self.parent: List[int] = list(range(n + 1))

    def find(self, x: int) -> int:
        if x == self.parent[x]:
            return x
        
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        parx = self.find(x)
        pary = self.find(y)

        if parx == pary:
            return False
        
        if self.rank[parx] > self.rank[pary]:
            self.parent[pary] = parx
        elif self.rank[pary] > self.rank[parx]:
            self.parent[parx] = pary
        else:
            self.parent[parx] = pary
            self.rank[parx] += 1

        return True


class TeamAssignment:
    def is_possible(self, n: int, dislikes: List[List[int]]) -> bool:
        adj_list: Dict[int, List[int]] = defaultdict(list)
        stack: Deque[int] = deque()
        color: Dict[int, int] = {}

        for dislike in dislikes:
            adj_list[dislike[0]].append(dislike[1])
            adj_list[dislike[1]].append(dislike[0])

        for person in range(1, n + 1):
            if person not in color:
                stack.appendleft(person)
                color[person] = 0
                while stack:
                    popped_person = stack.popleft()

                    for disliked_person in adj_list[popped_person]:
                        if disliked_person not in color:
                            color[disliked_person] = 1 - color[popped_person]
                            stack.appendleft(disliked_person)
                        elif color[disliked_person] == color[popped_person]:
                            return False

        return True

    def is_possible_with_uf(self, n: int, dislikes: List[List[int]]) -> bool:
        uf = UnionFind(n)
        enemy: Dict[int, int] = {}   # node -> one known enemy (must be on opposite team)

        for a, b in dislikes:
            # a and b must be on different teams; if already same team-group, impossible.
            if uf.find(a) == uf.find(b):
                return False

            if b in enemy:
                uf.union(a, enemy[b])
            else:
                enemy[b] = a

            if a in enemy:
                uf.union(b, enemy[a])
            else:
                enemy[a] = b

        return True
