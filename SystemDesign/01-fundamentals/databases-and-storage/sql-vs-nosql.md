# SQL vs NoSQL

One of the biggest decisions we make while designing a system is choosing between a relational (SQL) or non-relational (NoSQL) database.

## Data model

The data model of a database defines how data is stored, organized, and related.

### SQL

- SQL databases use a relational data model where data is stored in tables
- Each table has rows representing individual records and columns representing attributes of those records.
- The primary key uniquely identifies a record, whereas a foreign key links two or more tables

### No SQL

No SQL databases use flexible non relational data models.

#### Key-Value Model (e.g., Redis)

- The key-value model is the simplest NoSQL model, where data is stored as key-value pairs. This model works well for applications that need fast lookups by a unique key.
- This model is very efficient for simple lookups, but it doesn't support complex querying or relationships between data.

#### Document model (e.g Mongo DB)

- In the document model, data is stored as documents in formats such as JSON or BSON.
- Each document contains a unique identifier (key) and a set of key-value pairs (attributes). Documents can have varying structures, making the document model schema-less or flexible.
- In this document model, each user document contains an embedded array of orders, allowing for hierarchical storage within a single document.

#### Column-Family Model (e.g., Cassandra)

- In the column-family model, data is organized into rows and columns, but unlike the relational model, each row can have a variable number of columns. It is optimized for fast querying and large-scale distributed storage.

#### Graph Model (e.g., Neo4j)

- In the graph model, data is stored as nodes, edges, and properties. This model is ideal for applications where data relationships are complex and highly interconnected (e.g., social networks).

## Schema

### SQL

- In SQL databases, the schema must be defined upfront before inserting any data.
- Each table has a specific set of columns with defined data types, constraints, and relationships. The database enforces this schema, ensuring that every row adheres to the predefined structure.
- This schema enforcement ensures data integrity, making SQL databases ideal for applications where consistency and accuracy are critical.

### NoSQL

- In NoSQL databases, there is no fixed schema that must be defined upfront.
- This allows for flexible and dynamic data structures, where different records can have different attributes.
- This flexibility makes NoSQL databases suitable for applications where data formats may evolve over time.

## Scalability

### SQL

- SQL databases are typically designed to scale vertically (also known as scale-up).
- This means improving performance and capacity by adding more power (e.g., CPU, RAM, or storage) to a single server.
- This approach works well for moderate loads but becomes limiting when the application scales to high levels of traffic or data growth.
- SQL databases rely on maintaining ACID (Atomicity, Consistency, Isolation, Durability) properties, which makes horizontal scaling challenging due to the complexity of distributed transactions and joins.

### No SQL

- NoSQL databases are designed to scale horizontally (also known as scale-out).
- This means increasing capacity by adding more servers or nodes to a distributed system.
- This distributed architecture allows NoSQL databases to handle massive volumes of data and high traffic loads more efficiently.

## Query language

### SQL

- SQL (Structured Query Language) is the de facto standard language used to interact with relational databases to perform operations such as data retrieval, insertion, update, and deletion.
- It is declarative, meaning you specify what data you want, and the database engine determines how to retrieve it.

### No SQL

- NoSQL databases do not have a standard query language. Each NoSQL database may have its query syntax or API, depending on its data model.

## Transaction support

Transactions in databases ensure that a series of operations are executed in a reliable, consistent manner.

### SQL

- SQL databases are known for their robust support of ACID transactions.
- This makes SQL databases ideal for applications where data integrity and consistency are critical, such as financial systems.

### No SQL

- NoSQL databases typically do not prioritize full ACID transactions due to the need for high availability and scalability in distributed environments.
- Instead, many NoSQL databases follow the BASE model:
  - Basically Available: The system guarantees availability, meaning that data can always be read or written, even if some nodes in the distributed system are unavailable.
  - Soft state: The system may be in a temporarily inconsistent state, but eventual consistency will be reached over time.
  - Eventually consistent: Over time, the system will become consistent, though it may not happen immediately. This trades immediate consistency for higher availability.

## Performance

### SQL

- SQL databases are optimized to handle complex queries involving multiple joins, aggregations, and transactions.
- For small datasets, SQL databases perform well, as the query optimizer can efficiently execute joins and filter data.
- As the dataset grows, performance may degrade due to the complexity of joining large tables, especially if indexing is not optimized.
- Their performance can be excellent for read-heavy applications with well-defined schemas and where data integrity is paramount.
- However, they may struggle with write-intensive operations at scale without appropriate indexing and optimization.

### No SQL

- NoSQL databases are optimized to offer high performance at scale, especially for large volumes of unstructured or semi-structured data.
- They prioritize horizontal scalability and are optimized for high-throughput read/write operations, making them ideal for real-time applications, big data, and large-scale distributed systems.
- NoSQL databases generally have faster write performance compared to SQL because:
  - Eventual consistency: In distributed NoSQL systems, data does not have to be immediately consistent across all nodes, reducing the need for locks and increasing write speed.
  - Denormalized data model: NoSQL databases often store related data together in a single document, which means fewer write operations compared to the normalized SQL model.

## Use cases

The choice between SQL and NoSQL databases often depends on the specific use case, as each type of database excels in different scenarios.

### SQL

SQL databases are ideal for applications that require:

- Structured data with predefined schemas.
- Complex queries involving joins, aggregations, and transactions.
- Strong consistency and ACID (Atomicity, Consistency, Isolation, Durability) properties.
- Relational data where relationships between tables are important.


### No SQL

NoSQL databases are ideal for use cases requiring:

- Horizontal scalability to handle large amounts of distributed data.
- High-performance reads and writes for real-time applications.
- Flexible schema to store unstructured or semi-structured data.
- Eventual consistency and high availability in distributed systems.

## Flash cards/questions to solidify

What is SQL? What is NoSQL?
Can I define each in my own words and list their main characteristics?

What are the main differences between SQL and NoSQL databases?
Think about data models, schema, scalability, consistency, and query language.

What are the strengths and weaknesses of each approach?
When is SQL preferable? When is NoSQL a better fit?

What are common use cases for SQL and NoSQL?
Can I name real-world scenarios or companies using each?

How do they handle scalability and performance?
What does vertical vs horizontal scaling mean in this context?

How do they ensure data consistency and reliability?
What trade-offs do they make (e.g., ACID vs BASE)?

What are the challenges in migrating from SQL to NoSQL or vice versa?
What would I need to consider for such a migration?

How do they support distributed systems and replication?
What mechanisms do they use for sharding, replication, and failover?

Can I explain the differences to someone else using analogies or examples?
Try to teach the concept or draw a diagram.

What interview questions could be asked about SQL vs NoSQL?
How would I answer “When would you choose NoSQL over SQL?” or vice versa?