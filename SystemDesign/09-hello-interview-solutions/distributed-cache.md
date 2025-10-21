# Distributed Cache

Design a distributed cache system

## 💾 What is a Distributed Cache?

A distributed cache is a system that stores data as key-value pairs in memory across multiple machines in a network. Unlike single-node caches that are limited by the resources of one machine, distributed caches scale horizontally across many nodes to handle massive workloads. The cache cluster works together to partition and replicate data, ensuring high availability and fault tolerance when individual nodes fail.

## Functional Requirements

Core requirements

- Users should be able to set, get and delete key value pairs
- Users should be able to configure time to live for key value pairs
- Data should be evicted according to LRU policy

Out of scope

- Users should be able to configure cache size

## Non Functional Requirements

- System should be highly available, eventual consistency is acceptable
- System should have low latency for cache operations around (< 10 ms for get and set operations)
- System should be scalable to support 1TB data and 100K requests per seconds.

Below the line (out of scope)

- Durability (data persistence across restarts)
- Strong consistency guarantees
- Complex querying capabilities
- Transaction support

## Core Entities

The core entities are right there in front of our face! We're building a cache that stores key-value pairs, so our entities are keys and values.
In other words, the data we need to persist (in memory) are the keys and their associated values.

## API

According to our functional requirements, we have three key operations that we'll need to expose via an API: set, get, and delete.
APIs for the system as simple, listing them down here 

- Setting a key value pair

```shell
POST /:key
{
    "value": <>
}
```

- Getting a key value pair

```shell
GET /:key -> {"value" : <>}
```

- Deleting a key value pair

```shell
DELETE /:key
```

## High Level Design

We will start by building an MVP version that satisifies all the functional requirements. We will later work on enhancing the design to make it scalable and satisfy the non functional requirements.

### Users should be able to set, get, and delete key-value pairs

For this basic functionality, we can use an in memory data structure like hashmap in Java and Dict in python. Here's a high level pseudocode for this

At its core, a cache is just a hash table. Every programming language has one: Python's dict, Java's HashMap, Go's map. They're perfect for this because they give us O(1) lookups and inserts.

```python
class MyCache:
    def __init__(self):
        self.items = {}

    def put(self, key, val):
        self.items[key] = val

    def get(self, key):
        return self.items[key]

    def delete(self, key):
        self.items.pop(key)
```

We can host this code on a single server. When a user makes a API request, we'll parse the request, and then call the appropriate method on our Cache instance, returning the appropriate response.

### Users should be able to configure the expiration time for key-value pairs

We can next add expiration to our cache. We can do so by adding another parameter for expiration to the `put` method. 
We'll need to store a timestamp alongside each value and check it during reads. We'll also need a way to clean up expired entries.

- Instead of storing just values, we now store tuples of (value, expiry_timestamp)
- The get() method checks if the entry has expired before returning it
- The put() method takes an optional TTL parameter and calculates the expiry timestamp

```python
# Check the expiry time of the key on get
get(key):
    (value, expiry) = data[key]
    if expiry and currentTime() > expiry:
        # Key has expired, remove it
        delete data[key]
        return null
        
    return value

# Set the expiry time of the key on set
set(key, value, ttl):
    expiry = currentTime() + ttl if ttl else null
    data[key] = (value, expiry)
```

This handles the basic TTL functionality, but there's a problem: expired keys only get cleaned up when they're accessed. This means our cache could fill up with expired entries that nobody is requesting anymore.
To fix this, we need a background process (often called a "janitor") that periodically scans for and removes expired entries:

```python
cleanup():
    for key, val in items:
        ttl = val.expiry
        if current_time > ttl:
            delete item[key]
```

This cleanup process can run on a schedule (say every minute) or when memory pressure hits certain thresholds. The trade-off here is between CPU usage (checking entries) and memory efficiency (removing expired data promptly).

### Data should be evicted according to LRU policy

Now we need to handle what happens when our cache gets full. We'll use the Least Recently Used (LRU) policy, which removes the entries that haven't been accessed for the longest time. 

In order to implement the LRU policy, we will treat the cache data as a linked list. Whenever any key is added or accessed, we will move it to the head of the linked list. 

When cache becomes full, then the key at the end of the linked list will be the least recently used one and we can evict it to make space.

## Deep Dives

### How do we ensure our cache is highly available and fault tolerant?

In order the make our cache highly available and fault tolerant, we can replicate or duplicate the data across multiple server instances.

Replication of data helps in achieving high availability. If one of the server instance or node fails, the request can be served by another replica/node ensuring the system remains highly available even in case of failures.

The key challenge here is data replication - we need multiple copies of our data spread across different nodes. But this opens up a whole new set of questions:

- How many copies should we keep?
- Which nodes should store the copies?
- How do we keep the copies in sync?
- What happens when nodes fail or can't communicate?

