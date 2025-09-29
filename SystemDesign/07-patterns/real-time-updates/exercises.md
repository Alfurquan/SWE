# Practice Exercises

This section contains practice exercises to help you apply the concepts learned in the "Real-Time Updates" section. Try to solve these problems on your own before checking the solutions.

---

## Scenario 1: WhatsApp-like Messaging

You're designing a messaging app like WhatsApp. Users send messages in group chats (up to 256 people) and 1-on-1 conversations. Messages need to be delivered instantly, users should see typing indicators, and read receipts. The app has 2 billion users globally.

Your task: How do you handle real-time message delivery? What's your approach and why?

### Solution

To handle the real-time message delivery of a messaging app like WhatsApp, we will use a combination of web-socket connection and message queue. Here's a high level overview:

- Users will connect to chat rooms using a web socket connection
- When a user sends a message, it is broadcasted to all connected clients to the same web socket connection
- If in case any user is offline or disconnected, we will store the message in the message queue which will be delivered to them when they come online.

We have used web sockets as:

- Websockets provide full duplex communication and in our case we require users to both send and receive messages
- Latency is quite low as communication over web sockets is quite fast and this fulfills our requirement of real time communication

We have used message queues as:

- Message queues offer at least once guarantee that the message will be delivered to the user in case they are offline. This helps in reliable message delivery and ensuring messages are not lost.

### Enhanced solution

**Approach**: WebSockets + Pub/Sub + Message Queues

**Client-Server (Hop 1)**:

- WebSockets for bidirectional communication (messages, typing, read receipts)
- Layer 4 load balancing to maintain persistent connections

**Server-Server (Hop 2)**:

- Pub/Sub system (Kafka) with chat-room topics
- When User A sends message → publish to "chat_room_123" topic
- All servers with users in that room receive and forward via WebSocket

**Offline Handling**:

- Message queues per user for offline delivery
- Push notifications for mobile apps when offline

**Why WebSockets**: Need bidirectional, low-latency for typing indicators and real-time chat
**Why Pub/Sub**: Efficiently broadcast to multiple users across different servers

---

## Scenario 2: Stock Trading Dashboard

You're building a real-time stock trading dashboard for day traders. It displays live stock prices, portfolio values, and market news. Prices update multiple times per second during market hours. Users don't send data back - they just consume updates. 50,000 concurrent users during peak hours.

Your task: How do you deliver real-time price updates? What's your reasoning?

### Solution

**Approach**: SSE + Pub/Sub

**Client-Sever (Hop 1)**:

- Server side events to send messages from server to client.
- Message is sent in chunks

**Server-Server (Hop 2)**:

- Pub/sub system with topics on stock prices, portfolio values and market news
- Whenever there is new content, the pub/sub system publishes the content to respective topics, the server picks the content from the topics and sends as message blocks in form of SSE to the client.

**Why SSE**: Since we just need unidirectional communication from server to client, SSE serves our purpose. Its fast and provide real time updates to client

**Why Pub/Sub**: Efficiently send appropriate content as they come to respective topics for sever to pick and send it to client.

### Enhanced solution

**Approach**: SSE + Pub/Sub + Smart Batching

**Client-Server (Hop 1)**:

- SSE for streaming price updates to dashboard
- Each user subscribes only to their watchlist stocks
- Batch updates every 100ms to avoid overwhelming clients

**Server-Server (Hop 2)**:

- Kafka topics per stock symbol (AAPL, GOOGL, etc.)
- Market data feeds publish to relevant topics
- Edge servers subscribe and cache popular stocks

**Optimizations**:

- User-specific subscriptions (only send relevant data)
- Regional caching for low latency
- Automatic reconnection handling

**Why SSE**: Perfect for one-way, high-frequency streaming
**Why Pub/Sub**: Scales to distribute updates across global servers
**Why Batching**: Prevents client overwhelm with rapid updates

---

## Scenario 3: Collaborative Whiteboard (Miro/Figma)

You're designing a collaborative whiteboard where multiple users can draw, add shapes, and move objects simultaneously. Changes should appear instantly to all collaborators. Each stroke/movement needs to be synchronized. Typical sessions have 5-20 users.

Your task: How do you handle real-time collaboration? What's your approach?

### Solution

**Approach**: Websockets + Consistent hashing + OT for conflict resolution

**Client-Sever (Hop 1)**:

- Web sockets for bi directional communication
- Each users activity/edits are transformed using operational transform and then broadcasted to all connected users
- We use OT for managing conflicts between two users try to edit at same position in the whiteboard.

**Server-Server (Hop 2)**:

- We use consistent hashing to push updates via hash.
- Each user connects to same server, That server handles all their updates and then broadcast it to all other users for the same whiteboard id.

**Why Websockets**: Need bidirectional, low-latency for real-time collaboration.
**Why Consistent hashing**: Its good for maintaining user state which in case are their edits.
**Why OT**: Simple to implements, helps in resolving conflicts. For a scale of concurrent 5-20 users, it serves our purpose. For large scale, we can use CRDT as an alternative.

### Enhanced solution

**Approach**: WebSockets + Consistent Hashing + Operational Transform

**Client-Server (Hop 1)**:

- WebSockets for bidirectional, low-latency drawing/editing
- Each operation (draw, move, delete) sent immediately

**Server-Server (Hop 2)**:

- Consistent hashing by whiteboard_id
- All users on whiteboard_123 → same server (maintains document state)
- Server applies OT to resolve conflicts, broadcasts to all users

**Conflict Resolution**:

- Operational Transform for simultaneous edits
- Server maintains operation history for new user sync

