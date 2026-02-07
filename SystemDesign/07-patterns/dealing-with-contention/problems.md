# Problems 

## Exercise 1: The "High-Hype" Flash Sale

Scenario: You are designing the checkout backend for a strictly limited "flash sale" of a new gaming console.

Inventory: Exactly 500 units.

Traffic: 50,000 users will click "Buy" within the same 5-second window at 10:00 AM.

Constraint: You strictly cannot oversell (Inventory must never go below 0).

Database: You are using a standard relational database (e.g., PostgreSQL).

Your Task: Please answer the following three questions to demonstrate your mastery of the pattern:

The Strategy: Would you use Pessimistic Locking (FOR UPDATE) or Optimistic Concurrency Control (versioning) for this specific scenario? Explain your reasoning. Hint: Consider the "Retry" storm.

The Implementation: Write the pseudo-SQL or logic you would use to handle the inventory deduction safely.

The User Experience: The product manager is worried that users will put the item in their cart, spend 5 minutes entering shipping info, and then find out it’s sold out when they click "Pay". How do you use Distributed Locks (as described in the "Reservations" section of your notes) to fix this UX?

--- 

## Solution

### The Strategy

We would use Pessimistic Locking (FOR UPDATE) for this scenario. The reason is that during a flash sale with extremely high contention, the likelihood of many transactions trying to update the same inventory record simultaneously is very high. Optimistic Concurrency Control could lead to a "Retry" storm, where many transactions fail and have to retry, causing significant delays and potentially overwhelming the database. Pessimistic Locking ensures that once a transaction locks the inventory record, no other transaction can modify it until the lock is released, thus preventing overselling.

The trade off here is that pessimistic locking can lead to increased wait times for users, but in this high-contention scenario, it is more important to maintain data integrity and prevent overselling. To mitigate wait times, we can implement a queuing mechanism to manage incoming requests. This way, users are processed in a controlled manner, reducing the likelihood of long wait times.

### The Implementation

Here is the pseudo-SQL logic to handle the inventory deduction safely using Pessimistic Locking:

```sql
BEGIN TRANSACTION;
-- Lock the inventory row for update
SELECT inventory_count FROM products WHERE product_id = 'gaming_console' FOR UPDATE;

-- Check if inventory is available
IF inventory_count > 0 THEN
    -- Deduct one unit from inventory
    UPDATE products SET inventory_count = inventory_count - 1 WHERE product_id = 'gaming_console';
    COMMIT TRANSACTION;
    RETURN 'Purchase successful';
ELSE
    ROLLBACK TRANSACTION;
    RETURN 'Sold out';
END IF;
```

### The User Experience

To improve user experience, we can use redis distributed semaphore or a counter. We can use `DECR` on a redis key like `available_inventory:xbox`. If the result >= 0, the user has successfully reserved one unit. They can then go ahead and fill in the shipping info and make the payment. If they timeout or cancel, we can simply `INCR` the redis counter back.

---

## Exercise 2: The "Sharded" Money Transfer

Scenario: You are designing a banking system. The user base has grown so large that you have sharded your data.

Alice is on Shard A (Postgres Instance A).

Bob is on Shard B (Postgres Instance B).

Task: Alice sends $100 to Bob.

Your Task: The interviewer asks you to choose between Two-Phase Commit (2PC) and the Saga Pattern.

