# Real-World Graph Algorithm Interview Problems

This document contains realistic Google L5 interview problems based on graph algorithms. These problems are presented as they would be in actual interviews - without explicitly mentioning which algorithm to use.

## **Problem 1: Social Media Influence Analysis**
You're building a feature for a social media platform to identify influential user groups. Given a directed graph where edges represent "follows" relationships, design an algorithm to find groups of users who all follow each other (directly or indirectly through the group). These groups represent echo chambers where information circulates within the group but doesn't easily escape to other parts of the network.

**Follow-up**: How would you handle millions of users? What if the graph changes frequently?

---

## **Problem 2: Microservice Dependency Analyzer**
Your company has hundreds of microservices with complex dependencies. Given a directed graph of service dependencies, write a function to determine if it's possible to deploy all services (no circular dependencies) and if so, return a valid deployment order. Each service must be deployed before any service that depends on it.

**Follow-up**: What if some services can be deployed in parallel? How would you optimize the deployment time?

---

## **Problem 3: Network Infrastructure Resilience**
You're designing a computer network for a data center. Given an undirected graph representing network connections between servers, identify all critical connections whose failure would partition the network into disconnected components. These connections need redundant backup links.

**Follow-up**: What's the minimum number of additional connections needed to make the network resilient to any single connection failure?

---

## **Problem 4: Code Review Dependency Chain**
In your code review system, some pull requests depend on others (must be merged in order). Given a directed graph of PR dependencies, determine if all PRs can be merged and return the order in which they should be reviewed/merged to satisfy all dependencies.

**Follow-up**: How would you handle the case where a PR dependency creates a cycle? What would you tell the developers?

---

## **Problem 5: Supply Chain Vulnerability Assessment**
You're analyzing a supply chain network where companies depend on each other for materials. Given a directed graph of supplier relationships, identify critical suppliers whose disruption would affect the largest number of companies in the network. A disruption at one supplier affects all companies that depend on it (directly or indirectly).

**Follow-up**: How would you rank suppliers by their criticality? What if the graph has millions of nodes?

---

## **Problem 6: Server Farm Critical Points**
You manage a server farm where servers are connected in a network. Some servers act as critical junction points - if they go down, parts of the network become isolated. Given an undirected graph of server connections, identify all servers whose failure would increase the number of disconnected network components.

**Follow-up**: How would you prioritize which critical servers need the most redundancy? What about servers that would completely isolate other servers?

---

## **Problem 7: Financial Transaction Flow Analysis**
You're building a fraud detection system for a payment processor. Given a directed graph of money flows between accounts, identify closed loops of transactions that might indicate money laundering. These are groups of accounts where money circulates between them in a cycle.

**Follow-up**: How would you detect suspicious patterns in real-time as new transactions arrive?

---

## **Problem 8: Course Prerequisites Optimizer**
Design a system for a university to validate and optimize course scheduling. Given a directed graph where nodes are courses and edges represent prerequisites, determine if the course catalog is valid (no impossible prerequisite loops) and suggest an optimal semester-by-semester course sequence for students.

**Follow-up**: What if students want to take multiple courses per semester? How would you minimize the total semesters needed?

---

## **Problem 9: Database Query Dependency Resolver**
You're optimizing a complex analytics platform with interdependent database views and materialized tables. Given a directed graph of dependencies (table A depends on table B if A's data comes from B), design a system to determine the correct refresh order when underlying data changes.

**Follow-up**: How would you handle incremental updates? What if some dependencies are optional?

---

## **Problem 10: Internet Backbone Resilience**
You're working for an ISP analyzing internet backbone infrastructure. Given an undirected graph of fiber optic connections between cities, identify all connections that, if severed (by natural disaster, construction, etc.), would partition the internet into separate regions with no connectivity between them.

**Follow-up**: How would you design redundant routing to ensure no single cable failure can partition the network?

---

## **Problem 11: Recommendation Engine Cycle Detection**
You're building a content recommendation system where items can reference other items (like "customers who bought X also bought Y"). Given a directed graph of item relationships, ensure there are no recommendation cycles that could trap users in infinite loops, and design a traversal order for generating recommendations.

**Follow-up**: How would you handle weighted relationships? What if you want to allow some cycles but limit their depth?

---

## **Problem 12: Corporate Merger Impact Analysis**
During a large corporate merger, you need to analyze reporting structures. Given a directed graph where edges represent "reports to" relationships, identify all management chains and detect any circular reporting relationships that would need to be resolved before the merger.

**Follow-up**: How would you suggest reorganizing the structure to eliminate conflicts while minimizing disruption?

---

---

## **Problem 13: GPS Navigation Optimization**
You're working on Google Maps and need to optimize route calculations. Given a weighted graph where nodes represent intersections and edges represent road segments with travel times (weights), design a system to find the fastest route from a user's current location to their destination. The graph has real-time traffic data that updates edge weights dynamically.

