# Choose Right Database

In system design interviews, the quality of your design and its ability to scale depends heavily on the database you choose.

Choosing the wrong database can lead to high latency, data loss, or even system downtime.

## Structured Data Requiring ACID Compliance

Consider a major online marketplace like Amazon or Flipkart, which processes millions of transactions daily.

Each order involves multiple interdependent operations:

- Selecting a product.
- Updating inventory.
- Deducting payment from the customer.
- Recording the sale for accounting and analytics.

These operations need strong consistency and ACID transactions to avoid any data anomalies or transaction failures.

- Atomicity ensures that if you fail to charge the customer’s credit card, you won’t ship the item.

- Consistency guarantees that the product count never goes negative if the system runs out of stock.

- Isolation prevents two customers from purchasing the last item at the exact same time.

- Durability ensures that once a payment is processed, you can’t lose that record if the server crashes the next second.

Recommended Database - Relational Database
When you need strict data consistency and a well-defined schema, relational databases like MySQL or PostgreSQL are often the best choice.

## Flexible Schema

A flexible schema allows you to store and manage data without the strict requirements of predefined, rigid structures (as seen in relational databases).

In a flexible schema, each record or document can have unique fields, nested data, or variable field types, making it ideal for applications where data model is highly diverse or evolves frequently.

Consider a social networking app where user profiles can vary widely:

- One user may have: three hobbies, a short bio.
- Another user may have: two hobbies, multiple addresses and favorite sports.

If you try to represent these fields in a traditional relational database, you might need several tables and constant schema changes each time you add or modify a field.

With a flexible schema, you can simply update the document structure on the fly. To achieve this, you need a database that can adapt to changing fields quickly.

Recommended Databases - Document Database

- MongoDB: Stores data in JSON-like documents, making it highly flexible and intuitive for developers. Ideal for use cases like social networks, content management systems, and e-commerce platforms.

- Couchbase: Combines flexible JSON-based document storage with high-performance key-value operations. Provides strong support for offline-first applications, with built-in synchronization features.

## Needs Caching

Caching is a powerful technique that improves application performance by storing frequently accessed data in a high-speed storage layer—typically in memory.

This allows future requests for the same data to be served much faster, bypassing the need for time-consuming queries to slower, disk-based databases or external systems..

## Searching through large textual data

Many applications require efficient searching through large volumes of text.

For Example:

- Job Platforms: Users on platforms like LinkedIn search for specific roles or keywords.

- E-commerce: Shoppers search for products based on title, description, or category.

- Content Platforms: Users browse articles, blogs, or videos using keywords and phrases.

These use cases demand robust text search capabilities, including support for ranking, relevance scoring, and fuzzy matching.

For these use cases, traditional databases like relational or NoSQL systems often fall short in performance and features.

Recommended Database - Text Search Engine

Text search engines are built to handle complex text queries efficiently and provide features like ranking and fuzzy matching.

- Elasticsearch: A distributed, open-source search and analytics engine built on top of Apache Lucene. Supports advanced features like: full-text search with relevance scoring, fuzzy matching for typo-tolerant searches and highlighting matched terms in results.

- Apache Solr: Another search engine built on Apache Lucene, known for its flexibility and scalability. Provides powerful text search capabilities, similar to Elasticsearch, but often preferred for more complex or customized use cases.

## File Storage

Many modern applications need to efficiently store and serve media files—such as images, videos, audio, or other large binary objects.

For Example:

- Streaming Platforms: Services like YouTube or Netflix store and deliver massive amounts of video content.

- Social Media: Platforms like Instagram and Facebook manage billions of user-uploaded images and videos.

- Image Hosting Services: Smaller-scale platforms also require reliable storage and fast delivery for user-uploaded content.

While traditional relational or NoSQL databases can store binary data as BLOBs (Binary Large Objects), they are not optimized for such use cases due to:

- Scalability: Storing large binary files in databases increases storage costs and complexity, especially as the data grows.

- Performance: Serving media files directly from a database introduces latency and slows down overall system performance.

- Cost: Databases often charge based on storage and throughput, making them less cost-effective for handling large files.

For these reasons, dedicated object storage solutions, often combined with Content Delivery Networks (CDNs), are the preferred approach.

## Highly Connected Data

In many systems, data isn’t just a collection of rows and columns—it’s a web of interconnected entities.

In such cases, the relationships between entities are as important as, or sometimes even more critical than, the entities themselves. This is what we call highly connected data.

For Example:

- Social Networks: Platforms like Facebook analyze relationships to suggest friends, identify communities, and calculate mutual connections or shortest paths.

- Recommendation Systems: E-commerce platforms like Amazon recommend products based on user behavior and connections between users, items, and categories.

- Knowledge Graphs: Search engines or content platforms connect concepts to deliver enriched, contextual results.

Recommended Database - Graph Database

Graph databases are purpose-built for connected data, using a structure of nodes (entities) and edges (relationships) to store and traverse data efficiently.

- Neo4j: A popular graph database optimized for storing and querying connected data. It supports Cypher, a powerful query language designed for graph traversal.

- Amazon Neptune: A fully managed graph database supporting multiple graph models, including property graphs and RDF.

## Metrics Data and Time Series

Time series data consists of sequential data points, each associated with a timestamp, representing how a system, process, or metric evolves over time.

Examples include CPU usage, request latencies, error rates, stock prices, temperature readings, or user activity logs.

These datasets often arrive at high frequencies, requiring efficient ingestion, storage, and retrieval for both real-time monitoring and historical trend analysis.

Although you can store time series data in relational databases or NoSQL solutions, it’s not always optimal.

Recommended Databases:

- Time Series Databases (TSDBs): Purpose-built for time series data, these databases provide optimized storage, indexing, and query capabilities for time-based data.

  1. InfluxDB: Designed explicitly for time series data and offers powerful query features.

  2. TimescaleDB: Built on top of PostgreSQL, TimescaleDB extends relational database capabilities with time series features.

- Wide-Column Databases: For scenarios requiring distributed scalability and high write throughput, wide-column stores can also handle time series data effectively.

    1. Apache Cassandra: Supports high-velocity writes and distributed architecture, making it suitable for time series workloads.

## Spatial Data

Spatial data refers to any data that describes a location, shape, or boundary on Earth. This typically involves storing latitude and longitude coordinates (for points) or polygons (for areas).

If your application relies on where as much as what, you'll need a database that natively supports spatial data types and queries.

For example:

- A ride-sharing service like Uber needs to find nearby drivers and calculate distances in real time.

- A food delivery service like Swiggy or Zomato must locate nearby restaurants and customers efficiently.

Handling spatial data requires specialized indexing and query functions to perform geometric calculations like distance, overlap, and adjacency.

Traditional B-tree or hash indexes aren’t optimized for multi-dimensional data. Instead, spatial data structures like R-trees, Quadtrees, and Geohashes are used to narrow down search areas efficiently.
