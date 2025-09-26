# Query optimization

Query optimization is the process of improving the performance of database queries by reducing execution time, minimizing resource usage, and ensuring scalability.

## Why does query optimization matter ?

- Improves Application Speed – Faster queries mean better user experience.
- Reduces Server Load – Optimized queries use fewer CPU and memory resources.
- Supports Scalability – Efficient queries allow databases to handle more users without crashes.
- Lowers Cloud Costs – Faster queries require fewer compute resources, reducing cloud bills.

## Techniques for query optimization

### Indexing

- An index is like an index in a book—it helps find data faster.
- Without an index, the database scans every row to find the match (called a Full Table Scan), which is slow.
- With an index, the database directly finds the matching row, making queries faster.

### Use Caching for Frequent Queries

- If a query runs often (like fetching homepage products), use caching (e.g., Redis)
