# Practice exercises

This section contains practice exercises to help you apply the concepts learned in the "Dealing with Contention" pattern. Each exercise presents a scenario where contention might occur, and you need to choose the appropriate strategy to handle it effectively.

## Scenario 1: eBay Auction Bidding

You're designing the bidding system for eBay. Multiple users can bid on the same item simultaneously. Each new bid must be higher than the current highest bid. During the final minutes of popular auctions, you might have hundreds of bids per second. Users should see immediate feedback if their bid succeeds or fails.

Your task: How do you handle concurrent bidding? What's your approach and why?

### Solution

**Approach**: Optimistic Concurrency Control

**Why**: Bids are frequent but conflicts (two users bidding the exact same amount at the exact same time) are rare. Optimistic concurrency allows high throughput and low latency, with retries only when necessary.

**Implementation**:

- We use bid amounts as the versioning mechanism.
- When a user places a bid, we read the current highest bid and attempt to update it with the new bid amount, ensuring it's higher than the current bid.
- If the update fails (due to a concurrent higher bid), we notify the user and prompt them to try again with a higher amount.
- We also create atomic transactions to update highest bit and creating bid history.
- This approach minimizes locking and maximizes performance during high contention periods.

```SQL
BEGIN TRANSACTION;
UPDATE auctions SET highest_bid = 150 WHERE auction_id = 'item456' AND highest_bid = 140;
INSERT INTO bid_history (auction_id, bidder, amount, timestamp) VALUES (...);
COMMIT;
```

**Edge Cases**:

- If two users bid the same amount simultaneously, one will succeed and the other will be prompted to increase their bid.
- We can implement a short delay or backoff strategy for retries to avoid overwhelming the system during peak times.
- We can also implement a notification system to inform users when they have been outbid, enhancing user experience.

**Potential Challenges**:

- Handling very high contention in the last seconds of an auction may require additional strategies, such as routing all bids for hot auction to a single queue to eliminate contention entirely.
- Ensuring data integrity and preventing fraud (e.g., fake bids) is also crucial.

### Enhanced Solution

**Approach**: Optimistic Concurrency Control + Queue for Hot Auctions

**Why Optimistic**: High bid frequency but actual conflicts (same amount, same millisecond) are rare. Better performance than pessimistic locking.

**Implementation**:

- Use current highest bid as version check
- Validate new bid > current bid + minimum increment
- Atomic update of auction + bid history creation
- Real-time bid updates to show current highest bid

**Hot Auction Handling**:

- For auctions with >100 bids/second, route to dedicated queue
- Single worker processes bids sequentially
- Eliminates contention entirely during final minutes

**Retry Strategy**:

- Exponential backoff for failed bids
- Show user current highest bid for informed retry

---

## Scenario 2: Bank Account Transfer

You're building a banking system where users can transfer money between accounts. Alice wants to transfer $500 from her checking to savings account. The system needs to ensure the money is never lost or duplicated. Your bank has grown and now shards user accounts across multiple databases based on account number.

Your task: How do you handle transfers within the same bank vs. between different banks? What coordination is needed?

### Solution

**Approach**: Different strategies based on transfer type

**Same shared**: We use simple transactions.

```sql

BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE account_id = 'alice_checking';
UPDATE accounts SET balance = balance + 500 WHERE account_id = 'alice_savings';
COMMIT;
```

**Different shards (Cross-DB)**: Saga pattern

**Different banks**: Also SAGA but with external APIs

**Why Saga**: We choose SAGA pattern as it is much robust than 2PC and we can bear slight inconsistency here. If we need very strong consistency, we can go with 2PC but it is fragile and coordinator can crash leading to issues.

**Implementation**:

- The operation is broken down into small steps which are executed and committed independently

- Step 1 - Debit $100 from Alice's account in Database A, commit immediately
- Step 2 - Credit $100 to Bob's account in Database B, commit immediately
- Step 3 - Send confirmation notifications