Solution1: Peer to peer replication

In peer-to-peer replication, each node is equal and can accept both reads and writes. Changes are propagated to other nodes using gossip protocols, where nodes periodically exchange information about their state with randomly selected peers.

This provides scalability and availability since there's no single point of failure. When a node receives a write, it can process it immediately and then asynchronously propagate the change to its peers. The gossip protocol ensures that changes eventually reach all nodes in the cluster.

Challenges

While peer-to-peer replication offers great scalability and availability, it comes with some significant challenges. The implementation is more complex than other approaches since each node needs to maintain connections with multiple peers and handle conflict resolution. The eventual consistency model means that different nodes may temporarily have different values for the same key. Additionally, careful consideration must be given to conflict resolution strategies when concurrent updates occur at different nodes.

Solution2: Asynchronous Replication

Approach here is to update one primary copy immediately and then propagate changes to replicas asynchronously -- confirming the write once only the primary has acknowledged the change. This aligns well with the eventual consistency model that most caches adopt (and is a non-functional requirement for us), making it more suitable for a cache with our requirements than synchronous replication.

The asynchronous nature provides several key advantages. First, it enables better write performance since we don't need to wait for replica acknowledgement. It also offers higher availability, as writes can proceed even when replicas are down. The system scales better with additional replicas since they don't impact write latency. Finally, it's a natural fit for cache use cases where some staleness is acceptable.

Challenges

The main trade-offs come from the asynchronous nature. Replicas may temporarily have stale data until changes fully propagate through the system. Since all writes go through a single primary node, there's no need for complex conflict resolution - the primary node determines the order of all updates. However, failure recovery becomes more complex since we need to track which updates may have been missed while replicas were down and ensure they get properly synchronized when they come back online. Additionally, if the primary node fails, we need a mechanism to promote one of the replicas to become the new primary, which can introduce complexity and potential downtime during the failover process.

### How do we ensure our cache is scalable?

While describing the non functional requirements, we mentioned that we need to store 1TB data and support 100K requests per second. Our single node solution will not solve this.

We will need to distribute or shard the data across multiple instances. We will use consistent hashing here to distribute the data across the instances. Consistent hashing ensures that when no of server instances change, only a small amout of data needs to be moved across server instances.

### How can we ensure an even distribution of keys across our nodes?

Without consistent hashing, the naive solution would be to use a simple modulo operation to determine which node a key-value pair should be stored on. For example, if you had 4 nodes, you could use hash(key) % 4 and the result would be the node number that that key-value pair should be stored on.

This works great when you have a fixed number of nodes, but what happens when you add or remove a node?

Consistent hashing is a technique that helps us distribute keys across our cache nodes while minimizing the number of keys that need to be remapped when nodes are added or removed. Instead of using simple modulo arithmetic (which would require remapping most keys when the number of nodes changes), consistent hashing arranges both nodes and keys in a circular keyspace.

So insted of doing hash(key) % 4, we hash the key using the consistent hashing function to get a position on the hash ring. We then move clockwise on the ring to get the first server instance to store the data

### What happens if you have a hot key that is being read from a lot?

Hot keys are a common challenge in distributed caching systems. They occur when certain keys receive disproportionately high traffic compared to others - imagine a viral tweet's data or a flash sale product's inventory count. When too many requests concentrate on a single shard holding these popular keys, it creates a hotspot that can degrade performance for that entire shard.
There are two distinct types of hot key problems we need to handle:

- Hot reads: Keys that receive an extremely high volume of read requests, like a viral tweet's data that millions of users are trying to view simultaneously

- Hot writes: Keys that receive many concurrent write requests, like a counter tracking real-time votes.

Solution1: Read Replicas

We create multiple copies of the same data across different nodes. It makes it easy to distribute read requests across the replicas.

Challenges

While read replicas can effectively distribute read load, they come with significant overhead in terms of storage and network bandwidth since entire nodes need to be replicated. This approach also requires careful management of replication lag and consistency between primary and replica nodes. Additionally, the operational complexity increases as you need to maintain and monitor multiple copies of the same data, handle failover scenarios, and ensure proper synchronization across all replicas. This solution may be overkill if only a small subset of keys are actually experiencing high load.

Solution2: Copies of Hot keys

Unlike read replicas which copy entire nodes, this approach selectively copies only the specific keys that are experiencing high read traffic. The system creates multiple copies of hot keys across different nodes to distribute read load, making it a more targeted solution for handling specific traffic hotspots.

Here's how it works:

- First, the system monitors key access patterns to detect hot keys that are frequently read
- When a key becomes "hot", instead of having just one copy as user:123, the system creates multiple copies with different suffixes:

    - user:123#1 -> Node A stores a copy
    - user:123#2 -> Node B stores a copy
    - user:123#3 -> Node C stores a copy