**Why WebSockets**: Instant bidirectional for drawing strokes
**Why Consistent Hashing**: Single server per document = easier state management
**Why OT**: Handles conflicts when users edit simultaneously (5-20 users scale)

---

## Scenario 4: ive Sports Score Updates

You're building a sports app that shows live scores, game events (goals, fouls, etc.), and commentary. Updates happen every few seconds to minutes. Users just view - no interaction needed. During major events, you have 10 million concurrent viewers.

Your task: How do you deliver live updates efficiently? What's your solution?

### Solution 

**Approach**: SSE + Pub/Sub + Batch updates

**Client-Server (Hop 1)**:

- SSE to transfer updates from server to clients.
- Users only subscribe to the sports they want updates for.

**Server-Server (Hop 2)**:

- Pub/Sub system to publish updates to topics on server
- Server picks updates and streams them to client using SSE

**Optimization**:

- Handling 10 million concurrent viewers, we use regional caching to reduce latency
- User specific subscriptions only, send relevant data

**Why SSE?**: SSE is chosen, as we just need single way communication from server to client, and SSE helps us achieve that with very low latency.
**Why Pub/Sub?**: Pub/Sub is chosen as it helps decouple server from update source, clients can subscribe to topics, and updates are published to those topics which server can then stream back to the clients. It is Best for broadcasting to many users and this is what exactly we need.

### Polished solution

**Approach**: SSE + Pub/Sub + Hierarchical Distribution

**Client-Server (Hop 1)**:

- SSE for streaming live updates
- User subscribes to specific games/teams only
- CDN edge servers handle SSE connections regionally

**Server-Server (Hop 2)**:

- Pub/Sub with game-specific topics (game_12345)
- Hierarchical distribution: Central → Regional → Edge servers
- Batch related events (goal + time + score) into single update

**Scale Optimizations**:

- Regional CDN reduces load on origin servers
- Event prioritization: scores (instant) vs stats (batched)
- Connection pooling at edge servers

**Why SSE**: One-way, efficient for 10M concurrent streams
**Why Hierarchical**: Prevents single server from handling 10M fan-out
**Why Batching**: Reduces update frequency without losing important events

**When asked about scale**:

```text
"At 10M concurrent users, I'd implement hierarchical distribution - 
central servers feed regional servers, 
which feed edge servers. This prevents any single server from handling the full fan-out.
I'd also use CDN caching and batch updates to optimize further."
```

### Celebrity problem

#### What is the Celebrity Problem?

The "Celebrity Problem" occurs when one piece of content needs to be delivered to millions of users simultaneously. It's called the "celebrity problem" because it's like a celebrity posting on social media - millions of followers all need the same update at once.

#### Why is it a Problem?

Naive Approach (What Breaks):

```text
Game Server receives: "GOAL! Team A scores!"
↓
Server tries to send to: User1, User2, User3, ... User10,000,000
```

#### What happens:

- Server tries to make 10M individual connections/writes
- Server CPU/memory explodes 💥
- Network bandwidth gets saturated
- Server crashes under load
- Users get no updates at all

#### Real-World Example: Super Bowl

Imagine the Super Bowl final touchdown:

- 10M people watching the same game
- All need the "TOUCHDOWN!" update within seconds
- If each user needs individual delivery = 10M network operations
- Result: System meltdown 🔥

#### The Solution: Hierarchical Distribution

Instead of one server handling 10M users, create a tree structure:

```text
🏈 Game Event: "GOAL!"
       ↓
   Central Server (1 update)
       ↓
┌──────┼──────┐
│      │      │
Regional Servers (3 updates)
West   Central  East
│      │      │
┌─┼─┐  ┌─┼─┐  ┌─┼─┐
Edge Servers (9 updates total)
│ │ │  │ │ │  │ │ │
Users (10M total)
3M 3M 3M 1M 1M 1M etc...
```

#### How it Works

- Central Server gets the update, sends to 3 regional servers
- Regional Servers each send to ~3 edge servers (9 total)
- Edge Servers each handle ~1M users locally
- Total server work: 1 + 3 + 9 = 13 operations instead of 10M!

#### Additional Optimizations

1. CDN (Content Delivery Network)

```text
Instead of: All users → Game Server
Use: Users → Nearest CDN Edge → Game Server
```

2. Connection Pooling

```text
Instead of: 1M individual SSE connections per server
Use: Batch connections, share resources
```

3. Batching Updates

```text
Instead of: 3 separate updates (Goal + Time + Score)
Send: 1 combined update with all info
```

#### Why This Matters for L5 Interviews

Interviewers test this because:

- Shows you understand scale challenges
- Tests distributed systems thinking
- Reveals if you can identify bottlenecks
- Demonstrates practical solutions

**Red Flag Answer:** "We'll just use pub/sub" (doesn't address the fan-out) 
**Good L5 Answer:** "We need hierarchical distribution to prevent 10M fan-out from crushing any single server"

**In Your Sports App Context**:

```text
❌ Bad: Central server sends goal update to 10M users directly
✅ Good: Central → Regional → Edge → Users (hierarchical)
✅ Better: + CDN caching + Event batching + Connection pooling
```

The key insight: You can't avoid the work of delivering to 10M users, but you can distribute that work across many servers instead of crushing one server with it.

---

## Scenario 5: Online Gaming Lobby

You're designing the lobby/matchmaking system for an online game. Players need to see who's online, join/leave game rooms, and get notified when matches are found. Real-time presence updates are important, but not millisecond-critical. Peak: 1 million concurrent players.

Your task: How do you handle real-time presence and lobby updates?