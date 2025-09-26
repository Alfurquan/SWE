# ACID

Imagine you’re running an e-commerce application.

A customer places an order, and your system needs to deduct the item from inventory, charge the customer’s credit card, and record the sale in your accounting system—all at once.

What happens if the payment fails but your inventory count has already been reduced? Or if your application crashes halfway through the process?

This is where ACID transactions come into play. They ensure that all the steps in such critical operations happen reliably and consistently.

ACID is an acronym that refers to the set of 4 key properties that define a transaction: Atomicity, Consistency, Isolation, and Durability.

## What is a Database Transaction?

A transaction in the context of databases is a sequence of one or more operations (such as inserting, updating, or deleting records) that the database treats as one single action. It either fully succeeds or fully fails, with no in-between states.

Example: Bank transfer

When you send money to a friend, two things happen:

- Money is deducted from your account
- Money is added to their account

These two steps form one transaction. If either steps fail, both are cancelled.

Without transactions, databases could end up in inconsistent states.

For example:

- Partial updates: Your money is deducted, but your friend never received it.
- Conflicts: Two people booking the last movie ticket at the same time.

Transactions solve these problems by enforcing rules like ACID properties (Atomicity, Consistency, Isolation, Durability).

## Atomicity

Atomicity ensures that a transaction - comprising of multiple operations - executes as a single and indivisible unit of work. It either fully succeeds or fully fails.

If any part of the transaction fails, the entire transaction is rolled back and the database is restored to the state it was before the transaction

### How database implement atomicity ?

Database use two mechanism

- Transaction logs (Write ahead logs)
  
1. Every operation is recorded in a write ahead log before it is applied to the database table.
2. If a failure occurs, the database uses this log to undo incomplete changes

```text
[TRANSACTION LOG ENTRY]

Transaction ID: 12345
Actions to perform:
1) UPDATE accounts
   SET balance = balance - 100
   WHERE account_id = 1

2) UPDATE accounts
   SET balance = balance + 100
   WHERE account_id = 2
```

When the operation succeeds

- The database marks transaction as committed in transaction log.
- The new changes get flushed from memory to disk

If the database crashes after the log entry is written but before the data files are fully updated, the WAL provides a way to recover:

On restart, the database checks the WAL.

- It sees Transaction 12345 was committed.
- It reapplies the UPDATE operations to ensure the final balances are correct in the data files.

If the transaction had not committed (or was marked as “in progress”) at the time of the crash, the database would roll back those changes using information in the log, leaving the table as if the transaction never happened.

- Commit/Rollback Protocols

1. Databases provide commands like BEGIN TRANSACTION, COMMIT, and ROLLBACK
2. Any changes made between BEGIN TRANSACTION and COMMIT are considered “in-progress” and won’t be permanently applied unless the transaction commits successfully.
3. If any step fails, or if you explicitly issue a ROLLBACK, all changes since the start of the transaction are undone.

```SQL
-- Begin a transaction
BEGIN TRANSACTION;

-- Step 1: Update the user's profile
UPDATE users
SET username = 'newUsername'
WHERE user_id = 123;

-- Step 2: Insert a log entry
INSERT INTO user_logs (user_id, action, timestamp)
VALUES (123, 'Updated username', NOW());

-- If everything went well, COMMIT the transaction
COMMIT;

-- If an error happens between BEGIN TRANSACTION and COMMIT,
-- we manually or automatically ROLLBACK to undo partial changes.
```

## Consistency

Consistency in the context of ACID transactions ensures that any transaction will bring the database from one valid state to another valid state—never leaving it in a broken or “invalid” state.

**Example**

You have two tables in an e-commerce database

- products (with columns: product_id, stock_quantity, etc.)
- orders  (with columns: order_id, product_id, quantity, etc.)

Constraint: You can’t place an order for a product if quantity is greater than the stock_quantity in the products table.

```SQL
BEGIN TRANSACTION;

INSERT INTO orders (product_id, quantity)
VALUES (101, 10);

-- Next, try to decrement stock from the products table
UPDATE products
SET stock_quantity = stock_quantity - 10
WHERE product_id = 101;

-- Check constraint: If 'stock_quantity' goes below 0, this violates the rule.

COMMIT;
```

- If the product’s stock_quantity was 8 (less than what we’re trying to order), the database sees that the new value would be -2 which breaks the consistency rule (it should not go negative).

- The transaction fails or triggers a rollback, preventing the database from ending in an invalid state.

### How database implement consistency ?

- Database schema constrains
NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK constraints, and other schema definitions ensure no invalid entries are allowed.

- Triggers and Stored Procedures

1. Triggers can automatically check additional rules whenever rows are inserted, updated, or deleted.
2. Stored procedures can contain logic to validate data before committing.

## Isolation

Isolation ensures that concurrently running transactions do not interfere with each other’s intermediate states.

Essentially, while a transaction is in progress, its updates (or intermediate data) remain invisible to other ongoing transactions—giving the illusion that each transaction is running sequentially, one at a time.

Without isolation, two or more transactions could read and write partial or uncommitted data from each other, causing incorrect or inconsistent results.

### Concurrency anomalies

1. Dirty read

- Transaction A reads data that Transaction B has modified but not yet committed.
- If Transaction B then rolls back, Transaction A ends up holding an invalid or “dirty” value that never truly existed in the committed state.

2. Non repeatable read

