# Pratice problems

## Exercise 1: The "Read-Heavy" Fan-Out

Scenario: Design a Live Sports Score Widget for the Google Search results page.

Traffic: 10 million concurrent users watching the World Cup final.

Update Frequency: Scores change rarely (every few minutes), but game clock updates every second.

Constraint: You must minimize battery usage on client devices.

Your Tasks:

- Protocol Selection: Evaluate Server-Sent Events (SSE) vs. Long Polling vs. WebSockets. Which one is strictly better here and why? (Hint: Consider the unidirectional nature of the data).

- The "Thundering Herd" Twist: The game ends. 10 million clients simultaneously disconnect or refresh. How do you protect your backend?

- L5 Deep Dive: How do you architect the "Source → Server" hop to ensure that a single goal event is broadcast to 10 million connections with under 200ms latency? (Hint: Look into the "Pushing via Pub/Sub" section of the pattern).

## Solution

### Protocol Selection

For real time updates, we can choose any of polling, long polling, SSE and Websockets protocol.

For the live sports score widget app, we need to send score updates to users. Here there will only be a unidirectional flow of data.
So for this use case **Server-Sent Events (SSE)** is the protocol which we will be choosing.

Reasons for choosing **Server-Sent Events (SSE)**

- SSE is perfect for use cases where we want a unidirectional data flow from servers to clients and for our Live sports score app, this is exactly the use case
- With SSE, the server can send score updates to clients as soon as they score updates happen, giving a near real time experience to the users.
- Polling and Long polling will not be suited as it will make the clients do repeated API calls to fetch the scores, this will drain the clients battery and add overhead of so many API calls to be made. So polling and long polling are not battery efficient.
- Websockets here will be an overkill as we don't need bidirectional communication. Websockets also have more complex implementation and higher resource usage on server side. So for battery efficiency and simplicity, SSE is a better choice.

### The "Thundering Herd" Twist

To protect the backend from the "Thundering Herd" problem when 10 million clients disconnect or refresh simultaneously, we can implement the following strategies:

1. **Randomized Backoff**: Implement a randomized backoff mechanism on the client side. When the game ends, clients can wait for a random duration before attempting to reconnect or refresh. This will help spread out the load on the server over time. We can use exponential backoff with jitter to further reduce the chances of simultaneous reconnections.
2. **Load Shedding**: Implement load shedding on the server side. If the server detects a sudden spike in connections, it can temporarily reject new connections or serve a cached version of the widget to reduce the load.

### L5 Deep Dive

To ensure a single goal event is broadcast to 10 million connections with under 200 ms latency, we can use a Pub/Sub model with Redis.

- Users will be subscribing to games which we will be maintaining as topics on server side.
- Since we have around 10 million connections, we will be using hierarchial aggregation using regional servers.
- Each user will be connecting to regional servers which in turn will subscribe to topics on central pub/sub server.
- When a goal event happens, the source will publish the event to the central pub/sub server.
- The central pub/sub server will then push the event to all regional servers.
- Each regional server will then broadcast the event to all connected clients in that region.
- This hierarchical approach reduces the load on the central pub/sub server and ensures that the event is delivered to all clients within the required latency.
- To further optimize latency, we can use techniques like message batching and compression to reduce the size of messages being sent over the network.
- Additionally, we can use CDN (Content Delivery Network) to cache and deliver static assets of the widget, reducing the load on the origin server and improving overall performance.
- Monitoring and alerting systems should be in place to quickly identify and resolve any latency issues that may arise during the broadcast process.

By implementing these strategies, we can ensure that the Live Sports Score Widget can handle real-time updates efficiently and effectively, providing a seamless experience for users during high-traffic events like the World Cup final.

---

## Exercise 2

Scenario: Design a Collaborative Code Editor (like a simplified Google Docs).

Traffic: Small groups (2-5 users) per session.

Requirement: Users can type simultaneously. Latency must be perceived as "instant."

Your Tasks:

- **Protocol**: Why is Long Polling a disaster here? Why might WebSockets be preferred over SSE?

- **State Management**: Since WebSockets are stateful, a specific server holds the connection for User A. If User B sends an update, how does that update find the exact server holding User A's connection? (This is the core "Server-Side Push/Pull" challenge).

- **Conflict Resolution (The L5 Differentiator)**: User A types "Hello" at index 0. User B types "World" at index 0 at the exact same time. How do you ensure they end up with "Hello World" (or "World Hello") and not "HWeolrllod"? (Hint: Mention OT or CRDTs).

## Solution

### Protocol
Long Polling is a disaster for a collaborative code editor because it introduces significant latency and overhead. In Long Polling, the client sends a request to the server and waits for a response. If multiple users are typing simultaneously, this can lead to a flood of requests and responses, causing delays and making the experience feel sluggish. Additionally, Long Polling does not provide true real-time communication, which is essential for a collaborative editor where users expect instant updates. WebSockets, on the other hand, provide a persistent, full-duplex connection between the client and server, allowing for low-latency, real-time communication. This makes WebSockets a much better choice for collaborative applications where multiple users need to see each other's changes instantly.

### State Management

Now for our collaborative code editor app, it will hold state, like each user will be connecting to a specific server. We can use consistent hashing and load balancers to ensure that updates from User B can find the exact server holding User A's connection.

- When User A connects to the collaborative code editor, a load balancer will route their connection to a specific server based on consistent hashing of the document Id. This ensures that all users editing the same document are routed to the same server.
- When User B sends an update, the load balancer will again use consistent hashing to determine which server is responsible for the document being edited. This way, User B's update will be routed to the same server that holds User A's connection.
- The server will then broadcast User B's update to all connected clients, including User A, ensuring that everyone sees the changes in real-time.
- To handle server failures, we can implement a mechanism to replicate the state of each document across multiple servers. This way, if one server goes down, another server can take over and continue serving the clients without losing any data.


### Conflict Resolution (The L5 Differentiator)
To ensure that simultaneous edits from multiple users are merged correctly in a collaborative code editor, we can use Conflict-free Replicated Data Types (CRDTs) or Operational Transformation (OT).

- **Operational Transformation (OT)**: OT is a technique that allows multiple users to edit the same document simultaneously by transforming operations based on their context. When User A types "Hello" at index 0 and User B types "World" at index 0 at the same time, the system will transform one of the operations based on the other. For example, if User A's operation is processed first, User B's operation will be transformed to insert "World" at index 5, resulting in "HelloWorld". If User B's operation is processed first, User A's operation will be transformed to insert "Hello" at index 5, resulting in "WorldHello". This ensures that both edits are preserved and merged correctly.

- **Conflict-free Replicated Data Types (CRDTs)**: CRDTs are data structures that allow for concurrent updates without conflicts. Each user can make changes to their local copy of the document, and these changes can be merged automatically when they are synchronized with the server. In the case of User A and User B typing at the same time, the CRDT will ensure that both "Hello" and "World" are included in the final document, regardless of the order in which the updates are received. The CRDT will handle the merging of the two edits in a way that preserves both contributions.

By implementing either OT or CRDTs, we can ensure that simultaneous edits from multiple users are merged correctly, providing a seamless collaborative editing experience.

---