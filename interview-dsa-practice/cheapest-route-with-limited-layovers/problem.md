# Problem: Cheapest Route With Limited Layovers
You're building a flight-search backend. There are n airports labeled 0 to n - 1. You're given a list of flights where flights[i] = [from_i, to_i, price_i], meaning there's a directed flight from from_i to to_i costing price_i.

Given a src, a dst, and an integer k, return the cheapest total price to travel from src to dst with at most k layovers (i.e., at most k intermediate airports, meaning at most k + 1 flights). If there's no such route, return -1.

Example 1

```
n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
src = 0, dst = 3, k = 1
Output: 700
```

Example 2

```
n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]]
src = 0, dst = 2, k = 1
Output: 200
```

## Solution

I would model the above problem as a directed weighted graph where the city are nodes and the flights array in the problem denote edges with weights as the price to travel between the cities.

We are given a src city, a dst city and an integer k. We wneed to return cheapest total price to travel from src to dst with at most k layovers.

Now for such shortest path problem, dijkstra is the standard algorithm to use, but this problem adds a constraint of at most k layovers which will not allow us to use the standard version of dijkstra's algorithm.

We would a variant of breadth first search here, since breadth first search allows us to travel level by level, it is nice fit to get the shortest path between two nodes in an unweighted graph. But here we have weights and a constraint of at most k layovers so we would tweak the algorithm of BFS a bit.

Here would be the high level algorithm of the approach - 

- We initialize a queue to hold tuples, this denote the state of our BFS, the state includes - city, price to reach there, no of stops taken
- Initialize a dictionary of int -> int called min_cost which will hold the min cost to reach each city.
- We initialize the queue to hold [src, 0, 0]
- Initialize min_cost[src] = 0
- While queue is not empty:
    - pop the tuple (city, cost, stops) from the queue
    - if stops > k
        - break
    - for next_city, price in graph[city]
        - if next_city not in min_cost or min_cost[next_city] > price + cost
            - push (next_city, price + cost, stops + 1) to queue
            - min_cost[next_city] = price + cost

- return -1 if dst not in min_cost else min_cost[dst]


The approach here works even though we are using a global min_cost dictionary because of FIFO approach used in BFS. In FIFO, BFS states are dequeued in non decreasing order of stop-count (level-order). So the moment we attempt to push (x, cost, s), min_cost[x] can only have been set by paths with <= s stops. If the push gets pruned, existing path is both cheaper and uses no more stops.

## Time complexity

The while loop either terminates when queue is empty or stops > k. So it runs once per state popped from the queue.

In each loop iteration we traverse the edges of a city in the graph, if there are E edges in worst case we traverse all E edges in one iteration of the loop, so time complexity is O(K*E), where k is the no of levels.

## Space compexity

O(N) to store the min cost for all the cities and O(N) for storing the city, cost and stops tuple in the queue.
