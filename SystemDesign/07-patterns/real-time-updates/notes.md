# Real time updates

⚡ Real-time Updates addresses the challenge of delivering immediate notifications and data changes from servers to clients as events occur. From chat applications where messages need instant delivery to live dashboards showing real-time metrics, users expect to be notified the moment something happens. This pattern covers the architectural approaches to enable low-latency, bidirectional communication.

## The problem

Consider a collaborative document editor like Google Docs. When one user types a character, all other users viewing the document need to see that change within milliseconds. In apps like this you can't have every user constantly polling the server for updates every few milliseconds without crushing your infrastructure.

The core challenge is establishing efficient, persistent communication channels between clients and servers. Standard HTTP follows a request-response model: clients ask for data, servers respond, then the connection closes. This works great for traditional web browsing but breaks down when you need servers to proactively push updates to clients.

## The solution

When systems require real-time updates, push notifications, etc, the solution requires two distinct pieces:

- The first 'hop': How do we get updates from server to the client ?
- The second 'hop': How do we get updates from source to the server ?

![image](./imgs/real-time-updates-1.png)

We'll break down each hop separately as they involve different trade-offs which work together.

### Client server connection protocols

The first "hop" is establishing efficient communication channels between clients and servers. While traditional HTTP request-response works for a startling number of use-cases, real-time systems frequently need persistent connections or clever polling strategies to enable servers to push updates to clients. This is where we get into the nitty-gritty of networking.

#### Networking 101

Before diving into the different protocols for facilitating real-time updates, it's helpful to understand a bit about how networking works — in some sense the problems we're talking about here are just networking problems! Networks are built on a layered architecture (the so-called "OSI model") which greatly simplifies the world for us application developers who sit on top of it.

##### Networking layers

In networks, each layer builds on the abstractions of the previous one. This way, when you're requesting a webpage, you don't need to know which voltages represent a 1 or a 0 on the network wire - you just need to know how to use the next layer down the stack. While the full networking stack is fascinating, there are three key layers that come up most often in system design interviews:

- Network Layer (Layer 3): At this layer is IP, the protocol that handles routing and addressing. It's responsible for breaking the data into packets, handling packet forwarding between networks, and providing best-effort delivery to any destination IP address on the network. However, there are no guarantees: packets can get lost, duplicated, or reordered along the way.

- Transport Layer (Layer 4): At this layer, we have TCP and UDP, which provide end-to-end communication services:
  
  TCP is a connection-oriented protocol: before you can send data, you need to establish a connection with the other side. Once the connection is established, it ensures that the data is delivered correctly and in order. This is a great guarantee to have but it also means that TCP connections take time to establish, resources to maintain, and bandwidth to use.
  
  UDP is a connectionless protocol: you can send data to any other IP address on the network without any prior setup. It does not ensure that the data is delivered correctly or in order. Spray and pray!

- Application Layer (Layer 7): At the final layer are the application protocols like DNS, HTTP, Websockets, WebRTC. These are common protocols that build on top of TCP to provide a layer of abstraction for different types of data typically associated with web applications. We'll get into them in a bit!

###### Request Lifecycle

When you type a URL into your browser, several layers of networking protocols spring into action. Let's break down how these layers work together to retrieve a simple web page over HTTP. First, we use DNS to convert a human-readable domain name like hellointerview.com into an IP address like 32.42.52.62. Then, a series of carefully orchestrated steps begins:

- DNS Resolution: The client starts by resolving the domain name of the website to an IP address using DNS (Domain Name System)1.

- TCP Handshake: The client initiates a TCP connection with the server using a three-way handshake:

    SYN: The client sends a SYN (synchronize) packet to the server to request a connection.
    SYN-ACK: The server responds with a SYN-ACK (synchronize-acknowledge) packet to acknowledge the request.
    ACK: The client sends an ACK (acknowledge) packet to establish the connection.

- HTTP Request: Once the TCP connection is established, the client sends an HTTP GET request to the server to request the web page.

