# DynamoDB

DynamoDB is a fully-managed, highly scalable, key-value service provided by AWS. Cool, buzz-words. But what the hell does that mean and why does it matter?

- Fully Managed: This means that AWS takes care of all the operational aspects of the database. The fully-managed nature allows AWS to handle all operational tasks — hardware provisioning, configuration, patching, and scaling — freeing developers to concentrate on application development

- Highly Scalable - DynamoDB can handle massive amounts of data and traffic. It automatically scales up or down to adjust to your application's needs, without any downtime or performance degradation.

- Key-value - DynamoDB is a NoSQL database, which means it doesn't use the traditional relational database model. Instead, it uses a key-value model that allows for flexible data storage and retrieval.

The moral of the story is that DynamoDB is a super easy to use and can scale to support a wide variety of applications. For system design interviews in particular, it has just about everything you'd ever need from a database. It even supports transactions now! Which neutralizes one of the biggest criticisms of DynamoDB in the past.

## The Data Model

In DynamoDB, data is organized into tables, where each table has multiple items that represent individual records. This is just like a relational database, but with some distinct differences tailored for scalability and flexibility.

- Tables - Serve as the top-level data structure in DynamoDB, each defined by a mandatory primary key that uniquely identifies its items. Tables support secondary indexes, enabling queries on non-primary key attributes for more versatile data retrieval.

- Items - Correspond to rows in a relational database and contain a collection of attributes. Each item must have a primary key and can contain up to 400KB of data, including all its attributes.

- Attributes - Key-value pairs that constitute the data within an item. They can vary in type, including scalar types (strings, numbers, booleans) and set types (string sets, number sets). Attributes can also be nested, allowing for complex data structures within a single item.

Consider a users table in DynamoDB, structured as follows:

```json
{
  "PersonID": 101,
  "LastName": "Smith",
  "FirstName": "Fred",
  "Phone": "555-4321"
},
{
  "PersonID": 102,
  "LastName": "Jones",
  "FirstName": "Mary",
  "Address": {
    "Street": "123 Main",
    "City": "Anytown",
    "State": "OH",
    "ZIPCode": 12345
  }
},
{
  "PersonID": 103,
  "LastName": "Stephens",
  "FirstName": "Howard",
  "Address": {
    "Street": "123 Main",
    "City": "London",
    "PostalCode": "ER3 5K8"
  },
  "FavoriteColor": "Blue"
}
```

Each item represents a user with various attributes. Notice how some users have attributes not shared by others, like FavoriteColor, showing DynamoDB's flexibility in attribute management.

### Partition Key and Sort Key

DynamoDB tables are defined by a primary key, which can consist of one or two attributes:

- Partition Key - A single attribute that, along with the sort key (if present), uniquely identifies each item in the table. DynamoDB uses the partition key's value to determine the physical location of the item within the database. This value is hashed to determine the partition where the item is stored.

- Sort Key (Optional) - An additional attribute that, when combined with the partition key, forms a composite primary key. The sort key is used to order items with the same partition key value, enabling efficient range queries and sorting within a partition.

In an interview, you'll want to be sure to specify the partition key and, optionally, a sort key when introducing DynamoDB. This choice is important for optimizing query performance and data retrieval efficiency. Just like with any other database, you'll choose a partition key that optimizes for the most common query patterns in your application and keeping data evenly distributed across partitions. In the case you need to perform range queries or sorting, you'll want to also specify the Sort Key.

For example, if you're building a simple group chat application, it would make sense to use the chat_id as the partition key and message_id as the sort key. This way, you can efficiently query all messages for a specific chat group and sort them chronologically before displaying them to users.

Notice we're using a monotonically increasing message_id rather than a timestamp as the sort key. While timestamps might seem intuitive for sorting messages, they don't guarantee uniqueness - multiple messages could be created in the same millisecond. A monotonically increasing ID (like an auto-incrementing number or a UUID v1) provides both chronological ordering and uniqueness. The ID can be generated using techniques like:

- Auto-incrementing counters per partition
- Timestamp-based UUIDs (UUID v1)
- Snowflake IDs
- ULID