- Transaction A reads the same row(s) multiple times during its execution but sees different data because another transaction updated or deleted those rows in between A’s reads.

3. Phantom Read

- Transaction A performs a query that returns a set of rows. Another transaction inserts, updates, or deletes rows that match A’s query conditions.
- If A re-runs the same query, it sees a different set of rows (“phantoms”).

### Isolation levels

Databases typically allow you to choose an isolation level, which balances data correctness with performance.

Higher isolation levels provide stronger data consistency but can reduce system performance by increasing the wait times for transactions.

1. Read Uncommitted

- Allows dirty reads; transactions can see uncommitted changes.
- Rarely used, as it can lead to several anomalies

2. Read Committed

- A transaction sees only data that has been committed at the moment of reading.
- Prevents dirty read, but non repeatable and phantom reads can occur.

3. Repeatable Read

- Ensures if you read the same rows multiple times within a transaction, you’ll get the same values (unless you explicitly modify them).
- Prevents dirty reads and non-repeatable reads, but phantom reads may still happen (depending on the database engine).

4. Serializable

- The highest level of isolation, acting as if all transactions happen sequentially one at a time.
- Prevents dirty reads, non-repeatable reads, and phantom reads.
- Most expensive in terms of performance and concurrency because it can require more locking or more conflict checks.

### How Databases Enforce Isolation

1. Locking

- Rows or tables are locked so that no other transaction can read or write them until the lock is released.
- Can lead to blocking or deadlocks if multiple transactions compete for the same locks.

2. MVCC (Multi-Version Concurrency Control)

- Instead of blocking reads, the database keeps multiple versions of a row.
- Readers see a consistent snapshot of data (like a point-in-time view), while writers create a new version of the row when updating.
- This approach reduces lock contention but requires carefully managing row versions and cleanup (vacuuming in PostgreSQL, for example).

3. Snapshot Isolation

- A form of MVCC where each transaction sees data as it was at the start (or a consistent point) of the transaction.
- Prevents non-repeatable reads and dirty reads. Phantom reads may still occur unless the isolation level is fully serializable.

## Durability

Durability ensures that once a transaction has been committed, the changes it made will survive, even in the face of power failures, crashes, or other catastrophic events.

### How Databases Ensure Durability

1. Transaction Logs (Write-Ahead Logging)

Most relational databases rely on a Write-Ahead Log (WAL) to preserve changes before they’re written to the main data files:

- Write Changes to WAL: The intended operations (updates, inserts, deletes) are recorded in the WAL on durable storage (disk).
- Commit the Transaction: Once the WAL entry is safely persisted, the database can mark the transaction as committed.
- Apply Changes to Main Data Files: The updated data eventually gets written to the main files—possibly first in memory, then flushed to disk.

2. Replication / Redundancy

In addition to WAL, many systems use replication to ensure data remains durable even if hardware or an entire data center fails.

- Synchronous Replication: Writes are immediately copied to multiple nodes or data centers. A transaction is marked committed only if the primary and at least one replica confirm it’s safely stored.

- Asynchronous Replication: Changes eventually sync to other nodes, but there is a (small) window where data loss can occur if the primary fails before the replica is updated.

## Flashcards/Notes

1. What does each ACID property mean?

- Atomicity: Atomicity ensures that each transaction is executed as a single indivisible unit of work meaning all the operations constituting a transaction are executed as a whole and all of them either succeed or none of them. There is no partial success/failure

- Consistency: Consistency ensures that each transaction takes a database from one consistent state to another.

- Isolation: Isolation ensures that no transaction uncommitted state gets read or accessed by another transaction.

- Durability: Durability ensures that once a transaction is committed, the changes are persisted despite network failures, errors or crashes.

2. Why is each property important?

- Atomicity is important so that the database is not left in a intermediate state. Lets say we are transferring money from account A to account B. If lets say in the middle of the transaction, database crashes, we need to make sure that database is not left in an intermediate state, for e.g. money deducted from account A but not credited to account B.

- Consistency is important so that database is not left in an inconsistent state. For e.g if we have a product and orders table and if we order a product with a quantity greater than its stock, then the transaction will update the stock with a negative value. If we do not have consistency, then database will go into these inconsistent state.

- Isolation is important to make sure that none of the transaction read uncommitted or intermediate state of another transaction. If there is no isolation, the transactions can read/access each other intermediate results leading to ambiguous behavior. Say for e.g. a Transaction B updates value of x from 3 to 5. At the same time another transaction A reads value of x, B crashes before committing the transaction is committed. As a result A will have a dirty read of x. 

- Durability is important to make sure once a transaction is committed, the changes are persisted despite network failures, errors or crashes. If no durability, data will get lost in case of network failures and crashes

3. How does a database guarantee each property?

- Atomicity: Write ahead logs, Begin transaction, rollback and commit commands
- Consistency: Checks on values, primary key and foreign key constraints, triggers and stored procedures
- Isolation: Locks, MVCC, snapshot isolation
- Durability: Replication, Write ahead logs, backups

4. Can I think of real-world scenarios?

Many some of them are

- Movie ticket booking
- Ecommerce shopping
- Credit card transactions

5. How do different databases implement ACID?

Not sure now, will need to dig deep.

6. What are the trade-offs?

Not able to figure out now from the reading of article

7. How do ACID properties relate to distributed systems?

Not able to figure out now

8. Can I explain ACID to someone else?

yes, using my notes and understanding
