# Exercise 2: Replica Lag & Read-Your-Writes Consistency

## Setup

You have:

- 1 Leader
- 2 Followers
- Asynchronous replication
- Replication lag ≈ 5 seconds

## Scenario

A client does the following:

- Writes: email = new@email.com
- Immediately reads the profile

Assume:

- Reads are load-balanced across followers
- No special routing yet

## Your Tasks

- 1️⃣ What can the client observe?
Explain all possible outcomes of the read.

- 2️⃣ How do you guarantee read-your-writes consistency?
Give exactly 3 approaches:

- One client-side
- One server-side
- One infrastructure / system-level

---

## Solution

In this app setup we have 1 leader, 2 followers using async replication and there is a replication lag of 5 seconds.

The clients update the email and then reads the profile. Reads are served from followers, writes are sent to the leader.

## What can the client observe ?

Well here the client can observe these things

- See the updated email address: If the user refreshes the page after 5 seconds, the user will be seeing the updated email address as the follower would have caught up the change.
- See the old email address: This can happen due to various reasons as listed below
    - If the user refreshes the page within 5 seconds, they will still see old email address. This is due to replication lag kicking in and the followers not getting the latest change.
    - User refreshes the page after 5 seconds, but his read requests is routed by the load balancer to the follower which was recovering from failure and has not yet caught up with the change.

## How do you guarantee read-your-writes consistency?

### Client Side

- The client can cache the last write timestamp and for any read requests made within a certain threshold (e.g., 5 seconds), it can directly read from the leader instead of followers. This ensures that the client always sees its own writes immediately after they are made.

Trade-offs:
- Increased latency for reads made shortly after writes, as they have to go to the leader.
- Potentially increased load on the leader if many clients implement this strategy.
- Good for scenarios where read-your-writes consistency is critical for user experience.

### Server Side

- The server can implement a session stickiness mechanism. When a client performs a write operation, the server can tag the client's session to always read from the leader for a certain duration (e.g., 1 minute) after the write. This ensures that any subsequent reads during this period will reflect the latest writes.

Trade-offs:
- Increased load on the leader due to session stickiness.
- Potentially uneven load distribution among followers.
- Will work well for applications where users frequently read their own writes shortly after making them.


### Infrastructure / System-level

- Implement a read-after-write consistency mechanism at the load balancer level. The load balancer can track recent write operations and route subsequent read requests from the same client to the leader for a short period after a write operation. This can be done by maintaining a mapping of client identifiers to their last write timestamps.

Trade-offs:
- Increased complexity in the load balancer logic.
- Potentially increased latency for reads shortly after writes.
- Better overall user experience as it is transparent to the client and server applications.