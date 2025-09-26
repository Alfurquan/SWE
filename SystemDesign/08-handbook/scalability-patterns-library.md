# Scalability Patterns Library

## 🗂️ Data Partitioning Strategies

### Horizontal Partitioning (Sharding)
**Hash-Based Sharding**
```
shard = hash(user_id) % number_of_shards
```
- **Pros**: Even distribution
- **Cons**: Hard to rebalance
- **Use**: User data, messages

**Range-Based Sharding**  
```
if user_id < 1000: shard_1
elif user_id < 2000: shard_2
```
- **Pros**: Easy queries on ranges
- **Cons**: Hot spots possible
- **Use**: Time-series data

**Directory-Based Sharding**
- Lookup service to find data location
- **Pros**: Flexible, easy rebalancing
- **Cons**: Extra hop, single point of failure

### Geographic Partitioning
- **Use**: Global applications
- **Example**: US-East, US-West, Europe, Asia regions
- **Benefits**: Reduced latency, compliance

## 🔄 Replication Patterns

### Master-Slave Replication
- One write node, multiple read replicas
- **Use**: Read-heavy workloads
- **Example**: Product catalogs, user profiles

### Master-Master Replication  
- Multiple write nodes
- **Use**: High availability writes
- **Challenge**: Conflict resolution

### Leaderless Replication
- All nodes accept writes
- **Use**: High availability, eventual consistency
- **Example**: Cassandra, DynamoDB

## 📨 Messaging Patterns

### Request-Response
- Synchronous communication
- **Use**: Critical path operations
- **Example**: Payment processing

### Publish-Subscribe
- Asynchronous, event-driven
- **Use**: Decoupled services
- **Example**: Notification systems

### Message Queues
- Guaranteed delivery, load balancing
- **Use**: Background processing
- **Example**: Image processing, email sending

## 🏗️ Architecture Patterns by Scale

### Small Scale (< 10K users)
- Monolith + Database + Cache
- **Example**: Single server, PostgreSQL, Redis

### Medium Scale (10K - 1M users)  
- Load Balancer + App Servers + Database
- **Example**: Multiple app instances, read replicas

### Large Scale (1M+ users)
- Microservices + Multiple Databases + CDN
- **Example**: Service mesh, distributed databases

### Global Scale (10M+ users)
- Geographic distribution + Edge computing
- **Example**: Multi-region deployment, edge caches