# Websockets

Websockets are a communication protocol used to build real-time features by establishing a two-way connection between a client and a server.

Imagine an online multiplayer game where the leaderboard updates instantly as players score points, showing real-time rankings of all players.

This instantaneous update feels seamless and keeps you engaged, but how does it actually work?

The magic behind this real-time experience is often powered by WebSockets.

WebSockets enable full-duplex, bidirectional communication between a client (typically a web browser) and a server over a single TCP connection.

Unlike the traditional HTTP protocol, where the client sends a request to the server and waits for a response, WebSockets allow both the client and server to send messages to each other independently and continuously after the connection is established.

## How do web sockets work ?

The WebSocket connection starts with a standard HTTP request from the client to the server.

However, instead of completing the request and closing the connection, the server responds with an HTTP 101 status code, indicating that the protocol is switching to WebSockets.

After this handshake, a WebSocket connection is established, and both the client and server can send messages to each other over the open connection.

- Handshake: The client initiates a connection request using a standard HTTP GET request with an "Upgrade" header set to "websocket".
If the server supports WebSockets and accepts the request, it responds with a special 101 status code, indicating that the protocol will be changed to WebSocket.

- Connection: Once the handshake is complete, the WebSocket connection is established. This connection remains open until explicitly closed by either the client or the server.

- Data Transfer: Both the client and server can now send and receive messages in real-time.
These messages are sent in small packets called frames, and carry minimal overhead compared to traditional HTTP requests.

- Closure: The connection can be closed at any time by either the client or server, typically with a "close" frame indicating the reason for closure.

## Why are web sockets used ?

- Real-time Updates: WebSockets enable instant data transmission, making them perfect for applications that require real-time updates, like live chat, gaming, or financial trading platforms.

- Reduced Latency: Since the connection is persistent, there's no need to establish a new connection for each message, significantly reducing latency.

- Efficient Resource Usage: WebSockets are more efficient than traditional polling techniques, as they don't require the client to continuously ask the server for updates.

- Bidirectional Communication: Both the client and server can initiate communication, allowing for more dynamic and interactive applications.

- Lower Overhead: After the initial handshake, WebSocket frames have a small header (as little as 2 bytes), reducing the amount of data transferred.

## Websockets vs HTTP polling vs Long polling

To understand the advantages of WebSockets, it's helpful to compare them with other communication methods:

### HTTP

- Request-Response Model: In HTTP, the client sends a request, and the server responds, closing the connection afterward. This model is stateless and not suitable for real-time communication.
- Latency: Since each interaction requires a new request, HTTP has higher latency compared to WebSockets.

### Polling

- Repeated Requests: The client repeatedly sends requests to the server at fixed intervals to check for updates. While this can simulate real-time updates, it is inefficient, as many requests will return no new data.
- Latency: Polling introduces delays because updates are only checked periodically.

### Long-Polling

- Persistent Connection: In long-polling, the client sends a request, and the server holds the connection open until it has data to send. Once data is sent or a timeout occurs, the connection closes, and the client immediately sends a new request.
- Latency: This approach reduces the frequency of requests but still suffers from higher latency compared to WebSockets since it requires the client to repeatedly send new HTTP requests after each previous request is completed.
- Resource Usage: Long-polling can lead to resource exhaustion on the server as it must manage many open connections and handle frequent reconnections.

### Websocket

- Bi-Directional: Unlike HTTP, polling, and long-polling, WebSockets allow for two-way communication.
- Low Latency: Because the connection remains open, data can be sent and received with minimal delay.
- Efficiency: WebSockets are more efficient in terms of resource usage and bandwidth.

## Real world usages

- Real-Time Collaboration Tools
- Real-Time Chat Applications
- Live Notifications
- Multiplayer Online Games
- Live Streaming and Broadcasting

**In system design interviews, launching into a WebSocket implementation without justifying why they are needed is a great way to get a "thumbs down" from your interviewer. WebSockets are powerful, but the infra required to support them can be expensive and the overhead of stateful connections (especially at scale) will require significant accommodations in your design. Hold off unless you really need them!**