#### But what is actually happening under the hood?

DynamoDB uses a combination of consistent hashing and B-trees to efficiently manage data distribution and retrieval:

- Consistent Hashing for Partition Keys: The physical location of the data is determined by the partition key. We hash this key using consistent hashing to find which node in the DynamoDB cluster will store the item. This ensures data is evenly distributed across the cluster.

- B-trees for Sort Keys: Within each partition, DynamoDB organizes items in a B-tree data structure indexed by the sort key. This enables efficient range queries and sorted retrieval of data within a partition.

- Composite Key Operations: When querying with both keys, DynamoDB first uses the partition key's hash to find the right node, then uses the sort key to traverse the B-tree and find the specific items.

This two-tier approach allows DynamoDB to achieve both horizontal scalability (through partitioning) and efficient querying within partitions (through B-tree indexing). It's this combination that enables DynamoDB to handle massive amounts of data while still providing fast, predictable performance for queries using both partition and sort keys.

### Secondary Indexes

But what if you need to query your data by an attribute that isn't the partition key? This is where secondary indexes come in. DynamoDB supports two types of secondary indexes:

- Global Secondary Index (GSI) - An index with a partition key and optional sort key that differs from the table's partition key. GSIs allow you to query items based on attributes other than the table's partition key. Since GSIs use a different partition key, the data is stored on entirely different physical partitions from the base table and is replicated separately.

- Local Secondary Index (LSI) - An index with the same partition key as the table's primary key but a different sort key. LSIs enable range queries and sorting within a partition. Since LSIs use the same partition key as the base table, they are stored on the same physical partitions as the items they're indexing.

Understanding the physical storage difference between GSIs and LSIs is important. GSIs maintain their own separate partitions and replicas, which allows for greater query flexibility but requires additional storage and processing overhead. LSIs, on the other hand, are stored locally with the base table items, making them more efficient for queries within a partition but limiting their flexibility.

You'll want to introduce a GSI in situations where you need to query data efficiently by an attribute that isn't the partition key. For example, if you have a chat table with messages for your chat application, then your main table's partition key would likely be chat_id with a sort key on message_id. This way, you can easily get all messages for a given chat sorted by time. But what if you want to show users all the messages they've sent across all chats? Now you'd need a GSI with a partition key of user_id and a sort key of message_id.

LSIs are useful when you need to perform range queries or sorting within a partition on a different attribute than the sort key. Going back to our chat application, we already can sort by message_id within a chat group, but what if we want to query messages with the most attachments within a chat group? We could create an LSI on the num_attachments attribute to facilitate those queries and quickly find messages with many attachments.

| Feature | Global Secondary Index (GSI) | Local Secondary Index (LSI) |
|----------|------------------------------|------------------------------|
| **Definition** | Index with a different partition key than the main table | Index with the same partition key as the main table but a different sort key |
| **When to Use** | When you need to query on attributes that are not part of the primary key | When you need additional sort keys for querying within the same partition key |
| **Size Restrictions** | No size restrictions on items in the index | Limited to 10 GB per partition key |
| **Throughput** | Separate read/write capacity units from the base table | Shares the read/write capacity units of the base table |
| **Consistency** | Eventually consistent only | Supports both eventually consistent (default) and strongly consistent reads |
| **Deletion** | Deleting a GSI does not affect the base table items | Deleting an LSI is not possible without deleting the base table |
| **Maximum Count** | Up to 20 GSIs per table | Up to 5 LSIs per table |
| **Use Case Examples** | Use GSI for global search across all partitions, such as searching by email in a user database | Use LSI for local search within partitions, such as finding recent orders within a customer partition |


### Accessing Data

There are two primary ways to access data in DynamoDB: Scan and Query operations.

- Scan Operation - Reads every item in a table or index and returns the results in a paginated response. Scans are useful when you need to read all items in a table or index, but they are inefficient for large datasets due to the need to read every item and should be avoided if possible.

- Query Operation - Retrieves items based on the primary key or secondary index key attributes. Queries are more efficient than scans, as they only read items that match the specified key conditions. Queries can also be used to perform range queries on the sort key.

