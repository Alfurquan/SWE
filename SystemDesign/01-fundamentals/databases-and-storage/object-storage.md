# Object storage

Imagine you have millions of photos, videos, and documents that need to be stored, retrieved, and managed efficiently.

As your data grows exponentially, traditional storage systems like file or block storage can become cumbersome and expensive to scale.

This is where object storage comes into play—a highly scalable, cost-effective, and resilient solution for managing large amounts of unstructured data.

## What is object storage ?

Object storage is a method of storing data as objects, rather than as files within a hierarchy or as blocks within sectors.

Each object typically includes:

- The data itself (e.g., a photo, a video, a document)
- Metadata (detailed information about the data)
- A unique identifier (which serves as its address in the storage system)

## Key characteristics

- Scalability: Easily scale out to store petabytes (or even exabytes) of data by adding more nodes to the system.
- Cost-Effectiveness: Typically runs on commodity hardware and uses efficient data distribution and replication strategies to lower costs.
- Resilience and Durability: Uses replication and error-correction techniques to ensure that data is not lost even if some nodes fail.
- Rich Metadata: Each object comes with metadata, allowing for advanced search, indexing, and management capabilities.
- Flat Namespace: Objects are stored in a flat structure, making it simpler to manage at scale compared to hierarchical file systems.

## How object storage works ?

At a high level, an object storage system consists of multiple storage nodes that are organized in a distributed manner.

- Client Request: Clients interact with the storage system via APIs (often RESTful APIs) to store or retrieve objects.
- API Layer: The API layer handles requests, manages authentication, and routes operations to the appropriate storage nodes.
- Storage Nodes: Data is stored across multiple nodes in a distributed fashion. Each node is responsible for a portion of the overall data.