The Trade-off: Which pattern do you choose if the business requirement is "Zero Inconsistency" (Alice's balance must never appear deducted unless Bob receives it immediately)? What is the major downside of this choice regarding system availability?

The Saga Failure: You decide to use the Saga Pattern for better scalability. You successfully debit Alice (Step 1), but the credit to Bob (Step 2) fails because Bob's account is closed.

What exactly happens next? (Describe the mechanics).

What is the "temporary state" of the system called before this fix happens?

The "Phantom" Problem: In a Saga, after Alice is debited but before Bob is credited, Alice checks her balance. She sees -$100. She calls Bob, he checks his balance, he sees +$0. He claims Alice is lying. How do you solve this User Experience confusion without abandoning Sagas?

---

## Solution

### Tradeoff

If the bussiness requirement is "Zero Inconsistency", then we will need to choose Two-Phase Commit (2PC) pattern here. 2PC offers strong consistency guarantees but comes with a tradeoff woth system availability as it is fragile and complex. It includes a coordinator which handles the transaction across multiple nodes. The coordinator first sends prepare messages to the nodes to prepare the transaction and then sends commit messages to the nodes to commit the transaction. It also writes all the operations to a WAL (Write-Ahead log).

It keeps network connections open in the middle of a transaction. If the coordinator crashes in the middle of a transaction, lets say after preparation and before commit, the network connections remain open and the system remains in an unavailable state until a new coordinator comes up, reads the WAL and completes the in flight trnsaction.

### Saga failure

If we go ahead and choose Saga pattern, it gives better system availability but comes with a tradeoff that it makes the system eventually consistent. If we successfully debit Alice and fail to credit Bob, the transaction to debit Alice will be compensated back and the system will once again come back to the original state. The temporary state of the system before the compensation would be that Alice account balance will be lower than intended. This is the tradeoff with respect to eventual consistency that comes with saga pattern.

### Phantom problem

To solve the user experience in the Saga pattern, we can implement a "pending transactions" feature in the user interface. When Alice checks her balance after being debited but before Bob is credited, the system can show a notification indicating that there is a pending transaction of $100 to Bob. This way, Alice understands that the debit is not yet finalized and is part of an ongoing process. Similarly, when Bob checks his balance, the system can show a notification indicating that there is a pending credit of $100 from Alice. This approach helps manage user expectations and reduces confusion without abandoning the Saga pattern.

---

## Exercise 3: The "Celebrity" Problem (Hot Partition)

Scenario: You are designing the backend for "X" (formerly Twitter).

Feature: The "Like" button.

Normal User: When I tweet, I get ~10 likes in an hour.

The Celebrity: Taylor Swift tweets. She gets 1,000,000 likes in 1 minute.

Your Task:

The Bottleneck: You try to use the Pessimistic Locking strategy from Exercise 1 (UPDATE tweets SET likes = likes + 1 WHERE id = 'tswift'). Why does this system grind to a halt specifically for Taylor Swift, even if your database is huge? (Be specific about what resource is choked).

The Solution: The notes mention that "Sharding doesn't help" and "Read replicas don't help." The notes suggest Queue-based serialization for strong consistency.

However, for a "Like" count, we don't need strong consistency (it's okay if the count is off by a few seconds).

Propose a high-throughput solution to handle these 1M writes/minute that avoids locking the database row for every single user click.

---

## Solution

### The Bottleneck

If we go ahead with Pessimistic locking strategy for this problem, the system will grind to a halt. It will grind to a halt due to the load on the system. A single row will be locked for each request which will in turn consume lots of CPU and memory resources on the database server. The database will have to manage a large number of locks and context switches, leading to contention and delays. This will result in a bottleneck where the database cannot process requests fast enough, leading to timeouts and failures for users trying to like the tweet.

### The Solution

We can use a queue-based approach to handle the high throughput of likes. Instead of directly updating the database for each like, we can push each like event into a message queue (e.g., Kafka, RabbitMQ). A separate worker service can then consume these events from the queue and batch process them. This worker can aggregate likes for a specific tweet over a short time window (e.g., 1 second) and then perform a single database update to increment the like count by the total number of likes received in that window. This approach reduces the contention on the database row and allows the system to handle a high volume of likes efficiently.

To improve user experience, we can implement a read your write feature on the frontend. When a user likes a tweet, we can immediately update the like count on the UI optimistically, even before the database update is confirmed. This way, users see an immediate response to their action, and the eventual consistency of the like count is acceptable in this context.

---

