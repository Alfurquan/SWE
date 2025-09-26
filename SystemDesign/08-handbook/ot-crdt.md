# Operational Transformation (OT) vs Conflict-Free Replicated Data Types (CRDTs)

## Whats the core problem?

Imagine you and your friend are editing the same Google Doc simultaneously. You both start with the text "Hello!" and:

- You type ", world" after "Hello" → "Hello, world!"
- Your friend deletes the "!" → "Hello"

But both operations happen at the same time. What should the final result be? This is the fundamental challenge of collaborative editing.

## Operational Transformation (OT)

### Basic concept

OT is like having a smart coordinator that transforms (adjusts) operations so they work correctly even when applied in different orders.

Think of it as a traffic controller at an intersection - operations are like cars coming from different directions, and OT makes sure they don't crash into each other by adjusting their paths.

### How OT works - step by step

1. **Step 1: Operations as Instructions**

Instead of sending the entire document, users send specific instructions:

- INSERT(position, text) - "Insert this text at this position"
- DELETE(position, length) - "Delete text starting at this position"

2. **Step 2: The Transform Function**

When two operations conflict, OT transforms them using mathematical rules:

- **Example 1: Two insertions**

```text
Initial: "Hello"
User A: INSERT(5, "!") → "Hello!"
User B: INSERT(5, " world") → "Hello world"

Problem: Both want to insert at position 5
Solution: Transform User B's operation to INSERT(6, " world")
Result: "Hello! world"
```

- **Example 2: Insertion and Deletion**

```text
Initial: "Hello!"
User A: INSERT(5, ", world") → "Hello, world!"
User B: DELETE(5, 1) → "Hello" (delete the "!")

Problem: User B wants to delete position 5, but User A inserted at position 5
Solution: Transform User B's DELETE(5, 1) to DELETE(12, 1)
Result: "Hello, world"
```

3. **Step 3: Server as Central Authority**

- All operations go through one central server
- Server applies operations in order it receives them
- Server transforms conflicting operations before applying
- Server sends transformed operations to all other clients

### OT pros

1. Memory efficient

- Only stores the current state plus recent operations
- No need to keep entire history forever
- Each operation is small (just the change, not whole document)

2. Low latency

- Operations are transformed quickly with simple math
- No complex conflict resolution algorithms
- Direct communication between clients and server

3. Deterministic results

- Same operations always produce same final document
- Mathematical guarantee of consistency
- Predictable behavior for users

### OT cons

1. Requires a central server

- Single point of failure
- All operations must go through server
- Harder to work offline

2. Complex transformation logic

- Writing correct transform functions is tricky
- Easy to introduce bugs
- Must handle every possible combinations of operations

3. Order Dependency

- Operations must be processed in specific order
- Can't easily handle network partitions
- Difficult to merge offline changes

### Real world OT Examples

- Google Docs
  - Uses OT for real-time collaborative editing
  - All edits go through Google's servers
  - Transforms operations to handle conflicts
  - Works well because most documents have < 100 concurrent editors

- Microsoft Office 365
  - Similar to Google Docs, uses OT for Word and Excel online
  - Central server architecture
  - Handles complex documents with many users

## Conflict-Free Replicated Data Types (CRDTs)

### Basic concept of CRDTs

CRDTs are like having magic operations that can be applied in any order and always produce the same result.

Think of it like mixing ingredients for a smoothie - it doesn't matter if you add the banana first or the strawberry first, you'll get the same smoothie in the end.

### How CRDTs work - step by step

- **Step 1: Every Character Has Unique Identity**

Instead of positions, each character has a unique ID that never changes. For example:

```text
"Hello!" becomes:
H(1.0) e(2.0) l(3.0) l(4.0) o(5.0) !(6.0)
```

- **Step 2: Operations Use IDs, Not Positions**

```text
Insert ", world" after "Hello":
- Find character with ID 5.0 (the 'o')
- Insert new characters with IDs between 5.0 and 6.0:
  ,(5.1) (5.2) w(5.3) o(5.4) r(5.5) l(5.6) d(5.7)

Delete "!":
- Mark character with ID 6.0 as deleted (but keep the ID)
```

- **Step 3: Automatic Conflict Resolution**

Because operations use permanent IDs instead of changing positions:

```text
User A inserts ", world" → Creates IDs 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7
User B deletes "!" → Marks ID 6.0 as deleted

No matter which order these arrive, result is the same:
H(1.0) e(2.0) l(3.0) l(4.0) o(5.0) ,(5.1) (5.2) w(5.3) o(5.4) r(5.5) l(5.6) d(5.7) [DELETED: !(6.0)]
```

- **Step 4: Distributed by design**

- Each user can apply operations immediately to their local copy
- Operations can be sent to other users in any order
- No central server needed for conflict resolution

### CRDT pros

- No central server needed
  - Fully distributed architecture
  - Users can work offline and sync later
  - No single point of failure

- Automatic conflict resolution
  - Operations commute naturally
  - No complex transformation logic needed
  - Easier to implement correctly

- High availability
  - Users can always edit their local copy
  - Changes can be merged later without conflicts
  - Works well in unreliable networks
  
- Strong consistency guarantees
  - Mathematical proofs ensure convergence
  - All replicas eventually become identical
  - Predictable behavior even with many users

### CRDT cons

- Higher memory usage
  - Must store entire history of operations
  - Each character has unique ID, increasing metadata
  - Can lead to large data sizes over time

- Complex implementation
  - Harder to implement than simple position-based edits
  - Requires understanding of distributed systems concepts
  - ID generation algorithms can be tricky

- Higher latency for some operations
  - Some CRDT operations are more expensive
  - Merging states can be computationally intensive
  - Network bandwidth usage can be higher

### Real world CRDT Examples

- Figma
  - Uses CRDTs for real-time collaborative design
  - Fully distributed, no central server for edits
  - Handles complex vector graphics with many users

- Notion
  - Uses CRDTs for block-based document editing
  - Each block (paragraph, heading, etc.) is a CRDT
  - Enables offline editing and real-time collaboration

### Use Case Guidelines

Choose OT When:

- Low latency is critical (< 50ms)
- Users are mostly online and well-connected
- Smaller teams (< 100 concurrent users per document)
- Centralized architecture is acceptable
- You need immediate consistency

Choose CRDTs When:

- Offline support is important
- Users have unreliable connections
- Large-scale collaboration (thousands of users)
- Peer-to-peer or decentralized architecture needed
- Mobile applications with intermittent connectivity
- Cross-region collaboration with high latency

## OT and offline support

In Interviews, Acknowledge the Trade-off:

- Start with OT limitations:
  - "OT provides excellent real-time collaboration..."
  - "However, it requires central coordination..."
  - "For offline scenarios, we need different strategies..."

- Mention Google's approach:
  - "Google Docs handles this by queuing offline operations..."
  - "When users reconnect, operations are transformed and applied..."
  - "Complex conflicts may result in document copies..."

- Suggest improvements:
  - "For better offline support, we could use hybrid approach..."
  - "CRDTs for document structure, OT for fine-grained text edits..."
  - "Or implement conflict resolution UI for user decision..."