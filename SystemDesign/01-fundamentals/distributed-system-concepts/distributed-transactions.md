# Distributed transactions

A distributed transaction is a transaction that spans multiple, physically or logically separate databases or systems. Unlike a traditional transaction confined to a single system, a distributed transaction ensures that a set of operations across different systems either all succeed (commit) or all fail (rollback), maintaining data consistency.

Imagine you’re at a busy restaurant that uses separate systems for orders, payments, and kitchen operations. A distributed transaction would ensure that when a customer places an order, the order is recorded, the payment is processed, and the kitchen is notified—all together.

If one part fails (say, the payment system), the entire transaction is canceled, preventing a scenario where the order is taken but payment isn’t processed.

## Why Do We Need Distributed Transactions?

Distributed transactions are critical because they:

- Maintain Consistency: They ensure that all parts of a transaction are completed successfully, keeping the system in a consistent state.
- Prevent Partial Failures: By committing or rolling back all related operations together, they avoid scenarios where some systems are updated while others are not.
- Support Business Integrity: For processes like financial transactions, order processing, or inventory management, distributed transactions guarantee that business rules are followed correctly across the board.
