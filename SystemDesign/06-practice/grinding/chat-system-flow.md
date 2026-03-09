# 📝 System Design Blueprint: 1-on-1 & Group Chat Application (The Ultimate L5/L6 Revision)

---

## 1. System Requirements & Scale

| Metric | Value |
|---|---|
| **Traffic Shape** | 50 Million DAU. Highly concurrent, persistent connections. |
| **Group Constraints** | Support both 1-on-1 chats and large group communities (up to 50,000 members). |
| **Storage Load** | ~73 Petabytes per year (Text + Media) |
| **Read/Write Ratio** | 1:1 for 1-on-1. For large groups, heavily Read-Heavy (1 Write fans out to 50k Reads). |
| **Key Constraints** | Ultra-low latency (<200ms), strict message ordering (gapless), exactly-once processing (idempotency), and reliable offline delivery |

---

## 2. Core Architecture & Separation of Concerns

> Designing data-intensive applications at this scale requires strictly separating **state management**, **message routing**, **sequence generation**, and **permanent storage**.

### A. The Edge (Connection Handling)

- **Component:** Layer 4 Network Load Balancer (NLB).
- **Why:** A standard Layer 7 Application Load Balancer parses HTTP headers and suffers from ephemeral TCP port exhaustion (~65k ports per IP). An NLB passes raw TCP packets directly to the backend, allowing us to horizontally scale to **50 million concurrent, persistent connections**.

### B. The Application Layer (Stateful Pipes & Local Routing)

- **Component:** Chat Servers (horizontally scaled).
- **Why:** These servers hold hundreds of thousands of open WebSocket connections. They maintain a **bidirectional pipe** to the client.
- **The Local Map:** Every server maintains a local, in-memory dictionary (e.g., `ConcurrentHashMap<UserID, WebSocketFD>`). This maps a connected user directly to their physical TCP socket for instant local routing.

### C. The Routing & State Layer (Ephemeral Redis)

- **Component:** Redis Cluster 1 (Memory & Network Optimized).
- **Why:** Runs in pure RAM. It acts as the centralized "Post Office":
  - **Session Store:** Maps `user_id` → `chat_server_id` globally.
  - **Message Bus (Pub/Sub):** Routes payloads between Chat Servers without a complex server-to-server network mesh.

### D. The Sequence Generator (Durable Redis)

- **Component:** Redis Cluster 2 (CPU & Disk Optimized).
- **Why:** Physically separated from the Ephemeral Cluster. Uses atomic `INCR` commands to generate strict, collision-free logical sequence numbers (`seq:chat:999`). Requires strict **Append-Only File (AOF)** disk persistence to prevent data corruption during crashes.

### E. The Fan-Out Layer (Async Group Processing)

- **Component:** Message Queue (Kafka) + Fan-Out Workers + Group Cache (Redis).
- **Why:** Decouples the Chat Servers from the massive CPU burden of routing a single message to 50,000 group participants synchronously.

### F. The Ledger (Permanent Storage)

- **Component:** Cassandra / ScyllaDB.
- **Why:** Uses **Log-Structured Merge (LSM) Trees**, sequentially appending writes to disk without the lock contention that relational SQL databases suffer from under extreme write loads.

---

## 3. Data Modeling (Cassandra Schema)

> We design the table directly around the read query: _"Fetch the latest messages for this specific chat in chronological order."_

### Table: `messages`

| Column | Role | Description |
|---|---|---|
| `chat_id` | **Partition Key** | Represents either a 1-on-1 chat or a group. Forces all messages for that specific conversation to live on the exact same physical database node. |
| `sequence_number` | **Clustering Key** | Automatically sorts the messages sequentially on disk as they arrive. |
| `message_id` | UUID / Idempotency Key | Unique identifier for each message. |
| `sender_id` | — | The user who sent the message. |
| `text_payload` | — | Message body. |
| `media_url` | — | URL for attached media (if any). |
| `status` | — | `pending`, `delivered`, `read` |

---

## 4. The Complete End-to-End Flows

### Flow A: The Boot-Up & Connection Sync

1. **Server Boot:** When Chat Server 84 boots, it makes a single subscription to the Redis Message Bus: `SUBSCRIBE channel:Server84`.
2. **User Connects:** User B opens the app. The NLB routes their TCP connection to **Chat Server 84**.
3. **Local Map Update:** Chat Server 84 maps User B to their WebSocket file descriptor.
4. **Global Map Update:** Chat Server 84 registers User B in the global Redis Session Store: `SET session:UserB Server84`.
5. **Offline Sync:** Chat Server 84 queries Cassandra for missed messages (`status = 'pending'`), flushes them down the WebSocket, and marks them `delivered`.

### Flow B: Sending a 1-on-1 Message (Optimized Routing)

