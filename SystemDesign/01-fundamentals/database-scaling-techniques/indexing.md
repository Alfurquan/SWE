# Indexing

Database index guide the database to the exact location of the data, enabling faster and more efficient data retrieval.

## What are Database Indexes ?

A database index is a super-efficient lookup table that allows a database to find data much faster.
It holds the indexed column values along with pointers to the corresponding rows in the table.
Without an index, the database might have to scan every single row in a massive table to find what you want – a painfully slow process.
But, with an index, the database can zero in on the exact location of the desired data using the index’s pointers.

## Types of Database Indexes

- Primary index: Automatically created when a primary key constraint is defined on a table.
- Clustered index: Determines the order in which data is physically stored in the table. A clustered index is most useful when we’re searching in a range. Only one clustered index can exist per table.
- Non-clustered or Secondary Index: This index does not store data in the order of the index. Instead, it provides a list of virtual pointers or references to the location where the data is actually stored.

## How to use Database Indexes Smartly?

- Identify Query Patterns: Analyze the most frequent and critical queries executed against your database to determine which columns to index and which type of index to use.

- Index Frequently Used Columns: Consider indexing columns that are frequently used in WHERE, JOIN, and ORDER BY clauses.

- Index Selective Columns: Indexes are most effective on columns with a good spread of data values (high cardinality). Indexing a gender column might be less beneficial than one with a unique customer_id.

- Use Appropriate Index Types: Choose the right index type for your data and queries.

- Consider Composite Indexes: For queries involving multiple columns, consider creating composite indexes that encompass all relevant columns. This reduces the need for multiple single-column indexes and improves query performance.

- Monitor Index Performance: Regularly monitor index performance, remove unused indexes and adjust your indexing strategy as the database workload evolves.

- Avoid Over-Indexing: Avoid creating too many indexes, as this can lead to increased storage requirements and slower write performance. Indexes take up extra disk space since they're additional data structures that need to be stored alongside your tables. Every time you insert, update, or delete data in a table with an index, the index needs to update too. This can slightly slow down write operations.