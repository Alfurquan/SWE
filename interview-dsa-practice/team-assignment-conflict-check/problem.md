# Problem: Team Assignment Conflict Check
A company has n employees labeled 1 to n. You're given a list dislikes where dislikes[i] = [a, b] means employee a and employee b refuse to be on the same team.

You want to split all employees into exactly two teams (every employee on one of the two teams) such that no pair who dislike each other end up on the same team. Return True if such a split is possible, False otherwise.

Example 1
```
Input:  n = 4, dislikes = [[1,2],[1,3],[2,4]]
Output: True
```

Example 2
```
Input:  n = 3, dislikes = [[1,2],[1,3],[2,3]]
Output: False
```

## Solution

The above problem is an example of bipartite graphs where we need to divide the nodes in a graph into two sets A and B, such that every edge in the graph connects a node in A to a node in B. Here the two teams maps to sets A and B and the dislike relationship is represented by the edges between the sets.

I would use a DFS approach here with two coloring mechanism.

Here is the high level algorithm of the approach

- Initialize, color: Dict[int, int] = {}, to hold the color assigned to each node
- Create an adj_List: Dict[int, List[int]] = defaultdict(list) to hold the graph edges from the dislikes array
- Initialize a stack: Deque[int] = deque() to hold the DFS state. We would use iterative DFS here as recursion has memory overhead.
- Loop over each person, 1..n, for each person p
    - if p not in color
        - push p to stack
        - color[p] = 0
        - while stack
            - person = pop(stack)
            - for next_person in adj_list[person]
                - if next_person not in color
                    - color[next_person] = 1 - color[person]
                    - push next_person to stack
                - elif color[next_person] == color[person]
                    - return False
- return True

## Time complexity

- We traverse each node and each edge exactly once, so its O(V + E), where V = no of persons, E = no of dislike relations

## Space complexity

- O(V): For stack
- O(V + E) For adj list