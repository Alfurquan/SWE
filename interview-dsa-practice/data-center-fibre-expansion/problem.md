# Datacenter Fiber Network Expansion
We are expanding the Google Fiber network to connect a newly acquired cluster of datacenters. There are N datacenters in this region, labeled from 1 to N.

For the network to be functional, every single datacenter must be connected to the rest of the cluster, either directly or indirectly through other datacenters.

Some fiber links have already been built by previous engineering teams. You are given a budget and a list of new potential links you can build.

You are given:

N: The total number of datacenters.

existing_links: A list of arrays [u, v], representing datacenters u and v that are already connected. These cost 0 to keep.

possible_links: A list of arrays [u, v, cost], representing a potential new fiber link between u and v that costs cost to build.

Task: Write a function to find the minimum total cost to build new links so that all N datacenters are fully connected. If it is mathematically impossible to connect all of them given the possible_links, return -1.

--- 

## Approach

### Data Structures

- We can represent the datacenters and their connections using a graph. The datacenters will be the nodes, and the existing and potential links will be the edges.
- We can use a Union-Find (Disjoint Set Union) data structure to keep track of connected components of the graph. This will help us determine if two datacenters are already connected and to merge components when we add new links.

### Logic

- We initialize the Union-Find structure with N datacenters.
- We first process the existing_links to connect the datacenters that are already linked using the Union-Find structure.
- Next, we sort the possible_links based on their cost in ascending order.
- We iterate through the sorted possible_links and for each link, we check if the two datacenters it connects are already in the same component using the Union-Find structure. If they are not, we add this link to our total cost and merge the two components.
- After processing all possible_links, we check if all datacenters are connected by verifying if there is only one component in the Union-Find structure. If there is more than one component, it means we cannot connect all datacenters, and we return -1. Otherwise, we return the total cost.

### Time Complexity

- The time complexity of this approach is O(E log E) where E is the number of possible links, due to the sorting step. The Union-Find operations (union and find) are almost O(1) on average, so they do not significantly affect the overall time complexity.