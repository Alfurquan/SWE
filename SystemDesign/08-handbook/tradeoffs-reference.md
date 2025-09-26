# System Design Trade-offs Reference

## 🎯 Common Trade-off Decisions

### SQL vs NoSQL
| Aspect | SQL (PostgreSQL) | NoSQL (MongoDB) |
|--------|------------------|-----------------|
| **Schema** | Fixed, structured | Flexible, evolving |
| **Scaling** | Vertical, read replicas | Horizontal sharding |
| **Consistency** | ACID transactions | Eventual consistency |
| **Queries** | Complex joins, SQL | Simple queries, aggregation |
| **Use Cases** | Financial, booking | Content, analytics |

### Consistency vs Availability
| Scenario | Choose Consistency | Choose Availability |
|----------|-------------------|-------------------|
| **Banking** | ✅ Account balance must be accurate | ❌ |
| **Social Media** | ❌ | ✅ Feed can be slightly stale |
| **E-commerce** | ✅ Inventory must be accurate | ❌ |
| **Gaming** | ❌ | ✅ Game state can be approximate |

### Push vs Pull Model
| Aspect | Push (Fan-out on Write) | Pull (Fan-out on Read) |
|--------|------------------------|----------------------|
| **Read Time** | Fast (pre-computed) | Slower (compute on demand) |
| **Write Time** | Slower (fan-out cost) | Fast (just write) |
| **Storage** | High (duplicate data) | Low (single copy) |
| **Use Case** | Few writes, many reads | Many writes, few reads |

### Synchronous vs Asynchronous
| Operation Type | Sync | Async |
|----------------|------|-------|
| **Critical Path** | Payment processing | Analytics |
| **User Facing** | Login, search | Email notifications |
| **Real-time** | Chat messages | Batch processing |
| **Consistency** | Strong consistency needed | Eventually consistent OK |

## 🔧 Performance vs Other Factors

### Caching Trade-offs
| Factor | Benefit | Cost |
|--------|---------|------|
| **Speed** | Faster reads | Memory usage |
| **Scalability** | Reduced DB load | Cache invalidation complexity |
| **Consistency** | ❌ Possible stale data | Cache warming overhead |

### Denormalization Trade-offs  
| Factor | Benefit | Cost |
|--------|---------|------|
| **Read Speed** | Fewer joins needed | Data duplication |
| **Query Simplicity** | Simple lookups | Update complexity |
| **Scaling** | Better read performance | Storage overhead |

## 📊 Choosing the Right Pattern

### By Read/Write Ratio
- **Read Heavy (90:10)**: Caching, read replicas, denormalization
- **Write Heavy (10:90)**: Sharding, async processing, eventual consistency  
- **Balanced (50:50)**: Hybrid approaches, careful optimization

### By Consistency Requirements
- **Strong**: RDBMS, synchronous replication
- **Eventual**: NoSQL, async replication, caching
- **Weak**: In-memory stores, approximate algorithms

### By Latency Requirements  
- **< 10ms**: In-memory cache, CDN
- **< 100ms**: Optimized databases, local caching
- **< 1s**: Standard database queries, some network calls
- **> 1s**: Complex computations, external API calls