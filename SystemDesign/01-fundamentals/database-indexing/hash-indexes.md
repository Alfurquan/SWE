# Hash Indexes

While B-trees dominate the indexing landscape, hash indexes serve a specialized purpose: they excel at exact-match queries. They're simply a persistent hashmap implementation, trading flexibility for super-fast O(1) lookups.

## How Hash Indexes Work

At their core, hash indexes are just a hashmap that maps indexed values to row locations. The database maintains an array of buckets, where each bucket can store multiple key-location pairs. When indexing a value, the database hashes it to determine which bucket should store the pointer to the row data.

For example, with a hash index on email:

```text
buckets[hash("alice@example.com")] -> [ptr to page 1]
buckets[hash("bob@example.com")]   -> [ptr to page 2]
```

Hash collisions are handled through linear probing - when a collision occurs, the database simply checks the next bucket until it finds an empty spot. While this means worst-case lookups can degrade to O(n), with a good hash function and load factor, we typically achieve O(1).

This structure makes hash indexes incredibly fast for exact-match queries - just compute the hash, go to the bucket, and follow the pointer. However, this same structure makes them useless for range queries or sorting since similar values are deliberately scattered across different buckets.

## Real World Usage

Despite their speed for exact matches, hash indexes are relatively rare in practice. PostgreSQL supports them but doesn't use them by default because B-trees perform nearly as well for exact matches while supporting range queries and sorting. As the PostgreSQL documentation notes, "B-trees can handle equality comparisons almost as efficiently as hash indexes."

---