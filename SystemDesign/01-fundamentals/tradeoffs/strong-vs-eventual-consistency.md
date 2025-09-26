# Strong vs Eventual Consistency

In today’s distributed systems, data is almost never stored in a single place. It’s replicated across multiple servers, often spread across data centers around the world to ensure high availability, fault tolerance, and performance.

This global distribution enables scalability but it comes with a critical challenge:

```text
How do we ensure every user and system component sees a consistent and accurate view of the data, especially when updates are happening all the time?
```

This is where consistency models come into play. They define the rules for how and when changes to data become visible across the system.

Two of the most widely discussed models are:

- Strong Consistency – where everyone sees the latest value, always.
- Eventual Consistency – where updates eventually propagate, but temporary inconsistencies are allowed.

## What is data consistency in distributed system ?

In a single-server system, consistency is straightforward: when you write data, any subsequent read returns the most recent value. There’s only one copy of the data.

But in distributed systems, where data is replicated across multiple nodes (for availability, fault tolerance, or low latency), things become more complex.

Imagine you write an update to Node A. That change takes time to propagate to Node B and Node C. During this replication lag, different nodes may temporarily hold inconsistent versions of the same data.

Consistency Models define the rules and guarantees a system provides about:

- When an update becomes visible
- Where it becomes visible (to which users or replicas)
- In what order operations are seen across the system

## Strong Consistency

Strong consistency guarantees that once a write is successfully completed, any read operation from any client or replica will reflect that write or a newer one.

### How it works ?

To achieve strong consistency, the system performs coordinated communication between replicas before confirming a write:

- A client sends a write request, such as updating a value in the database.
- The primary node (e.g., Node A) propagates this write to a group of replicas.
- Each replica (e.g., Node B, Node C) applies the write and sends an acknowledgment.
- Only after receiving acknowledgments from all (or enough) replicas does the system confirm the write as complete to the client.
- From that point onward, any read will return the updated value.

This behavior is made possible through consensus algorithms that ensure all replicas agree on the order of operations. Common protocols used include Paxos and Raft.

### When to use strong consistency ?

Strong consistency is the right choice when your application needs immediate correctness and absolute accuracy.

- Banking and financial systems: Balances and transactions must always be accurate.
- Inventory management: You can’t afford to sell the same item to two people.
- Distributed locking: Locks must be exclusive and reflect the latest state.
- Unique ID generation: Duplicate IDs must be prevented across replicas.

## Eventual Consistency

Eventual consistency is a weaker consistency model that guarantees all replicas in a distributed system will converge to the same value, eventually as long as no new updates are made.

### How it Works ?

- A client sends a write request to a node, such as updating a data item on Node A.
- Node A acknowledges the write immediately, without waiting for other replicas to be updated.
- The updated value is asynchronously propagated to other replicas, such as Node B and Node C.
- While this propagation is in progress, reads from other replicas may return stale or outdated data.
- Once all replicas have received and applied the update, the system is fully consistent again.

This replication process allows the system to stay highly available and responsive, even in the presence of network partitions or server failures.

A temporary inconsistency is acceptable in many scenarios, especially when the data being read is not critical to business correctness and a slight delay in consistency does not harm the user experience.

### Example

Let’s say you're using a social media platform and you update your profile picture.

- You immediately see the new photo on your profile.
- A friend on the other side of the world might still see your old photo for a few seconds due to replication lag.
- After the system finishes syncing, everyone sees the updated photo.

This temporary inconsistency is acceptable because the correctness of the system doesn't depend on everyone seeing the same thing at the exact same moment.

### When to Use Eventual Consistency ?

Eventual consistency is a good fit for applications that require high availability and can tolerate temporary inconsistencies. It is especially effective when systems are distributed globally or need to operate at massive scale.

Common use cases include:

- Social media metrics: Like counts, shares, and view counters can tolerate brief inconsistencies without impacting user experience.
- Product view counts or analytics: Tracking page visits, clicks, or user events can tolerate minor delays in consistency.
- Recommendation systems: Personalized suggestions such as products, movies, or articles do not require real-time accuracy and benefit from fast, large-scale reads.
- DNS (Domain Name System): DNS records are cached at multiple layers worldwide. Slight delays in propagation are acceptable and help maintain global availability.
- Content delivery networks (CDNs): Static assets like images, stylesheets, and scripts are served from edge locations. Updates propagate gradually to balance performance and consistency.
- Shopping cart: Eventual consistency is suitable when users add items from different devices. Conflict resolution strategies (such as merging or last-write-wins) help maintain a coherent experience.

## Variations and Client-Centric Models

### Casual Consistency

If operation A causally precedes operation B (e.g., B reads a value written by A), then all processes see A before B. Operations that are not causally related can be seen in different orders.

Example: In a comment thread, replies should appear after the comment they respond to even if the system is eventually consistent overall.

### Read your writes consistency

After a client performs a write, any subsequent reads by that same client will always reflect the write (or a newer version). Other clients may still see stale data.

Example: You update your profile bio. When you refresh the page, your new bio appears immediately even if it takes a few seconds for others to see it.

### Monotonic read consistency

If a client reads a value, any future reads by the same client will return the same or a newer value. The client will never see an older version of the data.

Example: You see your post has 10 likes. After refreshing, you might see 10 or 11 likes but never fewer than 10.

**Even in an eventually consistent system, applying client-centric guarantees helps preserve a sense of order, responsiveness, and trust for individual users.**

## Choosing the right consistency model

There's no "best" consistency model. The right choice depends heavily on your application's specific requirements:

### Data criticality

How critical is it that all users see the most up-to-date, correct data at all times?

- High (e.g., financial transactions, inventory management)→ Use strong consistency.
- Lower (e.g., social likes, view counts, analytics)→ Eventual consistency is often sufficient.

### User experience expectations

Will users notice or care about stale data? Can the UI manage it gracefully?

For systems where users expect immediate feedback, you can often use:

- Optimistic UI updates (e.g., show the change immediately, then sync)
- Loading indicators (e.g., “Syncing…” or “Updating…”)

Strong consistency reduces confusion, but eventual consistency can be acceptable with the right UX design.

### Performance (Latency) Requirements

How important is low latency for reads and writes?

- Eventual consistency often delivers faster response times, since writes don’t block on global coordination.
- Strong consistency adds overhead especially in geo-distributed systems.

### Availability requirements

Can the system tolerate downtime or errors during network partitions?

- Strong consistency may sacrifice availability to preserve correctness (as per the CAP theorem).
- Eventual consistency allows systems to remain available even during partial failures or network splits.

### Scalability needs

Does the system need to support massive scale across regions or data centers?

- Eventually consistent systems scale more easily especially for read-heavy workloads.
- Strong consistency may limit scaling options due to coordination overhead.

### Conflict resolution

What happens if two users write conflicting data at the same time?

In eventually consistent systems, concurrent writes to different replicas must be reconciled when replicas sync.

Common strategies:

- Last Write Wins (LWW)
- CRDTs (Conflict-Free Replicated Data Types)
- Custom merge logic based on application semantics
