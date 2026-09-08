# Reconnect the Server Network
You have n servers labeled 0 to n - 1. They're wired together with ethernet cables. You're given a list connections where connections[i] = [a, b] means there's a cable directly connecting server a and server b (undirected).

Any server can reach any other server through the cables, directly or indirectly, if they're in the same connected group. You can unplug a cable from anywhere and replug it between any two servers you like. Each such move (remove one cable + place it elsewhere) counts as one operation.

Return the minimum number of operations needed to make the whole network connected (every server reachable from every other). If it's impossible, return -1.

Example 1

```
Input:  n = 4, connections = [[0,1],[0,2],[1,2]]
Output: 1
```

Example 2

```
Input:  n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
Output: 2
```

Example 3

```
Input:  n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
Output: -1
```

## Solution

Here is how I would approach this problem. I would model this problem as an undirected graph where servers are nodes and the connections are edges in the graph.

I would use a data structure called `Union Find` which basically divides the nodes into subsets such that all nodes in a subset have the same parent and are interconnected through edges.

It basically keeps track of two things

- parent: An array where each entry denotes the parent of the set the node belongs to.
- rank: The height of the set to which the node belongs to.

It provides two functions to perform

- union: It helps in unioning two nodes to the same set, making them both share the parent. If makes use of find function to find the parents of the two nodes.
- find: Finding if two nodes belong to the same set

Since this problem here is to make the whole network connected, it boils down to unioning all the servers to the same set, so union find fits here.

We can also optimize the two operations using techniques like path compression and union by rank to make the complexity of the operations O(alpha n) where alpha is inverse ackermann function.

Here is the high level algorithm 

- Initialize the union find data structure which supports find and union operations, pass n, uf = UF(n)
- if len(connections) < n - 1:
    return -1                      # not enough cables, ever
- for each connection (u,v) in connections
    - uf.union(u,v)
      
- return uf.n - 1

## Time complexity

- uf operations take O(alphaV), V = no of servers
- Loop over connections and uf operations take - O(NalphaV), N = no of connections, V = no of servers

## Space complexity

- O(V), for storing rank and parents