- Server Processing: The server processes the request, retrieves the requested web page, and prepares an HTTP response.

- HTTP Response: The server sends the HTTP response back to the client, which includes the requested web page content.

- TCP Teardown: After the data transfer is complete, the client and server close the TCP connection using a four-way handshake:
    FIN: The client sends a FIN (finish) packet to the server to terminate the connection.
    ACK: The server acknowledges the FIN packet with an ACK.
    FIN: The server sends a FIN packet to the client to terminate its side of the connection.
    ACK: The client acknowledges the server's FIN packet with an ACK.

While the specific details of TCP handshakes might seem technical, two key points are particularly relevant for system design interviews:

- First, each round trip between client and server adds latency to our request, including those to establish connections before we send our application data.
- Second, the TCP connection itself represents state that both the client and server must maintain. Unless we use features like HTTP keep-alive, we need to repeat this connection setup process for every request - a potentially significant overhead.
Understanding when connections are established and how they are managed is crucial to touching on the important choices relevant for realtime updates.

##### With Load Balancers

In real-world systems, we typically have multiple servers working together behind a load balancer. Load balancers distribute incoming requests across these servers to ensure even load distribution and high availability. There are two main types of load balancers you'll encounter in system design interviews: Layer 4 and Layer 7.

Layer 4 Load Balancers

Layer 4 load balancers operate at the transport layer (TCP/UDP). They make routing decisions based on network information like IP addresses and ports, without looking at the actual content of the packets. The effect of a L4 load balancer is as-if you randomly selected a backend server and assumed that TCP connections were established directly between the client and that server — this mental model is not far off.

For example, if a client establishes a TCP connection through an L4 load balancer, that same server will handle all subsequent requests within that TCP session. This makes L4 load balancers particularly well-suited for protocols that require persistent connections, like WebSocket connections. At a conceptual level, it's as if we have a direct TCP connection between client and server which we can use to communicate at higher layers.

Layer 7 Load Balancers

Layer 7 load balancers operate at the application layer, understanding protocols like HTTP. They can examine the actual content of each request and make more intelligent routing decisions.

For example, an L7 load balancer could route all API requests to one set of servers while sending web page requests to another (providing similar functionality to an API Gateway), or it could ensure that all requests from a specific user go to the same server based on a cookie. The underlying TCP connection that's made to your server via an L7 load balancer is not all that relevant! It's just a way for the load balancer to forward L7 requests, like HTTP, to your server.

**The choice between L4 and L7 load balancers often comes up in system design interviews when discussing real-time features. There are some L7 load balancers which explicitly support connection-oriented protocols like WebSockets, but generally speaking L4 load balancers are better for WebSocket connections, while L7 load balancers offer more flexibility for HTTP-based solutions like long polling.**

Alright, now that we covered the necessary networking concepts, let's dive into the different approaches for facilitating real-time updates between clients and servers, our first "hop". As a motivating example, let's consider a chat application where users need to receive new messages sent to the chat room they are a part of.

#### Simple Polling: The Baseline

The simplest possible approach is to have the client regularly poll the server for updates. This could be done with a simple HTTP request that the client makes at a regular interval. This doesn't technically qualify as real-time, but it's a good starting point and provides a good contrast for our other methods.

**A lot of interview questions don't actually require real-time updates. Think critically about the product and ask yourself whether lower frequency updates (e.g. every 2-5 seconds) would work. If so, you may want to propose a simple, polling-based approach. It's better to suggest a less-than-perfect solution than to fail to implement a complex one.
That said, do make this proposal to your interviewer before pulling the trigger. If they are dead-set on you talking about WebSockets, SSE, or WebRTC, you'll want to know that sooner than later!**

How does it work? It's dead simple! The client makes a request to the server at a regular interval and the server responds with the current state of the world. In our chat app, we would just constantly be polling for "what messages have I not received yet?".

