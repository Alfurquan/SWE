# Exercise: Leaderless Replication (Quorum Reasoning)

## Scenario

You are designing a Key-Value Store using leaderless replication (Dynamo-style).

System parameters:

- N = 3 replicas per key
- Writes go to all replicas
- Reads can go to any replicas
- Network partitions and node failures can occur

## Your Tasks

1️⃣ Choose quorum values

Pick values for:

- W (write quorum)
- R (read quorum)

Explain why in 2–3 bullets.

2️⃣ What consistency does this guarantee?

Explain:

- What consistency guarantee you get with your chosen R and W
- What it does not guarantee

(Be precise—no CAP buzzwords.)

3️⃣ What happens during a failure?

Answer one of the following:

- A replica is down during a write
- A replica returns stale data during a read

Explain how the system detects and repairs it.

---

## Solution

Here in this problem, we are designing a key value store using leaderless replication. We have N = 3 replicas per key, with writes going to all replicas. Reads can happen from any replica.

### Quorom Values

For Quorom we will choose R = 2 and W = 2 as it will satisy the equation => R + W > N.

Reason for choosing the values

- Choosing R = 2 and W = 2 ensures that when reading a key after writing it, one of the replica will always have up to date value which will ensure data freshness.
- This configuration allows the system to tolerate one replica failure during writes or reads, as we can still achieve the required quorum.
- It balances read and write latencies, as both reads and writes require contacting only two replicas.

### Consistency Guarantee

With R = 2 and W = 2, we get the following consistency guarantees:

- Read-after-write consistency: After a successful write, any subsequent read will return the most recent value, as at least one of the two replicas read will have the latest write.
- Eventual consistency: In the absence of new writes, all replicas will eventually converge to the same value.

However, it does not guarantee:
- Strong consistency: There may be scenarios where concurrent writes lead to conflicts, and without a conflict resolution mechanism, different replicas may hold different values temporarily.

### Handling Failures

- A replica is down during writes: If a replica is down during writes, since we have choose R = 2 and W = 2, we can tolerate one replica failure on writes as we will reach the required quorom, when the replica comes back up, when the same key is read, the other replicas will return updated value and the replica which was down will then get the updated value (This is called Read repair).

- A replica returns stale data during a read: When a replica returns a stale data during a read, the other the other replicas will return updated values, then system will update the replica which sends stale value with the updated value (This is called Read repair).

---