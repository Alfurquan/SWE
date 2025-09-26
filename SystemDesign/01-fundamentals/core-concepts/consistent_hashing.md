# Consistent Hashing

In a distributed system where nodes (servers) are frequently added or removed, efficiently routing requests becomes challenging
A common approach is to hash the request and assign it to server using `Hash(key) mod N`, where N is the number of servers.

However this method is highly dependent on the number of servers and any change in N can lead to significant rehashing, causing a major re distribution of keys

Consistent hashing addresses this issue by ensuring that only a small subset of keys need to be reassigned when keys are added or removed.

## Problem with traditional hashing

Imagine we're building a high-traffic web application that serves millions of users daily. To handle the load efficiently, we distribute incoming requests across multiple backend servers using a hash-based load balancer.

Our system consists of 5 backend servers (S0, S1, S2, S3, S4), and requests are assigned using a hash function that maps each user's IP address to a specific server.

The process works like this:

- The load balancer takes a user’s IP address (or session ID).
- A hash function maps the IP to one of the backend servers by taking the sum of bytes in the IP address and computing mod 5 (since we have 5 servers).
- The request is routed to the assigned server, ensuring that the same user is always directed to the same server for session consistency.

Everything works fine, until we decide to scale

### Scenario 1: Adding a new server

As traffic increases, we decide to scale up by adding a new backend server (S5). Now, the hash function must be modified to use mod 6 instead of mod 5 since we have 6 servers now.

This seemingly simple change completely disrupts the existing mapping, causing most users to be reassigned to different servers.

This results into massive rehashing, leading to high overhead, and potential downtime.

### Scenario 2: Removing a server (S4)

Now, let’s say one of the servers (S4) fails or is removed. The number of servers drops to 4, forcing the hash function to switch from mod 5 to mod 4.
Even though only one server was removed, most users are reassigned to different servers. 

## How consistent hashing works ?

Consistent hashing is a distributed hashing technique used to efficiently distribute data across multiple nodes (servers, caches, etc.).

It uses a circular hash space (hash ring) with a large and constant hash space.

Both nodes (servers, caches, or databases) and keys (data items) are mapped to positions on this hash ring using a hash function.

Unlike modulo-based hashing, where changes in the number of nodes cause large-scale remapping, consistent hashing ensures that only a small fraction of keys are reassigned when a node is added or removed, making it highly scalable and efficient.

### Constructing the hash ring

Instead of distributing keys based on Hash(key) mod N, consistent hashing places both servers and keys on a circular hash ring.

**Defining hash space**

- We use a large, fixed hash space ranging from 0 to 2^32 - 1 (assuming a 32-bit hash function).
- This creates a circular structure, where values wrap around after reaching the maximum limit.

**Placing severs on the ring**

- Each server (node) is assigned a position on the hash ring by computing Hash(server_id).
- Using the above example with 5 servers (S0, S1, S2, S3, S4), the hash function distributes them at different positions around the ring.

**Mapping Keys to Servers**

- When a key is added, its position is determined by computing Hash(key).
- We then move clockwise around the ring until we find the next available server.
- The key (or request) is assigned to this server for storage or retrieval.

### Adding a new server

Suppose we add a new server (S5) to the system.

- The position of S5 falls between S1 and S2 in the hash ring.
- S5 takes over all keys (requests) that fall between S1 and S5, which were previously handled by S2.
- Example: User D’s requests which were originally assigned to S2, will now be redirected to S5.

### Removing a server

When a server, such as S4, fails or is removed from the system:

- All keys previously assigned to S4 are reassigned to the next available server in the ring (S3).
- Only the keys (requests) that were mapped to S4 need to move, while all other keys remain unaffected.

### Virtual nodes

In basic consistent hashing, each server is assigned a single position on the hash ring. However, this can lead to uneven data distribution, especially when:

- The number of servers is small.
- Some servers accidentally get clustered together, creating hot spots.
- A server is removed, causing a sudden load shift to its immediate neighbor.

Virtual nodes (VNodes) are a technique used in consistent hashing to improve load balancing and fault tolerance by distributing data more evenly across servers.

Instead of assigning one position per server, each physical server is assigned multiple positions (virtual nodes) on the hash ring.

- Each server is hashed multiple times to different locations on the ring.
- When a request (key) is hashed, it is assigned to the next virtual node in a clockwise direction.
- The request is then routed to the actual server associated with the virtual node.