```typescript
async function poll() {
  const response = await fetch('/api/updates');
  const data = await response.json();
  processData(data);
}

// Poll every 2 seconds
setInterval(poll, 2000);
```

Advantages

- Simple to implement.
- Stateless.
- No special infrastructure needed.
- Works with any standard networking infrastructure.
- Doesn't take much time to explain.

**This last point is underrated. If the crux of your problem is not real-time updates, you'll want to propose a simple, polling-based approach. You'll preserve your mental energy and interview time for the parts of the system that truly matter.**

Disadvantages

- Higher latency than other methods. Updates might be delayed as long as the polling interval + the time it takes to process the request.
- Limited update frequency.
- More bandwidth usage.
- Can be resource-intensive with many clients, establishing new connections, etc.

When to use simple polling ?

Simple polling is a great baseline and, absent a problem which specifically requires very-low latency, real-time updates, it's a great solution. It's also appropriate when the window where you need updates is short.

Things to Discuss in Your Interview

You'll want to be clear with your interviewer about the trade-offs you're making with polling vs other methods. A good explanation highlights the simplicity of the approach and gives yourself a backdoor if you discover that you need something more sophisticated. "I'm going to start with a simple polling approach so I can focus on X, but we can switch to something more sophisticated if we need to later."

The most common objection from interviewers to polling is either that it's too slow or that it's not efficient. Be prepared to discuss why the polling frequency you've chosen is appropriate and sufficient for the problem. On the efficiency front, it's great to be able to discuss how you can reduce the overhead. One way to do this is to take advantage of HTTP keep-alive connections. Setting an HTTP keep-alive which is longer than the polling interval will mean that, in most cases, you'll only need to establish a TCP connection once which minimizes some of the setup and teardown overhead.

#### Long Polling: The easy solution

After a baseline for simple polling, long polling is the easiest approach to achieving near real-time updates. It builds on standard HTTP, making it easy to implement and scale.

The idea is also simple: the client makes a request to the server and the server holds the request open until new data is available. It's as if the server is just taking really long to process the request. The server then responds with the data, finalizes the HTTP requests, and the client immediately makes a new HTTP request. This repeats until the server has new data to send. If no data has come through in a long while, we might even return an empty response to the client so that they can make another request.

- Client makes HTTP request to server
- Server holds request open until new data is available
- Server responds with data
- Client immediately makes new request
- Process repeats

```typescript
// Client-side of long polling
async function longPoll() {
  while (true) {
    try {
      const response = await fetch('/api/updates');
      const data = await response.json();
      
      // Handle data
      processData(data);
    } catch (error) {
      // Handle error
      console.error(error);
      
      // Add small delay before retrying on error
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
}
```

The simplicity of the approach hides an important trade-off for high-frequency updates. Since the client needs to "call back" to the server after each receipt, the approach can introduce some extra latency:

Advantages

- Builds on standard HTTP and works everywhere HTTP works.
- Easy to implement.
- No special infrastructure needed.
- Stateless server-side.

Disadvantages

- Higher latency than alternatives.
- More HTTP overhead.
- Can be resource-intensive with many clients.
- Not suitable for frequent updates due to the issues mentioned above.
- Makes monitoring more painful since requests can hang around for a long time.

When to Use Long Polling

Long polling is a great solution for near real-time updates with a simple implementation. It's a good choice when updates are infrequent and a simple solution is preferred. If the latency trade-off of a simple polling solution is at all an issue, long-polling is an obvious upgrade with minimal additional complexity.

Long Polling is a great solution for applications where a long async process is running but you want to know when it finishes, as soon as it finishes - like is often the case in payment processing. We'll long-poll for the payment status before showing the user a success page.

Things to Discuss in Your Interview

Because long-polling utilizes the existing HTTP infrastructure, there's not a bunch of extra infrastructure you're going to need to talk through. Even though the polling is "long", you still do need to be specific about the polling frequency. Keep in mind that each hop in your infrastructure needs to be aware of these lengthy requests: you don't want your load balancer hanging up on the client after 30 seconds when your long-polling server is happy to keep the connection open for 60 (15-30s is a pretty common polling interval that minimizes the fuss here).