1. **The Intent:** User A types "Hello". Their client generates a unique `idempotency_key` and sends the payload over their WebSocket to **Server 12**.
2. **Sequence Generation:** Server 12 makes a sub-millisecond call to the Durable Redis Cluster: `INCR seq:chat:999`.
3. **Persistence:** Server 12 writes the payload, `idempotency_key`, and `sequence_number` asynchronously to Cassandra.
4. **Global Discovery:** Server 12 queries the Ephemeral Redis Session Store: `GET session:UserB`. Redis returns `Server84`.
5. **The Handoff:** Server 12 publishes the enriched message payload to the Ephemeral Redis Pub/Sub channel: `PUBLISH channel:Server84 {"target": "UserB", "text": "Hello"}`.
6. **The Final Mile:** Server 84 receives the message on its single subscribed channel, looks up `"UserB"` in its local `ConcurrentHashMap`, and flushes the bytes directly to User B's phone.

### Flow C: Sending Media (Images/Video)

1. **Request Upload Token:** User A selects a 5MB image. Their client makes a standard HTTP GET request to the Media Service API.
2. **Upload Direct to Edge:** The Media Service returns a **Presigned URL**. The client uses this URL to upload the heavy byte stream **directly to Object Storage (S3)**, completely bypassing the Chat Servers.
3. **Store & Forward:** S3 returns the final URL. The client then executes **Flow B**, sending a lightweight JSON WebSocket payload containing only the S3 URL.
4. **Download:** User B receives the JSON payload, reads the URL, and their phone downloads the image directly from the CDN.

### Flow D: Sending a Group Message (Async Fan-Out)

1. **The Intent:** User A sends a message to `group:555` (a community with 50,000 members) via their WebSocket connection to **Chat Server 12**.
2. **The Fast Ingest:** Chat Server 12 generates the sequence number, writes the message to Cassandra, replies `200 OK` to User A, and instantly drops the payload into a **Kafka Message Queue** (topic: `group_messages`). It does **not** attempt to route the message.
3. **The Async Worker:** A background **Fan-Out Worker** consumes the event from Kafka.
4. **The Resolution:** The Worker queries the **Redis Group Cache** to retrieve the 50,000 participant IDs.
5. **The Handoff:** The Worker chunks the IDs into batches, queries the Ephemeral Redis Session Store to find their active Chat Servers, and executes the `PUBLISH` commands asynchronously, leaving the core Chat Servers completely unblocked.

---

## 5. L5/L6 Deep Dives (Solving the Distributed Bottlenecks)

### Deep Dive 1: The Group Chat "Fan-Out" Trap

- **The Problem:** If User A sends a message to a 50,000-person community group, executing 50,000 Redis `GET` and `PUBLISH` commands synchronously will lock the Chat Server's thread, maxing out CPU and starving other users' WebSocket connections.

- **The L6 Solution:** Use the Async Fan-Out flow described in **Flow D**. By pushing the routing logic to a Kafka queue and stateless workers, the stateful Chat Servers are mathematically isolated from the massive CPU spikes of group routing.

### Deep Dive 2: The Pub/Sub Scaling Trap (Channel Churn)

- **The Problem:** Subscribing to one Redis channel per user (50 million channels) will melt the Redis cluster due to massive subscription churn as users constantly connect and disconnect.

- **The L5 Solution:** One channel per server. Chat Server 84 only subscribes to `channel:Server84`. Server 12 publishes to Server 84's channel via the centralized Redis Bus. The internal `ConcurrentHashMap` on Server 84 handles the "last mile" routing, completely decoupling the infrastructure and eliminating server-to-server network mesh spaghetti.

### Deep Dive 3: Strict Ordering via Gap Detection (Beating Clock Drift)

- **The Problem:** Network lag can cause messages to arrive out of order. Relying on physical timestamps will result in a permanently jumbled UI.

- **The L5 Solution:** We rely on the logical `sequence_number` and push reconciliation to the client.
  1. User B's phone tracks `last_seen_seq_no = 100`.
  2. The phone receives a WebSocket payload: `seq = 102`.
  3. The client logic flags a gap: `102 != 100 + 1`. Sequence 101 vanished in transit.
  4. The client **hides** Sequence 102 from the UI to prevent jumping.
  5. The client silently makes an HTTP GET to fetch Sequence 101 from Cassandra. It then renders 101, then 102, guaranteeing a mathematically perfect linear UI.

### Deep Dive 4: Idempotency & Fault Isolation

- **Idempotency:** A client retry due to a dropped network ack can duplicate messages. The client generates a UUID (`idempotency_key`) before the first attempt. The Chat Server checks this key against Cassandra, silently dropping duplicate database writes to guarantee **exactly-once processing**.

- **Fault Isolation:** The **Sequence Generator** (CPU-heavy, strict disk writes) is physically isolated from the **Session/Pub-Sub cluster** (Memory-heavy, pure RAM). A viral global event maxing out routing traffic will never starve the sequence generator.