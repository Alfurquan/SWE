"""
Week 3 - Problem 1: Distributed Hash Table
Difficulty: Hard | Time Limit: 90 minutes | Google L5 Distributed Systems

PROBLEM STATEMENT:
Implement a distributed hash table with consistent hashing

OPERATIONS:
- addNode(node_id): Add new node to the ring
- removeNode(node_id): Remove node and redistribute data
- put(key, value): Store key-value pair
- get(key): Retrieve value from appropriate node
- rebalance(): Redistribute data after topology changes

REQUIREMENTS:
- Consistent hashing with virtual nodes
- Handle node failures gracefully
- Minimize data movement during rebalancing
- Support replication factor N

ALGORITHM:
Consistent hashing, virtual nodes, data replication

REAL-WORLD CONTEXT:
Amazon DynamoDB, Apache Cassandra, distributed caching systems

FOLLOW-UP QUESTIONS:
- How to handle network partitions?
- Read/write quorum strategies?
- Anti-entropy and conflict resolution?
- Performance optimization techniques?

EXPECTED INTERFACE:
dht = DistributedHashTable(replication_factor=3)
dht.addNode("server1")
dht.addNode("server2")
dht.put("key1", "value1")
nodes = dht.getResponsibleNodes("key1")
value = dht.get("key1")
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