#### Server-Sent Events (SSE): The Efficient One-Way Street

SSE is an extension on long-polling that allows the server to send a stream of data to the client.
Normally HTTP responses have a header like Content-Length which tells the client how much data to expect. SSE instead uses a special header Transfer-Encoding: chunked which tells the client that the response is a series of chunks - we don't know how many there are or how big they are until we send them. This allows us to move from a single, atomic request/response to a more granular "stream" of data.

With SSE, instead of sending a full response once data becomes available, the server sends a chunk of data and then keeps the request open to send more data as needed. SSE is perfect for scenarios where servers need to push data to clients, but clients don't need to send data back frequently.

In our chat app, we would open up a request to stream messages and then each new message would be sent as a chunk to the client.

How SSE works ?

- Client establishes SSE connection
- Server keeps connection open
- Server sends messages when data changes or updates happen
- Client receives updates in real-time

Modern browsers have built-in support for SSE through the EventSource object, making the client-side implementation straightforward.

```typescript
// Client-side
const eventSource = new EventSource('/api/updates');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateUI(data);
};

// Server-side (Node.js/Express example)
app.get('/api/updates', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  const sendUpdate = (data) => {
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  };

  // Send updates when data changes
  dataSource.on('update', sendUpdate);

  // Clean up on client disconnect
  req.on('close', () => {
    dataSource.off('update', sendUpdate);
  });
});
```

Advantages

- Built into browsers.
- Automatic reconnection.
- Works over HTTP.
- More efficient than long polling due to less connection initiation/teardown.
- Simple to implement.

Disadvantages

- One-way communication only.
- Limited browser support (not an issue for modern browsers).
- Some proxies and networking equipment don't support streaming. Nasty to debug!

When to Use SSE ?

SSE is a great upgrade to long-polling because it eliminates the issues around high-frequency updates while still building on top of standard HTTP. That said, it comes with lesser overall support because you'll need both browsers and and/all infra between the client and server to support streaming responses.
A very popular use-case for SSE today is AI chat apps which frequently involve the need to stream new tokens (words) to the user as they are generated to keep the UI responsive.

Things to Discuss in Your Interview

SSE rides on existing HTTP infrastructure, so there's not a lot of extra infrastructure you'll need to talk through. You also don't have a polling interval to negotiate or tune.
Most SSE connections won't be super-long-lived (e.g. 30-60s is pretty typical), so if you need to send messages for a longer period you'll need to talk about how clients re-establish connections and how they deal with the gaps in between. The SSE standard includes a "last event ID" which is intended to cover this gap, and the EventSource object in browsers explicitly handles this reconnection logic. If a client loses its connection, it can reconnect and provide the last event ID it received. The server can then use that ID to send all the events that occurred while the client was disconnected.

#### Websockets: The Full-Duplex Champion

WebSockets are the go-to choice for true bi-directional communication between client and server. If you have high frequency writes and reads, WebSockets are the champ.

How Websockets work ?

Websockets build on HTTP through an "upgrade" protocol, which allows an existing TCP connection to change L7 protocols. This is super convenient because it means you can utilize some of the existing HTTP session information (e.g. cookies, headers, etc.) to your advantage.

Once a connection is established, both client and server can send "messages" to each other which are effectively opaque binary blobs. You can shove strings, JSON, Protobufs, or anything else in there. Think of WebSockets like a TCP connection with some niceties that make establishing the connection easier, especially for browsers.

- Client initiates WebSocket handshake over HTTP
- Connection upgrades to WebSocket protocol
- Both client and server can send messages
- Connection stays open until explicitly closed

