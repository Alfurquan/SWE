## 🛒 Exercise 5: The “Always-On” Shopping Cart  
**(Leaderless Replication)**

### Context
You are designing the **Shopping Cart service** for a large e-commerce platform.

### Business Requirement
> **“Add to Cart” must never fail.**  
Even if entire datacenters are unavailable, users must always be able to add items.

### Architecture Choice
- **Leaderless Replication**
- No dedicated leader
- Any replica can accept writes

### System Configuration
- **N = 3 replicas** per shopping cart data object

---

## Your Task
Answer the following questions with a focus on the **availability vs. consistency trade-off**.

---

## A. Quorum Math (Strong Consistency)

To ensure **strong consistency** (reads always see the latest write), we typically use the quorum rule:

W + R > N


### Question
Given **N = 3**, what values would you choose for:
- **W** → Write quorum  
- **R** → Read quorum  

to guarantee strong consistency?

### L5 Check
- If **2 out of 3 replicas go offline**:
  - Can the system still **accept writes**?
  - Can the system still **serve reads**?

---

## B. Sloppy Quorum (Availability Hack)

Strict quorums can hurt availability, which conflicts with the business requirement that **“Add to Cart must never fail.”**

### Question
Explain how a **Sloppy Quorum** combined with **Hinted Handoff** allows the system to:
- Continue accepting writes
- Even when the primary **N = 3 replicas** for a cart are unreachable

### Hint
If all three “home” nodes for **User A’s cart** are down:
- Where does the write go?
- What happens once the original nodes recover?

---

## C. Handling Conflicts (Siblings)

Because the system allows **concurrent writes** on different replicas (especially during network partitions), conflicts are inevitable.

### Scenario
- Initial cart: **[Milk]**
- **Device A** connects to **Node 1** and adds **Eggs**  
  → Cart becomes **[Milk, Eggs]**
- **Device B** connects to **Node 2** and adds **Bread**  
  → Cart becomes **[Milk, Bread]**
- The network partition heals
- Node 1 and Node 2 exchange data

### Problem
The database detects a conflict and returns **both versions** of the cart (siblings).  
It cannot simply overwrite one version without losing data.

### Question
What **merge logic** should the **client application** use to combine these two cart versions into the correct final state?

---

## Answer

### A. Quorom Math

We are given N = 3, we will choose W = 2 and R = 2 as it satisfies the quorom condition W + R > N

Reasons for choice:

- Choosing R = 2 and W = 2 ensures that when reading a key after writing it, one of the replica will always have up to date value which will ensure data freshness.
- This configuration allows the system to tolerate one replica failure during writes or reads, as we can still achieve the required quorum.
- It balances read and write latencies, as both reads and writes require contacting only two replicas.

If two out of three replicas go down

- The system cannot accept writes because W = 2 requires at least two replicas to acknowledge the write.
- The system cannot serve reads because R = 2 requires at least two replicas to respond to the read request.

### B. Sloppy Quorum

Sloppy Quorum allows the system to accept writes even when the primary N = 3 replicas are unreachable by writing to alternative replicas (hints).

- When all three “home” nodes for User A’s cart are down, the write can go to any available replica in the cluster. This replica temporarily holds the write as a "hint" for the original nodes.
- Once the original nodes recover, the hinted writes are forwarded to them, ensuring that the data eventually reaches its intended replicas. This process is known as Hinted Handoff.

### C. Handling Conflicts

To merge the two cart versions into the correct final state, the client application should use a union merge logic:

- The client application should combine the items from both cart versions without losing any data. In this case, it should take the union of the two lists: [Milk, Eggs] and [Milk, Bread].
- The final merged cart should be [Milk, Eggs, Bread], ensuring that all items added by both devices are preserved.
- This approach ensures that no items are lost due to concurrent writes, and the user sees a complete view of their shopping cart.

---
