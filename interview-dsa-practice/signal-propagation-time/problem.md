# Signal Propagation Time

You're running a network of n nodes labeled 1 to n. You're given a list of directed, weighted edges times where times[i] = [u, v, w] means a signal travels from node u to node v taking w units of time.

You send a signal starting from a given node k. Return the minimum time it takes for all n nodes to receive the signal. If it's impossible for all nodes to receive it, return -1.

("All nodes receive it" = the time is determined by the node that takes the longest to reach, since the signal spreads along shortest paths.)

Example 1

```
Input:  times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2
```

Example 2

```
Input:  times = [[1,2,1]], n = 2, k = 2
Output: -1
```

## Solution

I would model the solution as a directed weighted graph where weighted edged with weight w denotes that it takes w units of time for a signal to travel from u to v

I would use dijkstra shortest path algorithm here to compute the minimum time it takes for all nodes to receive the signal.

We start the dijkstra from node k, we maintaina time dict where time[u] = time it takes for signal to reach u from k. We use heap to always pop the node with shortest distance and then relax its edges following dijkstra's algorithm.

Finally we take the max of time in the dict and it denotes the minimum time needed for the signal to reach all nodes, since the max of the time here will denote the time it took for the signal to reach the farthest node.

If length of time dict is not equal to n, it means some of the nodes were not reachable, so we return -1

Here is the algorithm

- Initialize adj_list: Dict[int, List[Tuple[int, int]]] = {}
- Initialize time: Dict[int, int] = {}
- Initialize heap: List[Tuple[int, int]] = [] # (a,b) in tuple where a = dist, b = node
- Loop over times, for each time t = [u, v, w]
    - adj_list[u].append((v, w))
- push (0, k) to heap
- time[k] = 0
- while heap
    - pop (t, u) from heap
    - for each v, w in adj_list[u]
        - if v not in time or time[v] > t + w
            - push (t + w, v) to heap
            - time[v] = t + w
- if len(time) != n
    - return -1
return max([for t in time.values()])

## Time complexity

Dijsktra's Algorithm using heap takes O(V + ElogV), where V = no of nodes and E = node of Edges. Here as well we traverse each edge once and while relaxing we push and pop from heap storing nodes, so it takes Log V time

## Space complexity

- (V), for storing nodes in the heap and the time dict