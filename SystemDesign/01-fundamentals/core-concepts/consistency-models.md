# Consistency Models

In modern applications, data rarely lives in just one place. It's spread across multiple servers, potentially in different data centers around the globe.

This distribution brings scalability and resilience, but it also introduces a fascinating challenge: how do we ensure that all users, and all parts of the system, see a coherent and correct view of the data, especially when things are changing rapidly?

This is where consistency models come into play.

## What Exactly is Data Consistency?

In a single-server system, consistency is straightforward. When data is updated, all subsequent reads see that new data. Simple.

But in a distributed system, when you write data to one node (replica), it takes time for that update to propagate to other nodes. During this propagation delay, different nodes might have different versions of the data.

```text
Data Consistency Models define the rules and guarantees about the order and visibility of updates across replicas. 
```

They provide a contract between the data store and the application:

```text
If you follow these rules for writing, I guarantee you'll see these behaviors when reading
```

## The Consistency Spectrum

Consistency isn't a binary "yes" or "no." It's a spectrum, ranging from very strong guarantees to much weaker ones.

### Strong consistency models

These models provide the most stringent guarantees, making the distributed system behave (from the client's perspective) much like a single, non-distributed system.

#### Strict consistency

Any read on a data item X returns the value corresponding to the most recent write on X, regardless of where the read or write occurred.

#### Linearizability (Atomic Consistency)

All operations on a data item appear to occur atomically (i.e., indivisibly) at a single point in time, in a way that respects real-time ordering.

In simple terms:

- If operation A completes before operation B begins in real time, then A must be observed before B in the system's global execution order.
- All nodes see operations in the same order, and the system behaves as if there's only one copy of the data, updated instantaneously.

**Pros**

- Easy to reason about because it mimics the behavior of local, single-threaded systems.
- Every read reflects the most recent completed write.

**Cons**

- Can be slow due to coordination required
- Can impact availability if coordination fails

**When to use**

- Critical operations where data correctness is paramount and users must always see latest value
- Example: Bank applications, distributed locks etc.

#### Sequential Consistency

All operations across all clients are observed in the same sequential order, and that this order respects the program order of operations from each individual client.

In simpler terms:

- Every process sees operations happen in a globally agreed-upon order.
- If one client performs a write(X) followed by a read(X), every other client must observe those operations in that same order.
- However, unlike linearizability, this global order does not have to align with real-time. Operations may appear reordered as long as the program order is preserved for each client.

**Pros**

- Easier to implement than linearizability
- Offers better performance and availability trade-offs.

**Cons**

- Still a relatively strong consistency model that can be complex to enforce in distributed systems.

**When to use**

- Environments where global agreement on operation order is important, but real-time alignment is not critical.
- Common scenarios include: Cache coherence protocols in shared-memory multiprocessor systems, memory models in concurrent programming environments.

### Weaker consistency models

These models relax some guarantees for better performance, availability, or scalability. They are often easier to implement but require developers to be more careful about potential stale data.

#### Casual consistency

If operation A causally precedes operation B (e.g., B reads a value written by A, or A is a reply to B), then all processes see A before B.

**Pros**

- Preserves the intended sequence of user interactions.
- More scalable and performant than stronger models like linearizability.

**Cons**

- Requires systems to track causal relationships between operations (e.g., using vector clocks or version vectors), which adds complexity.
- Doesn’t guarantee a single global order of operations.

**When to use**

- Common use cases include: Collaborative editing tools (e.g., Google Docs, Notion), Comment threads and replies on social media platforms

#### Eventual consistency

If no new updates are made to a given data item, all accesses to that item will eventually return the last updated value.

There’s no guarantee on when this convergence will happen—only that it will happen at some point in the future. In the meantime, reads may return stale or outdated values depending on which replica is accessed.

**Pros**

- High availability
- Low read latency
- Excellant scalability
- Resilient to network partitions

**Cons**

- Stale reads
- Complexity shifts to the application
- Potential for inconsistent user experience

**When to use**

- Ideal for systems where high availability and low latency are more important than immediate consistency, and temporary data discrepancies are acceptable.
- Examples: social media likes, view counts, product recommendations, DNS.

## Choosing the Right Consistency Model

**Business Needs & User Expectations**
How critical is data accuracy to the user experience or business logic?

For a banking system, users expect absolute correctness. Showing an outdated balance could lead to serious trust and financial issues.

→ Use strong consistency (e.g., linearizability).

For social media likes or view counts, temporary inconsistencies are acceptable. Seeing a slightly outdated like count for a few seconds rarely causes issues.

→ Eventual consistency is often sufficient and more efficient.

**Performance & Scalability**
Weaker consistency models (e.g., eventual or causal consistency) typically allow for faster reads/writes and easier horizontal scaling.

Strong consistency usually involves coordination overhead (e.g., consensus protocols), which can impact system throughput and response time.

### Example Scenarios

**E-commerce Inventory**

Consistency Model: Strong Consistency (e.g., Linearizability)
Why: You must prevent overselling the last item in stock. If two users attempt to purchase the last unit, only one should succeed.
Implication: Inventory updates should be synchronized and acknowledged across replicas before confirming a purchase.

**Shopping Cart**

Consistency Model: Read-your-writes or Session Consistency (within a user session); Eventual Consistency across devices
Why: Users expect their cart to reflect their own changes immediately. However, slight inconsistencies between devices can be acceptable, as long as conflicts (like unavailable items) are handled gracefully.
Implication: Use local writes with background synchronization, and detect invalid states (e.g., item out of stock) at checkout.

**User Profile Updates (e.g., Display Name or Avatar)**

Consistency Model: Read-Your-Writes for the user; Eventual Consistency for others
Why: The user should immediately see their changes. Other users can tolerate a brief delay before seeing the update.
Implication: Optimize for responsiveness in the user’s own session while syncing updates asynchronously across the system.

**Game Leaderboards**

Consistency Model: Eventual Consistency
Why: Real-time precision isn’t critical. A small delay in reflecting new scores does not significantly affect the user experience.
Implication: Use distributed caching or batched updates to improve performance while maintaining eventual convergence.
