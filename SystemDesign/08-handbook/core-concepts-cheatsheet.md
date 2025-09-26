# System Design Core Concepts Cheat Sheet

## 📈 Scalability Patterns

### Horizontal vs Vertical Scaling
**Vertical (Scale Up)**
- ✅ Simple, no code changes
- ❌ Single point of failure, expensive
- **When**: Small to medium scale, simple apps

**Horizontal (Scale Out)**  
- ✅ Better availability, cost-effective
- ❌ Complex, data consistency challenges
- **When**: Large scale, high availability needs

### Load Balancing Algorithms
- **Round Robin**: Equal distribution, simple
- **Weighted Round Robin**: Different server capacities
- **Least Connections**: For long-lived connections
- **IP Hash**: Session affinity (sticky sessions)

## 💾 Caching Strategies

### Cache Patterns
**Cache-Aside (Lazy Loading)**
```
if (data not in cache):
    data = fetch_from_db()
    cache.set(key, data)
return data
```
- **Use**: Read-heavy, data doesn't change often
- **Example**: User profiles, product details

**Write-Through**
```
cache.set(key, data)
db.write(data)
```
- **Use**: Write consistency important
- **Example**: Financial transactions

**Write-Behind (Write-Back)**
```
cache.set(key, data)  // Write to DB later
```
- **Use**: High write volume, eventual consistency OK
- **Example**: Analytics data, logs

### Cache Levels
1. **Browser Cache**: Static assets (CSS, JS, images)
2. **CDN**: Geographic distribution of static content
3. **Application Cache**: API responses, computed results
4. **Database Cache**: Query result caching

## 🔄 Consistency Patterns

### Strong Consistency
- All nodes see same data simultaneously
- **Use**: Financial systems, booking systems
- **Example**: Bank account balance, ticket inventory

### Eventual Consistency  
- Nodes will converge to same value eventually
- **Use**: Social media, content distribution
- **Example**: Twitter follower count, Like counts

### Weak Consistency
- No guarantees when all nodes will be consistent
- **Use**: Real-time gaming, live video
- **Example**: Voice calls, live streaming

## 🚨 Reliability Patterns

### Circuit Breaker States
- **Closed**: Normal operation, requests pass through
- **Open**: Failure detected, requests fail fast
- **Half-Open**: Testing if service recovered

### Retry Strategies
**Exponential Backoff**
```
retry_delay = base_delay * (2 ^ retry_count) + jitter
```

**When to Retry**
- ✅ Timeouts, 5xx errors, network issues
- ❌ 4xx errors, validation failures

### Bulkheading
- Isolate resources to prevent cascading failures
- **Example**: Separate thread pools for different operations

## 📊 CAP Theorem Quick Reference

**Consistency + Availability**: RDBMS (PostgreSQL, MySQL)
**Consistency + Partition Tolerance**: MongoDB, Redis
**Availability + Partition Tolerance**: Cassandra, DynamoDB

## 🎯 When to Use Each Pattern

| Pattern | Use When | Examples from Our Systems |
|---------|----------|---------------------------|
| **Microservices** | Complex domain, team scaling | Chat (User, Message, Sync services) |
| **Event Sourcing** | Audit trail needed | Ticketing (booking events) |
| **CQRS** | Read/write patterns differ | News feed (write posts, read feeds) |
| **Saga Pattern** | Distributed transactions | Ride sharing (booking + payment) |
| **Fan-out** | 1-to-many distribution | News feed (post to followers) |