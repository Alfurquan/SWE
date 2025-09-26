# Sharding

Imagine a social media site like Instagram, which has over 1 billion active users.

Think about what would happen if it tried to keep all the user profile data on a single server.

Due to limited scalability of a single machine, it would quickly run out of storage space and slow down leading to performance issues.

But what if we divided the user base into smaller groups based on a key like userId and stored each group on separate servers?

Example:

- Group 1: Users with IDs 0-999
- Group 2: Users with IDs 1000-1999
- Group 3: Users with IDs 2000-2999

Distributing data in this way makes it easier to scale and manage more users.

This is the idea behind Database Sharding.

## What is Database Sharding?

Database sharding is a horizontal scaling technique used to split a large database into smaller, independent pieces called shards.
These shards are then distributed across multiple servers or nodes, each responsible for handling a specific subset of the data.

## Benefits

- Improved performance: By distributing the data across multiple nodes, sharding can significantly reduce the load on any single server, resulting in faster query execution and improved overall system performance.
- Scalability: Sharding allows databases to grow horizontally. As data volume increases, new shards can be added to spread the load evenly across the cluster.
- High Availability: With data spread across multiple shards, the failure of a single shard doesn't bring down the entire system. Other shards can continue serving requests, ensuring high availability.

## Strategies

- Hash based sharding: Data is distributed using a hash function, which maps data to a specific shard.
- Range-Based Sharding: Data is distributed based on a range of values, such as dates or numbers.
- Geo-Based Sharding: Data is distributed based on geographic location

## Best Practices for Sharding

- Choose the Right Sharding Key: Select a sharding key that ensures an even distribution of data across shards and aligns with the application's access patterns.

- Use Consistent Hashing: Implement a consistent hashing algorithm to minimize data movement when adding or removing shards.

- Monitor and Rebalance Shards: Regularly monitor shard performance and data distribution. Rebalance shards as needed to ensure optimal performance and data distribution.

- Handle Cross-Shard Queries Efficiently: Optimize queries that require data from multiple shards by using techniques like query federation or data denormalization.