If Step 2 fails (Bob's account doesn't exist), you run the compensation for Step 1. You credit $100 back to Alice's account. If Step 3 fails, you compensate both Step 2 (debit Bob's account) and Step 1 (credit Alice's account). Each step is a complete, committed transaction. There are no long-running open transactions and no coordinator crashes leaving things in limbo. Each database operation succeeds or fails independently.

**Failures and challenges**:

- One challenge is that the system remains in inconsistent state for a very short amount of time. After Step 1 completes, Alice's account is debited but Bob's account isn't credited yet. Other processes might see Alice's balance as $100 lower during this window. If someone checks the total money in the system, it appears to have decreased temporarily.
- This eventual consistency is what makes sagas practical. You avoid the fragility of 2PC by accepting that the system will be briefly inconsistent. You handle this by designing your application to understand these intermediate states. For example, you might show transfers as "pending" until all steps complete.

### Enhanced solution

**Approach**: Tiered strategy based on data location

**Same Shard (Alice checking → savings)**:

- Single database transaction with pessimistic locking
- Validate sufficient funds before transfer
- Atomic debit + credit operations

**Cross-Shard (Different databases)**:

- Saga pattern for resilience
- Step 1: Debit source account (with idempotency key)
- Step 2: Credit destination account
- Step 3: Mark transfer complete
- Each step has compensation action

**Why Saga over 2PC**: Banking can tolerate brief inconsistency for better availability. Show transfers as "pending" during execution.

**Idempotency**: Each saga step uses unique transaction ID to prevent duplicate execution on retry.

**Insufficient Funds**: Validate in Step 1 before any debits occur.

---

## Scenario 3: Limited-Time Flash Sale

You're designing a flash sale system for an e-commerce platform. A popular item (iPhone) goes on sale with only 100 units available. At exactly 12:00 PM, thousands of users simultaneously try to purchase. You need to ensure exactly 100 items are sold, no more, no less.

Your task: How do you handle the inventory management and purchase coordination? What's your strategy?

### Solution

**Approach**: Queue based serialization with distributed lock having TTL

**Why**:

- Distributed lock with TTL helps locking a product unit for a user to complete the transaction so that no other user can purchase it
- For a hot flash sale, where multiple users try to purchase the same product simultaneously, keeping a queue for such a system helps process the requests from the users serially and helps prevent overselling the product. This eliminates contention entirely by making operations sequential rather than concurrent. The queue acts as a buffer that can absorb traffic spikes while the worker processes requests at a sustainable rate

**Implementation**:

- When the user goes to purchase the product, we place them in a queue that gets processed by a single worker thread.
- When the user request is being processed, we lock the unit for the user, so that no other user can purchase the same unit. We can use a distributed lock like redis with a TTL.
- Once the user request is completed and they complete the payment, the lock is released.
- If the user fails to complete the payment, and TTL expires, the lock is release and the unit is made available to other users

**Tradeoffs**:

- Queue based system helps remove contention, but increases latency for the users.  But this is often better than the alternative of having your entire system grind to a halt under the contention.

### Enhanced solution

**Approach**: Queue-Based Serialization + Distributed Locks

**Core Problem**: With 1000+ users hitting 100 items simultaneously, traditional concurrency control fails due to hot partition.

**Implementation**:

- Single queue processes all purchase requests sequentially
- Redis distributed locks with 10-minute TTL for cart reservations
- Show queue position and estimated wait time to users
- Decrement inventory optimistically when entering queue

**User Experience**:

- "You're #47 in line, estimated wait: 2 minutes"
- Lock prevents others from buying while user completes payment
- TTL automatically releases abandoned purchases

**Why This Works**: Eliminates contention entirely by serializing the bottleneck operation while maintaining fairness.

---

## Scenario 4: Meeting Room Booking

You're building a corporate meeting room booking system. Employees can book conference rooms for specific time slots. Multiple people might try to book the same room for the same time. The system should prevent double-bookings but allow users to see room availability in real-time.

Your task: How do you prevent booking conflicts while maintaining good user experience? What's your approach?