```typescript
// Client-side
const ws = new WebSocket('ws://api.example.com/socket');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleUpdate(data);
};

ws.onclose = () => {
  // Implement reconnection logic
  setTimeout(connectWebSocket, 1000);
};

// Server-side (Node.js/ws example)
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  ws.on('message', (message) => {
    // Handle incoming messages
    const data = JSON.parse(message);
    processMessage(data);
  });

  // Send updates to client
  dataSource.on('update', (data) => {
    ws.send(JSON.stringify(data));
  });
});
```

Advantages

- Full-duplex (read and write) communication.
- Lower latency than HTTP due to reduced overhead (e.g. no headers).
- Efficient for frequent messages.
- Wide browser support.

Disadvantages

- More complex to implement.
- Requires special infrastructure.
- Stateful connections, can make load balancing and scaling more complex.
- Need to handle reconnection.

When to Use WebSockets

Generally speaking, if you need high-frequency, bi-directional communication, you're going to want to use WebSocket. I'm emphasizing high-frequency here because you can always make additional requests/connections for writes: a very common pattern is to have SSE subscriptions for updates and do writes over simple HTTP POST/PUT whenever they occur.

I often find candidates too eagerly adopting Websockets when they could be using SSE or simple polling instead. Because of the additional complexity and infra lift, you'll want to defer to SSE unless you have a specific need for this bi-directional communication.

Things to Discuss in Your Interview

Websockets are a powerful tool, but they do come with a lot of complexity. You'll want to talk through how you'll manage connections and deal with reconnections. You'll also need to consider how your deployment strategy will handle server restarts.
Managing statefulness is a big part of the conversation. Senior/staff candidates will frequently talk about how to minimize the spread of state across their architecture.

There's also a lot to discuss about how to scale WebSocket servers. Load can be uneven which can result in hotspots and failures. Using a "least connections" strategy for the load balancer can help, as well as minimizing the amount of work the WebSocket servers need to do as they process messages. Using the reference architecture above and offloading more intensive processing to other services (which can scale independently) can help.

#### WebRTC: The Peer-to-Peer Solution

Our last option is the most unique. WebRTC enables direct peer-to-peer communication between browsers, perfect for video/audio calls and some data sharing like document editors.

Clients talk to a central "signaling server" which keeps track of which peers are available together with their connection information. Once a client has the connection information for another peer, they can try to establish a direct connection without going through any intermediary servers.
In practice, most clients don't allow inbound connections for security reasons (the exception would be servers which broadcast their availability on specific ports at specific addresses) using devices like NAT (network address translation). So if we stopped there, most peers wouldn't be able to "speak" to each other.

The WebRTC standard includes two methods to work around these restrictions:

- STUN: "Session Traversal Utilities for NAT" is a protocol and a set of techniques like "hole punching" which allows peers to establish publically routable addresses and ports. I won't go into details here, but as hacky as it sounds it's a standard way to deal with NAT traversal and it involves repeatedly creating open ports and sharing them via the signaling server with peers.

- TURN: "Traversal Using Relays around NAT" is effectively a relay service, a way to bounce requests through a central server which can then be routed to the appropriate peer.

#### Overview

There are a lot of options for delivering events from the server to the client. Being familiar with the trade-offs associated with each will give you the flexibility to make the best design decision for your system. If you're in a hurry, the following flowchart will help you choose the right tool for the job.

- If you're not latency sensitive, simple polling is a great baseline. You should probably start here unless you have a specific need in your system.

- If you don't need bi-directional communication, SSE is a great choice. It's lightweight and works well for many use cases. There are some infrastructure considerations to keep in mind, but they're less invasive than with WebSocket and generally interviewers are less familiar with them or less critical if you don't address them.

- If you need frequent, bi-directional communication, WebSocket is the way to go. It's more complex, but the performance benefits are huge.

- Finally, if you need to do audio/video calls, WebRTC is the only way to go. In some instances peer-to-peer collaboration can be enhanced with WebRTC, but you're unlikely to see it in a system design interview.

### Server side push/pull

Now that we've established our options for the hop from server to client (Simple Polling, Long-Polling, SSE, WebSockets, WebRTC), let's talk about how we can propagate updates from the source to the server.