- These copies get distributed to different nodes via consistent hashing
- For reads, clients randomly choose one of the suffixed keys, spreading read load across multiple nodes
- For writes, the system must update all copies to maintain consistency

This approach is specifically designed for read-heavy hot keys. If you have a key that's hot for both reads and writes, this approach can actually make things worse due to the overhead of maintaining consistency across copies.

Challenges

The main challenge is keeping all copies in sync when data changes. When updating a hot key, we need to update all copies of that key across different nodes. While we could try to update all copies simultaneously (atomic updates), this adds significant complexity. However, most distributed caching systems, including ours, are designed to be eventually consistent - meaning it's acceptable if copies are briefly out of sync as long as they converge to the same value. This makes the consistency challenge much more manageable since we don't need perfect synchronization.

There's also overhead in monitoring to detect hot keys and managing the lifecycle of copies - when to create them and when to remove them if a key is no longer hot. The approach works best when hot keys are primarily read-heavy with minimal writes.

### What happens if you have a hot key that is being written to a lot?

Solution1: Write Batching

Write batching addresses hot writes by collecting multiple write operations over a short time window and applying them as a single atomic update. Instead of processing each write individually as it arrives, the client buffers writes for a brief period (typically 50-100ms) and then consolidates them into a single operation. This approach is particularly effective for counters, metrics, and other scenarios where the final state matters more than tracking each individual update.

Consider a viral video receiving 10,000 view updates per second. Rather than executing 10,000 separate operations to set new values (e.g. views=1, views=2, views=3, etc), write batching might collect these updates for 100ms, then execute a single operation to set the final value 1,000 higher. This reduces the write pressure on the cache node by an order of magnitude while still maintaining reasonable accuracy. The trade-off is a small delay in write visibility, but for many use cases, this delay is acceptable given the substantial performance benefits.

Challenges

The main challenge with write batching is managing the trade-off between batching delay and write visibility. Longer batching windows reduce system load but increase the time until writes are visible. There's also the complexity of handling failures during the batching window - if the batch processor fails, you need mechanisms to recover or replay the buffered writes. Additionally, batching introduces slight inconsistency in read operations, as there's always some amount of pending writes in the buffer. This approach works best for metrics and counters where eventual consistency is acceptable, but may not be suitable for scenarios requiring immediate write visibility.

Solution2: Sharding hot keys with suffixes

Instead of having a single counter or value that receives all writes, the system spreads writes across multiple shards using a suffix strategy. For example, a hot counter key "views:video123" might be split into 10 shards: "views:video123:1" through "views:video123:10". When a write arrives, the system randomly selects one of these shards to update.

This approach effectively distributes write load across multiple nodes in the cluster. For our viral video example with 10,000 writes per second, using 10 shards would reduce the per-shard write load to roughly 1,000 operations per second. When reading the total value, the system simply needs to sum the values from all shards. This technique is particularly powerful because it works with any operation that can be decomposed and recomposed, not just simple counters.

Challenges

The primary challenge with key sharding is the increased complexity of read operations, which now need to aggregate data from multiple shards. This can increase read latency and resource usage, effectively trading write performance for read performance. There's also the challenge of maintaining consistency across shards during failure scenarios or rebalancing operations. The number of shards needs to be carefully chosen - too few won't adequately distribute the load, while too many will make reads unnecessarily complex. Finally, this approach may not be suitable for operations that can't be easily decomposed, such as operations that need to maintain strict ordering or atomicity across all updates.

### How do we ensure our cache is performant?

Our single-node design started off simple and snappy—lookups and writes were O(1) and served straight out of memory. But as we grow our system into a large, distributed cache spanning dozens or even hundreds of nodes, the problem changes. Suddenly, performance isn’t just about how fast a hash table runs in memory. It’s about how quickly clients can find the right node, how efficiently multiple requests are bundled together, and how we avoid unnecessary network chatter.

Once we start scaling out, we can no longer rely solely on local performance optimizations. Even if each individual node is blazing fast, the interaction between nodes and clients, and the overhead of network hops, can introduce significant latency. It’s not unusual for a request that was once served in microseconds to slow down when it has to traverse the network multiple times, deal with connection setups, or handle many small requests individually.

Request batching, which helped us with our hot writes, is also an effective general technique for reducing latency since it reduces the number of round trips between the client and server.

Consistent hashing, which we talked about in our sharding solution, is also an effective general technique for reducing latency since it means we don't need to query a central routing service to find out which node has our data -- saving us a round trip.
 
Constantly tearing down and re-establishing network connections between the client and servers is a recipe for wasted time. Instead of spinning up a fresh connection for every request, clients should maintain a pool of open, persistent connections. This ensures there’s always a ready-to-use channel for requests, removing expensive round-trip handshakes and drastically reducing tail latencies (like those p95 and p99 response times that can make or break user experience).

---