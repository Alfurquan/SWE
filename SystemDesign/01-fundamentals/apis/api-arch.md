# What is an API ?

An API is a set of rules that allows different software systems to communicate with each other. They enable applications to request data or services from other systems without needing to know the internal details of how those systems work.

## Common API Architectural Styles

### REST

REST is one of the most popular API architectural styles. It uses standard HTTP methods (GET, POST, PUT, DELETE) to interact with resources (data objects) identified by URLs.

#### Key characteristics

- Stateless: Every API call contains all the information needed for the request. The server does not store any client context between requests.
- Resource-Based: Everything is considered a resource (e.g., users, orders, products) that can be manipulated through standard HTTP methods.
- Flexible Data Formats: Often uses JSON or XML to represent data, making it easy to parse and use across different platforms.

### GraphQL

GraphQL is a modern API query language and runtime developed by Facebook. It allows clients to request exactly the data they need, and nothing more.

#### Key Characteristics

- Flexible Queries: Clients can specify precisely what fields they need, which minimizes over-fetching or under-fetching of data.
- Single Endpoint: Unlike REST, which often has multiple endpoints for different resources, GraphQL typically operates from a single endpoint.
- Strongly Typed Schema: The API has a well-defined schema that specifies the types of data and relationships available.

### gRPC

gRPC is an open-source, high-performance remote procedure call (RPC) framework developed by Google. It uses HTTP/2 for transport, Protocol Buffers (protobuf) as the interface description language, and provides features like authentication, load balancing, and more.

#### Key Characteristics

- Efficient Binary Protocol: Uses Protocol Buffers, which are smaller and faster to serialize/deserialize than JSON or XML.
- HTTP/2 Based: Benefits from multiplexing, header compression, and improved network efficiency.
- Strongly Typed Interfaces: Enforces a strict contract between client and server via protobuf definitions.