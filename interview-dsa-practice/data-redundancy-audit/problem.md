# Datacenter Redundancy Audit (Single Points of Failure)

We are auditing a newly constructed global network of N data centers, labeled from 0 to N - 1. The network is fully connected, meaning every data center can communicate with every other data center through a series of bidirectional fiber-optic links.

You are given an array of connections, where connections[i] = [u, v] represents a bidirectional fiber link between data center u and data center v.

To ensure high availability, the infrastructure team needs to identify any Single Points of Failure (SPOF). A link is considered a SPOF (or a "critical connection") if, in the event that this specific link is cut, the network becomes partitioned and some data centers can no longer communicate with each other.

Task: Write a function that returns a list of all critical connections in the network. You may return the links in any order.

---

## Approach

### Data Structures

- We will represent the network as an adjacency list to efficiently store and traverse the connections between data centers.
- We will use two arrays, `disc` and `low`, to keep track of discovery times and the lowest reachable discovery time for each data center during a Depth-First Search (DFS).

### Algorithm

- Build the adjacency list from the given connections.
- Initialize the `disc` and `low` arrays to store discovery times and low values for each data center.
- Perform a DFS on the graph, starting from an unvisited data center with a discovery time of 0.
- For each DFS call
    - Update the discovery time and low value for the current data center.
    - For each adjacent data center:
        - If it has not been visited and not the parent of the current data center, recursively perform DFS on it.
        - After returning from the recursive call, update the low value of the current data center.
        - If the low value of the adjacent data center is greater than the discovery time of the current data center, then the connection between them is a critical connection (SPOF).
- Collect all critical connections in a list and return it.