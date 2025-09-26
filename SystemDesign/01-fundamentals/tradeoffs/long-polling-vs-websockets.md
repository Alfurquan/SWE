# Long polling vs Web sockets

Whether you are playing an online game or chatting with a friend—updates appear in real-time without hitting “refresh”.

Behind these seamless experiences lies a critical engineering decision: how to push real-time updates from servers to clients.

The traditional HTTP model was designed for request-response: "Client asks, server answers.". But in many real-time systems, the server needs to talk first and more often.

This is where Long Polling and WebSockets come into play—two popular methods for achieving real-time updates

## Why Traditional HTTP Isn’t Enough

HTTP, the backbone of the web, follows a client-driven request-response model:

- The client (e.g., a browser or mobile app) sends a request to the server.
- The server processes the request and sends back a response.
- The connection closes.

This model is simple and works for many use-cases, but it has limitations:

- No automatic updates: With plain HTTP, the server cannot proactively push data to the client. The client has to request the data periodically.
- Stateless nature: HTTP is stateless, meaning each request stands alone with no persistent connection to the server. This can be problematic if you need continuous exchange of data.

## Long polling

Long polling is a technique that mimics real-time behavior by keeping HTTP requests open until the server has data.

Long Polling is an enhancement over traditional polling. In regular polling, the client repeatedly sends requests at fixed intervals (e.g., every second) to check for updates. This can be wasteful if no new data exists.

Long Polling tweaks this approach: the client asks the server for data and then “waits” until the server has something new to return or until a timeout occurs

### How does long polling work ?

- Client sends a request to the server asking for new data
- Server holds the request open till it has new data to send or timeout is reached.
- Once client gets a response - new data or timeout, it immediately sends a request to the server to keep connection loop going.

### Pros

- Simple to implement

### Cons

- Resource heavy
- Higher latency

## Web sockets

WebSockets provide a full-duplex, persistent connection between the client and the server. Once established, both parties can send data to each other at any time, without the overhead of repeated HTTP requests.

### How do websockets work ?

- Handshake: Client sends an HTTP request with Upgrade: websocket.
- Connection: If supported, the server upgrades the connection to WebSocket (switching from http:// to ws://). After the handshake, client and server keep a TCP socket open for communication.
- Full-Duplex Communication: Once upgraded, data can be exchanged bidirectionally in real time until either side closes the connection.

### Pros of websockets

- Ultra low latency
- Lower overhead

### Cons of websockets

- Complex setup
- Some proxies or firewalls do not allow websockets

## Choosing right solution

### Complexity and Support

- Long Polling is easier to implement using standard libraries. Any environment that supports HTTP can handle it, often without extra packages.

- WebSockets require a bit more setup and a capable proxy environment (e.g., support in Nginx or HAProxy). However, many frameworks (e.g., Socket.io) simplify the process significantly.

### Scalability and Performance

- Long Polling can become resource-intensive with a large number of simultaneous clients, due to multiple open connections waiting on the server side.

- WebSockets offer a more efficient, persistent connection and scale better for heavy, frequent data streams.

### Type of Interaction

- Long Polling fits scenarios where data updates aren’t super frequent. If new data arrives every few seconds or minutes, long polling might be enough.

- WebSockets are better for high-frequency updates or two-way communication (e.g., multiple participants editing a document or interacting in a game).

**While both achieve real-time communication, WebSockets are generally more efficient for truly real-time applications, while Long Polling can be simpler to implement for less demanding scenarios.**