When working with Dynamo, you typically want to avoid expensive scan operations where ever possible. This is where careful data modeling comes into play. By choosing the right partition key and sort key, you can ensure that your queries are efficient and performant.

## CAP Theorem

You'll typically make some early decisions about consistency and availability during the non-functional requirements phase of your interview. As such, it's important that you choose a database that aligns with those requirements.

Most candidates choose DynamoDB when they need high availability and scalability. This isn't wrong, but just like the traditional SQL vs NoSQL debate, it's outdated.

DynamoDB can be configured to support two different consistency models: eventual consistency and strong consistency.

- Eventual Consistency - This is the default consistency model in DynamoDB. It provides the highest availability and lowest latency, but it can result in stale reads. This means that if you write data and then immediately read it, you might not see the updated data right away. With this configuration, Dynamo is a AP system displaying BASE properties.

- Strong Consistency - This model ensures that all reads reflect the most recent write. This comes at the cost of higher latency and potentially lower availability. With this configuration, Dynamo is an CP system displaying ACID properties.

Again, this is just a simple configuration change in the AWS console or via the SDK and means that you can use DynamoDB in a wide variety of scenarios, including those where strong consistency is required like in a banking application or ticket booking system.

### But what is actually happening under the hood?

DynamoDB's consistency models are implemented through its distributed architecture and replication mechanisms:

#### Eventually Consistent Reads (Default)

- Write operations are first written to a primary replica and then asynchronously replicated to secondary replicas
- Reads may be served by any replica, which might not have the latest update yet
- Background processes continuously synchronize data across replicas
- Consumes less read capacity (0.5 RCU per 4KB) and provides lower latency

#### Strongly Consistent Reads

- Strongly consistent reads are routed directly to the leader node for the partition
- The leader ensures it has the most up-to-date data before responding
- Consumes more read capacity (1 RCU per 4KB) and may have higher latency
- Provides the most recent version of data that reflects all successful writes

## Architecture and Scalability

### Scalability

DynamoDB scales through auto-sharding and load balancing. When a server reaches capacity, data is automatically redistributed. Consistent hashing ensures even distribution across nodes, balancing traffic and load.

### Fault Tolerance and Availability

DynamoDB is designed to provide high availability and fault tolerance through its distributed architecture and data replication mechanisms. The service automatically replicates data across multiple Availability Zones within a region, so that data is durable and accessible even in the event of hardware failures or network disruptions.

Under the hood, DynamoDB utilizes a quorum-based replication system to ensure both data consistency and durability. Write operations require acknowledgment from a majority of replicas before being considered successful . For strongly consistent reads, DynamoDB routes the request to the primary replica, guaranteeing the most up-to-date data. However, in eventual consistency mode, reads can be served from any replica, which might result in slightly outdated information due to the asynchronous nature of replication .

## DynamoDB in an Interview

### When to use It

In interviews, you can often justify using DynamoDB for almost any persistence layer needs. It's highly scalable, durable, supports transactions, and offers sub-millisecond latencies. Additional features like DAX for caching and DynamoDB Streams for cross-store consistency make it even more powerful. So if your interviewer allows, its probably a great option.
However, it's important to know when not to use DynamoDB because of its specific downsides.

### Knowing its limitations

There are a few reasons why you may opt for a different database (beyond just generally having more familiarity with another technology):

- Cost Efficiency: DynamoDB's pricing model is based on read and write operations plus stored data, which can get expensive with high-volume workloads. If you need hundreds of thousands of writes per second, the cost might outweigh the benefits.

- Complex Query Patterns: If your system requires complex queries, such as those needing joins or multi-table transactions, DynamoDB might not cut it. It's great for basic queries but struggles with more intricate operations.

- Data Modeling Constraints: DynamoDB demands careful data modeling to perform well, optimized for key-value and document structures. If you find yourself frequently using Global Secondary Indexes (GSIs) and Local Secondary Indexes (LSIs), a relational database like PostgreSQL might be a better fit.

- Vendor Lock-in: Choosing DynamoDB means locking into AWS. Many interviewers will want you to stay vendor-neutral, so you may need to consider open-source alternatives to avoid being tied down.

---