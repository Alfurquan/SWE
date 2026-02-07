# Exercise 3: Conflict Resolution Mini-Design (Like Counter)

## Problem

Design replication for a “Like counter” on a post.

## Requirements

- Users can like from multiple regions
- Writes can happen concurrently
- Must tolerate network partitions
- The count must be eventually correct
- No global locking


## Your Tasks

1️⃣ Why is last-write-wins incorrect here?

Give 2 clear reasons.

2️⃣ How would you model the data?

Describe:
- The data structure
- What each replica stores

(No CRDT jargon required, but the idea should be there.)

3️⃣ How does merge work?

Explain:

- What happens when replicas sync
- Why it always converges

---

## Solution

In this problem, we are designing the replication for a "Like counter" on a post. 
We will be using multi leader replication here, with multiple leader-follower replication strategy deployed across different datacenters across the globe.

### Design

- Each region has one leader and multiple followers
- Write requests for a region go to the leader in the regional datacenter
- The leader then replicates the write to the followers in the regional datacenter
- The leader of each datacenter replicate changes to leaders of other datancenters
- Read requests are served from followers of a regional datacenter.
- We can use Read your own writes, where if lets say a user likes a post, we serve their reads from the regional leader for 1 minute. This ensures each user sees the changes they make instantly leading to good user experience.

When leaders across datacenters sync the data, then conflicts can happen. 

### Why is last write wins incorrect ?

Last write wins strategy to resolve the conflicts is incorrect here due 

- It can lead to data loss. Lets say user A likes a post in region 1 and user B likes the same post in region 2 at the same time. If the write from region 2 reaches region 1 after the write from region 1, then the like from user A will be lost.
- It does not ensure eventual correctness. In a distributed system, network partitions can happen and messages can be delayed. This means that the last write may not be the most recent write, leading to incorrect counts.

### Data Modeling

We can model the data using a vector clock like structure.

- Each replica (leader in each datacenter) maintains a map of region IDs to counts.
- For example, if we have 3 regions (R1, R2, R3), then the data structure at each replica would look like:
  ```
  {
    "R1": count1,
    "R2": count2,
    "R3": count3
  }
  ```
- Each time a user likes a post in a region, the leader in that region increments the count for that region in its map.

### Merge Process

When replicas sync, they exchange their maps of region IDs to counts.
- Each replica merges the maps by taking the maximum count for each region ID.
- For example, if replica A has the map `{"R1": 5, "R2": 3}` and replica B has the map `{"R1": 4, "R2": 6}`, then after merging, both replicas will have the map `{"R1": 5, "R2": 6}`.
- This ensures that all likes are counted, and no data is lost.
- The total like count for a post can be calculated by summing the counts from all regions in the merged map.
- It always converges because the merging process is commutative and associative, meaning that the order in which replicas sync does not affect the final result.

This approach guarantees eventual consistency because:
- Each like is recorded in the region where it occurred.
- When replicas sync, they always take the maximum count for each region, ensuring that all likes are eventually counted.
- Since the merging process is commutative and associative, the order in which replicas sync does not affect the final result, leading to convergence.

---