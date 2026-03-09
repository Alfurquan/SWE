# 📝 System Design Deep Dive: Live Delivery Tracker

---

## Part 1: The Heavy Write Block (Ingestion & Storage)

When 100,000 drivers send their GPS coordinates every 3 seconds, you are dealing with a firehose of **~33,000 writes per second**.

If you try to write this directly to a standard relational database (like PostgreSQL), the system will crash. Why? Because SQL databases use **B-Trees** under the hood. To update a row in a B-Tree, the database has to physically find that exact block of data on the hard drive, read it, modify it, and write it back. This is called **Random I/O**, and hard drives (even SSDs) bottleneck quickly when doing 33,000 random jumps per second.

To solve this, L5 engineers split the data stream into two distinct paths: **Current State** and **Historical Path**.

### 1. Current State (Redis)

We only need to know the driver's exact current location to show it on the map and calculate ETAs. We do not need the last 50 pings in RAM.

- **The Mechanism:** When the API Gateway receives the ping, it fires a `GEOADD` command to Redis.
- **How it works:** Redis stores this in RAM using a **Geohash** (which converts a 2D latitude/longitude into a 1D string, like `9q8yy`). Under the hood, this is stored in a **Sorted Set (ZSET)**. Because it is purely in memory, writing to it takes microseconds.
- **The Optimization:** We overwrite the driver's previous location. This ensures our Redis memory footprint never grows infinitely, even if the driver drives for 12 hours.

### 2. The Historical Path (Cassandra)

We still must save every single ping (the "breadcrumb trail") for customer disputes, safety investigations, and machine learning.

- **The Buffer:** The API Gateway drops the raw ping into a **Kafka Topic** (e.g., `driver_locations`).
- **The Storage:** Background workers consume from Kafka and write to **Cassandra** (or ScyllaDB).

> **Why Cassandra? (The DDIA Connection):**
> Cassandra does not use B-Trees; it uses **Log-Structured Merge (LSM) Trees**. When a write hits Cassandra, it doesn't search the disk. It simply appends the data sequentially to an in-memory structure called a **MemTable**, and eventually flushes it to disk as an immutable file (**SSTable**). Sequential I/O is blazing fast. Cassandra can easily absorb **100,000+ writes per second** without ever locking up.

---

## Part 2: The Customer View Block (Real-Time Routing)

Now we have the data safely stored. But you are staring at your phone, and we need to make the little car icon move across your screen smoothly.

### 1. The Connection: Server-Sent Events (SSE)

You correctly chose SSE over WebSockets. Here is exactly why that is the right choice to defend in an interview:

- **WebSockets** are full-duplex (two-way communication). They require a special handshake and custom protocol handling.
- **SSE** is half-duplex (server-to-client only). The client makes a standard HTTP GET request with the header `Accept: text/event-stream`. The server responds with `200 OK`, but intentionally leaves the TCP connection open. The server can now stream plaintext JSON payloads down that open pipe forever. Because it operates over standard HTTP, it easily passes through firewalls and corporate proxies without issue.

### 2. The Routing: Redis Pub/Sub

If the driver's phone is connected to **Gateway Server A**, and your phone is connected to **Gateway Server B**, how does the GPS ping cross the gap? We use the exact same pattern we used in the Chat App.

1. **The Subscription:** When you open the Uber app, your phone establishes an SSE connection to Server B. Server B registers this internally and subscribes to a Redis channel for your specific trip: `SUBSCRIBE channel:trip:999`.
2. **The Ingest:** The driver's phone sends a HTTP POST to Server A with `{lat: 37.77, lng: -122.41}`.
3. **The Broadcast:** Server A instantly executes: `PUBLISH channel:trip:999 '{"lat": 37.77, "lng": -122.41}'`.
4. **The Delivery:** Server B receives the payload from Redis. It looks in its local memory, finds your open SSE connection, and pushes the JSON down the pipe to your phone.

---

## Part 3: The L5 Edge Case (The Reconnect)

An interviewer will always test what happens when the network fails.

**The Scenario:** You drive into a tunnel. Your phone loses internet. The SSE connection drops. Ten seconds later, you exit the tunnel and your phone reconnects. How do we prevent the car from magically "teleporting" on your screen, skipping the 10 seconds of data?

**The Native SSE Feature:** SSE has a built-in feature called `Last-Event-ID`. Every time the server sends a GPS ping, it attaches an ID (usually the timestamp).

**The Recovery Flow:**

1. When your phone reconnects, the HTTP header automatically includes: `Last-Event-ID: 1710000000`.
2. Server B receives the connection. Before it subscribes to the live Pub/Sub stream, it makes a lightning-fast query to Cassandra (or a short-lived Redis List caching the last 2 minutes): *"Fetch all pings for Trip 999 since timestamp 1710000000."*
3. Server B flushes those missed pings down the SSE pipe.
4. Your phone's UI animates the car quickly catching up along the road.
5. Server B resumes the live Redis Pub/Sub stream.