Invariably our system is somehow producing updates that we want to propagate to our clients. This could be other users making edits to a shared documents, drivers making location updates, or friends sending messages to a shared chat.

Making sure these updates get to their ultimate destination is closely tied to how we propagate updates from the source to the server. Said
differently, we need a trigger.

When it comes to triggering, there's three patterns that you'll commonly see:

- Pulling via Polling
- Pushing via Consistent Hashes
- Pushing via Pub/Sub

#### Pulling with Simple Polling

With Simple Polling, we're using a pull-based model. Our client is constantly asking the server for updates and the server needs to maintain the state necessary to respond to those requests. The most common way to do this is to have a database where we can store the updates (e.g. all of the messages in the chat room), and from this database our clients can pull the updates they need when they can. For our chat app, we'd basically be polling for "what messages have been sent to the room with a timestamp larger than the last message I received?".

Advantages

- Dead simple to implement.
- State is constrained to our DB.
- No special infrastructure.
- Doesn't take much time to explain.

Disadvantages

- High latency.
- Excess DB load when updates are infrequent and polling is frequent.

When to Use Pull-Based Polling

Pull-based polling is great when you want your user experience to be somewhat more responsive to changes that happen on the backend, but responding quickly is not the main thing. Generally speaking, if you need real-time updates this is not the best approach, but again there are a lot of use-cases where real-time updates are actually not required!

Things to Discuss in Your Interview

When you're using Pull-based Polling, you'll want to talk about how you're storing the updates. If you're using a database, you'll want to discuss how you're querying for the updates and how that might change given your load.
In many instances where this approach might be used, the number of clients can actually be quite large. If you have a million clients polling every 10 seconds, you've got 100k TPS of read volume! This is easy to forget about.

#### Pushing via Consistent Hashes

The remaining approaches involve pushing updates to the clients. In many of the client update mechanisms that we discussed above (long-polling, SSE, WebSockets) the client has a persistent connection to one server and that server is responsible for sending updates to the client.
But this creates a problem! For our chat application, in order to send a message to User C, we need to know which server they are connected to.

Ideally, when an a message needs to be sent, I would:

- Figure out which server User C is connected to.
- Send the message to that server.
- That server will look up which (websocket, SSE, long-polling) request is associated with User C.
- The server will then write the message via the appropriate connection.

There are two common ways to handle this situation, and the first is to use hashing. Let's build up our intuition for this in two steps.

##### Simple hashing

Our first approach might be to use a simple modulo operation to figure out which server is responsible for a given user. Then, we'll always have 1 server who "owns" the connections for that user.

To do this, we'll have a central service that knows how many servers there are N and can assign them each a number 0 through N-1. This is frequently Apache ZooKeeper or Etcd which allows us to manage this metadata and allows the servers to keep in sync as it updates, though in practice there are many alternatives.
We'll make the server number n responsible for user u % N. When clients initially connect to our service, we can either:

- Directly connect them to the appropriate server (e.g. by having them know the hash, N, and the server addressess associated with each index).
- Have them randomly connect to any of the servers and have that server redirect them to the appropriate server based on internal data.

When a client connects, the following happens:

- The client connects to a random server.
- The server looks up the client's hash in Zookeeper to figure out which server is responsible for them.
- The server redirects the client to the appropriate server.
- The client connects to the correct server.
- The server adds that client to a map of connections.
- Now we're ready to send updates and messages!

When we want to send messages to User C, we can simply hash the user's id to figure out which server is responsible for them and send the message there.

This approach works because we always know that a single server is responsible for a given user (or entity, or ID, or whatever). All inbound connections go to that server and, if we want to use the connection associated with that entity, we know to pass it to that server for forwarding to the end client.

##### Consistent hashing