**Follow-up**: How would you handle real-time traffic updates that change edge weights? What if you need to find routes for millions of users simultaneously?

---

## **Problem 14: Data Center Network Design**
You're designing the internal network for a new Google data center. Given a graph where nodes are servers and edges represent possible fiber optic connections with their installation costs (weights), find the minimum cost way to connect all servers while ensuring the network remains connected. You want to minimize total cable installation cost.

**Follow-up**: What if some connections are more reliable than others? How would you balance cost vs. redundancy?

---

## **Problem 15: Currency Exchange Platform**
You're building a currency trading platform that supports multiple currencies. Given a weighted directed graph where nodes are currencies and edge weights represent exchange rates, detect if there are arbitrage opportunities (cycles where you can start with one currency and end up with more of the same currency through a series of exchanges).

**Follow-up**: How would you handle negative spreads (transaction costs)? What if exchange rates update thousands of times per second?

---

## **Problem 16: Internet Routing Protocol**
You're implementing a routing protocol for a network infrastructure company. Given a weighted graph representing network routers and their connection latencies, design an algorithm to find the lowest latency paths from multiple source routers to all other routers in the network. Different source routers may need to route traffic simultaneously.

**Follow-up**: How would you handle router failures that temporarily remove nodes from the graph? What about load balancing across multiple equal-cost paths?

---

## **Problem 17: Corporate Network Consolidation**
Your company is merging with another company and needs to consolidate their office networks. Given a weighted graph where nodes are office locations and edges are potential network connections with costs, design the most cost-effective network that connects all offices. However, you have a limited budget and some connections are mandatory for compliance reasons.

**Follow-up**: What if the budget constraint means you can't connect all offices? How would you prioritize which offices to connect first?

---

## **Problem 18: Supply Chain Cost Optimization**
You're optimizing a global supply chain network. Given a weighted graph where nodes are warehouses/suppliers and edges represent shipping costs and times, find the most cost-effective way to route products from suppliers to regional distribution centers. Each edge has multiple weights: cost, time, and reliability score.

**Follow-up**: How would you handle multi-objective optimization (minimize cost AND time)? What if some routes have capacity constraints?

---

## **Problem 19: Fiber Optic Network Planning**
You're planning a fiber optic network to connect rural communities to high-speed internet. Given a weighted graph where nodes are communities and edges represent fiber installation costs, design a network that connects all communities to existing internet backbone nodes (not all nodes need direct connections to backbone, but all must have a path). Minimize total installation cost.

**Follow-up**: What if the terrain makes some connections impossible? How would you handle the case where connecting some remote communities is extremely expensive?

---

## **Problem 20: Network Latency Optimization**
You're designing a content delivery network (CDN) where content needs to be efficiently routed between any two nodes. Given a weighted graph representing servers and network latencies, precompute the shortest paths between all pairs of servers to enable fast content routing decisions. The network topology changes infrequently but routing queries happen millions of times per second.

**Follow-up**: How would you handle the space complexity of storing all-pairs shortest paths for thousands of servers? What if you need to update the precomputed paths when the network topology changes?

---

## Interview Strategy

These problems test the same algorithmic concepts you've implemented but are framed as real-world engineering challenges that Google engineers actually face. The interviewer would expect you to:

1. **Clarify requirements** - Ask questions about input size, constraints, edge cases
2. **Design the solution** - Explain your approach and why it works
3. **Implement efficiently** - Write clean, bug-free code
4. **Analyze complexity** - Discuss time/space trade-offs
5. **Handle scale** - Consider real-world constraints and optimizations
6. **Test thoroughly** - Walk through examples and edge cases

## Algorithm Mapping (for your reference)

The key is recognizing the underlying graph structure in each business problem and choosing the right algorithmic approach without being told which one to use:

- **Problems 1, 5, 7**: Strongly Connected Components (SCC detection)
- **Problems 2, 4, 8, 9**: Topological Sorting and Cycle Detection
- **Problems 3, 10**: Bridge Detection in Undirected Graphs
- **Problems 6**: Articulation Points (Cut Vertices)
- **Problems 11, 12**: General Graph Traversal with Cycle Detection
- **Problems 13, 16, 18**: Dijkstra's Shortest Path Algorithm
- **Problems 14, 17, 19**: Minimum Spanning Tree (Kruskal's Algorithm)
- **Problem 15**: Negative Cycle Detection (Bellman-Ford Algorithm)
- **Problem 20**: All-Pairs Shortest Path (Floyd-Warshall Algorithm)

## Practice Tips

1. **Start with clarifying questions**: Always ask about input constraints, expected output format, and edge cases
2. **Think out loud**: Explain your reasoning as you work through the problem
3. **Code incrementally**: Write a working solution first, then optimize
4. **Test with examples**: Walk through your algorithm with concrete examples
5. **Discuss trade-offs**: Compare different approaches and their complexity implications
6. **Consider scalability**: How would your solution handle millions of nodes/edges?
