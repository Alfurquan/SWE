# 🔒 Dealing with Contention Pattern - Cheatsheet

## 🎯 The Core Problem

When multiple processes compete for the same resource simultaneously (concert tickets, auction bids, bank transfers), you get **race conditions, double-bookings, and inconsistent state** without proper coordination.

---

## 🔧 The Solution Progression

### Single Database Solutions

- 🟢 **Atomicity (Start Here!)**
  - Group operations in transactions (`BEGIN → operations → COMMIT`)
  - Either all succeed or all fail together
  - **Use when:** Multiple related operations need to happen together  
  - 💡 *L5 Tip:* Always mention atomicity first - shows you understand basics  

- 🟡 **Pessimistic Locking (High Contention)**
  
  ```sql
    SELECT * FROM concerts WHERE id = 123 FOR UPDATE;
    UPDATE concerts SET seats = seats - 1 WHERE id = 123;
   ```
  
  - Lock resources upfront, prevent conflicts before they happen  
  - **Use when:** High contention, conflicts are likely  
  - **Trade-off:** Blocks other transactions, can cause deadlocks  

- 🟠 **Optimistic Concurrency Control (Low Contention)**

    ```sql
        -- Use version or existing data as "version"
        UPDATE concerts SET seats = seats - 1, version = version + 1 
        WHERE id = 123 AND version = 42;
     ```
  
  - Assume conflicts are rare, detect them when they happen  
  - **Use when:** Low contention, performance matters  
  - **Trade-off:** Need retry logic, wasted work on conflicts  

---

### Multiple Database Solutions

- 🔴 **Two-Phase Commit (2PC) - Strong Consistency**
  - Phase 1: Ask all databases to "prepare"  
  - Phase 2: Tell all to "commit" or "abort"  
  - **Use when:** Must have atomicity across systems  
  - ⚠️ **Warning:** Complex, fragile, coordinator can crash  

- 🟣 **Saga Pattern - Resilience**
  - Break operation into independent steps  
  - Each step can be "compensated" (undone) if later steps fail  
  - **Use when:** Cross-database operations, can tolerate brief inconsistency  
  - **Trade-off:** Temporary inconsistency, more complex logic  

- 🔵 **Distributed Locks - User Experience**
  - Reserve resources temporarily (Redis TTL, DB status columns)  
  - Prevent users from entering contention scenarios  
  - **Use when:** User-facing flows, want to avoid conflicts  
  - **Example:** Ticketmaster seat reservations  

---

## 🚀 Quick Decision Tree

- Single database? → Use **pessimistic locking** (high contention) or **optimistic concurrency** (low contention)  
- Multiple databases + must be atomic? → **2PC (if you must)** or **Saga pattern (preferred)**  
- User experience matters? → **Distributed locks with reservations**  
- High contention on one resource? → **Queue-based serialization**  

---

## 💡 L5 Interview Tips

- ✅ **Start Simple:** Always mention single-database solutions first  
- ❓ **Question Requirements:** "How often do conflicts happen? Can we tolerate brief inconsistency?"  
- ⚖️ **Show Trade-offs:** "Pessimistic locking is safer but blocks users; optimistic is faster but needs retries"  
- 🚫 **Avoid Over-engineering:** Don't jump to distributed solutions if a single DB works  

---

## 🎪 Common Scenarios

- 🎟️ **Concert Tickets:** Optimistic concurrency with seat count as version  
- 🏦 **Bank Transfers:** Pessimistic locking (same bank) or Saga pattern (different banks)  
- 🔨 **Auction Bidding:** Optimistic concurrency with current bid as version  
- 📦 **Inventory Systems:** Distributed locks for cart reservations + optimistic for final purchase  

---

## 🔥 Deep Dive Prep

- 🔁 **Deadlock Prevention:** Always acquire locks in consistent order (user ID, etc.)  
- 🧑‍💻 **2PC Coordinator Crash:** Need persistent logs and failover coordinator  
- 🔄 **ABA Problem:** Use monotonically increasing columns (counts, timestamps)  
- 🎉 **Hot Partition:** Queue-based serialization for celebrity problems  

---

## 🎯 The L5 Approach

1. Identify the contention early in your design  
2. Start with single-database solutions (**atomicity + locking**)  
3. Only go distributed if truly needed (and justify why)  
4. Consider user experience (**reservations prevent conflicts**)  
5. Address failure scenarios when asked about edge cases  

👉 **Remember:** Most contention problems can be solved within a single database.  
Only reach for distributed coordination when you absolutely need **cross-system atomicity**!