The hashing approach works great when N is fixed, but becomes problematic when we need to scale our service up or down. With simple modulo hashing, changing the number of servers would require almost all users to disconnect and reconnect to different servers - an expensive operation that disrupts service.
Consistent hashing solves this by minimizing the number of connections that need to move when scaling. It maps both servers and users onto a hash ring, and each user connects to the next server they encounter when moving clockwise around the ring.

When we add or remove servers, only the users in the affected segments of the ring need to move. This greatly reduces connection churn during scaling operations.

Advantages

- Predictable server assignment
- Minimal connection disruption during scaling
- Works well with stateful connections
- Easy to add/remove servers

Disadvantages

- Complex to implement correctly
- Requires coordination service (like Zookeeper)
- All servers need to maintain routing information
- Connection state is lost if a server fails

When to Use Consistent Hashing

Consistent hashing is ideal when you need to maintain persistent connections (WebSocket/SSE) and your system needs to scale dynamically. It's particularly valuable when each connection requires significant server-side state that would be expensive to transfer between servers.
For example, in the Google Docs design, connections are associated with specific documents that require substantial state to maintain collaborative editing functionality. Consistent hashing helps keep that state on a single server while allowing for scaling.
However, if you're just passing small messages to clients without much associated state, you're probably better off using the next approach: Pub/Sub.

#### Pushing via Pub/Sub

Another approach to triggering updates is to use a pub/sub model. In this model, we have a single service that is responsible for collecting updates from the source and then broadcasting them to all interested clients. Popular options here include Kafka and Redis.

The pub/sub service becomes the biggest source of state for our realtime updates. Our persistent connections are now made to lightweight servers which simply subscribe to the relevant topics and forward the updates to the appropriate clients. I'll refer to these servers as endpoint servers.
When clients connect, we don't need them to connect to a specific endpoint server (like we did with consistent hashing) and instead can connect to any of them. Once connected, the endpoint server will register the client with the pub/sub server so that any updates can be sent to them.

On the connection side, the following happens:

- The client establishes a connection with an endpoint server.
- The endpoint server registers the client with the Pub/Sub service, often by creating a topic, subscribing to it, and keeping a mapping from topics to the connections associated with them

On the update broadcasting side, the following happens:

- Updates are pushed to the Pub/Sub service to the relevant topic.
- The Pub/Sub service broadcasts the update to all clients subscribed to that topic.
- The endpoint server receives the update, looks up which client is subscribed to that topic, and forwards the update to that client over the existing connection.

Advantages

- Managing load on endpoint servers is easy, we can use a simple load balancer with "least connections" strategy.
- We can broadcast updates to a large number of clients efficiently.
- We minimize the proliferation of state through our system.

Disadvantages

- We don't know whether subscribers are connected to the endpoint server, or when they disconnect.
- The Pub/Sub service becomes a single point of failure and bottleneck.
- We introduce an additional layer of indirection which can add to latency.
- There exist many-to-many connections between Pub/Sub service hosts and the endpoint servers.

When to Use Pub/Sub

Pub/Sub is a great choice when you need to broadcast updates to a large number of clients. It's easy to set up and requires little overhead on the part of the endpoint servers. The latency impact is minimal (<10ms). If you don't need to respond to connect/disconnect events or maintain a lot of state associated with a given client, this is a great approach.

Things to Discuss in Your Interview

If you're using a pub/sub model, you'll probably need to talk about the single point of failure and bottleneck of the pub/sub service. Redis cluster is a popular way to scale pub/sub service which involves sharding the subscriptions by their key across multiple hosts. This scales up the number of subscriptions you can support and the throughput.

## When to Use in Interviews

Real-time updates appear in almost every system design interview that involves user interaction or live data. Rather than waiting for the interviewer to ask about real-time features, proactively identify where immediate updates matter and address them in your initial design.

A strong candidate recognizes real-time requirements early. When designing a chat application, immediately acknowledge that "messages need to be delivered instantly to all participants - I'll address that with WebSockets." For collaborative editing, mention that "character-level changes need sub-second propagation between users."

### Common Interview Scenarios

- Chat Applications - The classic real-time use case. Messages must appear instantly across all participants. WebSockets handle the bidirectional communication perfectly, while pub/sub distributes messages to the right servers. Consider message ordering, typing indicators, and presence status.

- Live Comments - High-volume, real-time social interaction during live events. Millions of viewers commenting simultaneously creates extreme fan-out problems. Hierarchical aggregation and careful batching prevent system overload while maintaining the live feel.

- Collaborative Document Editing - Character-level changes need instant propagation between users. WebSockets provide the low-latency communication, while operational transforms or CRDTs handle conflict resolution. User cursors and selection highlighting add additional real-time complexity.

- Live Dashboards and Analytics - Business metrics and operational data that changes constantly. Server-Sent Events work well for one-way data flow from servers to dashboards. Consider data aggregation intervals and what constitutes "real-time enough" for business decisions.

- Gaming and Interactive Applications - Multiplayer games need the lowest latency possible. WebRTC enables peer-to-peer communication for reduced latency, while WebSockets handle server coordination. Consider different update frequencies for different game elements.

### When NOT to Use

Avoid real-time updates when you can get away with a simple polling model. If you're not latency sensitive, polling is a great baseline and minimizes complexity — a property highly valued in senior+ interviews. By polling you avoid both hops: you don't need to worry about the client->server protocols AND you don't have to handle propagation from the event source.

## Common Deep Dives

### "How do you handle connection failures and reconnection?"

Real-world networks are unreliable. Mobile users lose connections constantly, WiFi drops out, and servers restart. Your real-time system needs graceful degradation and recovery.
The key challenge is detecting disconnections quickly and resuming without data loss. WebSocket connections don't always signal when they break - a client might think it's connected while the server has already cleaned up the connection. Implementing heartbeat mechanisms helps detect these "zombie" connections.
For recovery, you need to track what messages or updates a client has received. When they reconnect, they should get everything they missed. This often means maintaining a per-user message queue or implementing sequence numbers that clients can reference during reconnection. Using Redis streams for this is a popular option.

### "What happens when a single user has millions of followers who all need the same update?"

This is the classic "celebrity problem" in real-time systems. When a celebrity posts, millions of users need that update simultaneously. Naive approaches create massive fan-out that can crash your system.

The solution involves strategic caching and hierarchical distribution. Instead of writing the update to millions of individual user feeds, cache the update once and distribute through multiple layers. Regional servers can pull the update and push to their local clients, reducing the load on any single component.

### "How do you maintain message ordering across distributed servers?"

When multiple servers handle real-time updates, ensuring consistent ordering becomes complex. Two messages sent milliseconds apart might arrive out of order if they travel different network paths or get processed by different servers.

Vector clocks or logical timestamps help establish ordering relationships between messages. Each server maintains its own clock, and messages include timestamp information that helps recipients determine the correct order.

For critical ordering requirements, you might need to funnel all related messages through a single server or partition. This trades some scalability for consistency guarantees, but simplifies the ordering problem significantly.

## Conclusion

Real-time updates are among the most challenging patterns in system design, appearing in virtually every interactive application from messaging to collaborative editing. The key insight is that real-time systems require solving two distinct problems: client-server communication protocols and server-side update propagation.

Start simple and escalate based on requirements. If polling every few seconds meets your needs, don't jump to complex WebSocket architectures. Most candidates over-engineer real-time solutions when simpler approaches would suffice. However, when true real-time performance is required, understanding the trade-offs between protocols becomes crucial.

For client communication, SSE and WebSockets handle most real-time scenarios effectively. SSE works brilliantly for one-way updates like live dashboards, while WebSockets excel when you need bidirectional communication. Both are well-supported and understood by most infrastructure teams.

On the server side, pub/sub systems provide the best balance of simplicity and scalability for most applications. They decouple update sources from client connections, making your system easier to reason about and scale. Reserve consistent hashing approaches for scenarios where connection state management becomes a primary concern