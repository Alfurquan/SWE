# Whatsapp

Whatsapp is a messaging service that allows users to send and receive encrypted messages and calls from their phones and computers. Whatsapp was famously originally built on Erlang (no longer!) and renowned for handling high scale with limited engineering and infrastructure outlay.

## Functional Requirements

Apps like WhatsApp and Messenger have tons of features, but your interviewer doesn't want you to cover them all. The most obvious capabilities are almost definitely in-scope but it's good to ask your interviewer if they want you to move beyond. Spending too much time in requirements will make it harder for you to give detail in the rest of the interview, so we won't dawdle too long here!

Core requirements:

- Users should be able to start group chats with multiple participants (limit 100).
- Users should be able to send/receive messages.
- Users should be able to receive messages sent while they are not online (up to 30 days).
- Users should be able to send/receive media in their messages.

Below the line (out of scope):

- Audio/Video calling.
- Interactions with businesses.
- Status updates.
- Voice messages.
- Registration and profile management.
- Message reactions, replies, and quoting.
- Message editing and deletion.

## Non-Functional Requirements

Core requirements:

- Messages should be delivered to available users with low latency, < 500ms.
- We should guarantee deliverability of messages - they should make their way to users.
- The system should be able to handle billions of users with high throughput (we'll estimate later).
- Messages should be stored on centralized servers no longer than necessary.
- The system should be resilient against failures of individual components.

Below the line (out of scope):

- Exhaustive treatment of security concerns.
- Spam and scraping prevention systems.

## Core Entities

**Interviewers aren't evaluating you on what you list for core entitites, they're an intermediate step to help you reason through the problem. That doesn't mean they don't matter though! Getting the entities wrong is a great way to start building on a broken foundation - so spend a few moments to get them right and keep moving.**

We can walk through our functional requirements to get an idea of what the core entities are. We need:

- Users
- Chats (2-100 users)
- Messages
- Clients (a user might have multiple devices)

## API design

Next, we'll want to think through the API of our system. Unlike a lot of other products where a REST API is probably appropriate, for a chat app, we're going to have high-frequency updates being both sent and received. This is a perfect use case for a bi-directional socket connection!

```text
WebSocket connections and real-time messaging demonstrate the broader real-time updates pattern used across many distributed systems. Whether it's chat messages, live dashboards, collaborative editing, or gaming, the same principles apply: persistent connections for low latency, pub/sub for scaling across servers, and careful state management for reliability.
```

For this interview, we'll just use websockets although a simple TLS connection would do. The idea will be that users will open the app and connect to the server, opening this socket which will be used to send and receive commands which represent our API.

- First, let's be able to create a chat.

```json
// -> createChat
{
    "participants": [],
    "name": ""
} -> {
    "chatId": ""
}
```

- Now we should be able to send messages on the chat.

```json
// -> sendMessage
{
    "chatId": "",
    "message": "",
    "attachments": []
} -> "SUCCESS" | "FAILURE"
```

- We need a way to create attachments (note: I'm going to amend this later in the writeup).

```json
// -> createAttachment
{
    "body": ...,
    "hash": 
} -> {
    "attachmentId": ""
}
```

- And we need a way to add/remove users to the chat.

```json
// -> modifyChatParticipants
{
    "chatId": "",
    "userId": "",
    "operation": "ADD" | "REMOVE"
} -> "SUCCESS" | "FAILURE"
```

- When a chat is created or updated ...

```json
// <- chatUpdate
{
    "chatId": "",
    "participants": [],
} -> "RECEIVED"
```

- When a message is received

```json
// <- newMessage
{
    "chatId": "",
    "userId": ""
    "message": "",
    "attachments": []
} -> "RECEIVED"
```

Note that enumerating all of these APIs can take time! In the actual interview, I might shortcut by only writing the command names and not the full API. It's also usually a good idea to summarize the API initially before you build out the high-level design in case things need to change. "I'll come back to this as I learn more" is completely acceptable!

Our whiteboard might look something like this:

Commands Sent

- createChat
- sendMessage
- createAttachment
- modifyParticipants

Commands Received

- chatUpdate
- newMessage

## High-Level Design

### Users should be able to start group chats with multiple participants (limit 100)

For our first requirement, we need a way for a user to create a chat. We'll start with a simple service behind an L4 load balancer (to support Websockets!) which can write Chat metadata to a database. Let's use DynamoDB for fast key/value performance and scalability here, although we have lots of other options.

The steps here are:

- User connects to the service and sends a createChat message.
- The service, inside a transaction, creates a Chat record in the database and creates a ChatParticipant record for each user in the chat.
- The service returns the chatId to the user.

On the chat table, we'll usually just want to look up the details by the chat's ID. Having a simple primary key on the chat id is good enough for this.

For the ChatParticipant table, we'll want to be able to (1) look up all participants for a given chat and (2) look up all chats for a given user.

- We can do this with a composite primary key on the chatId and participantId fields. A range lookup on the chatId will give us all participants for a given chat.

- We'll need a Global Secondary Index (GSI) with participantId as the partition key and chatId as the sort key. This will allow us to efficiently query all chats for a given user. The GSI will automatically be kept in sync with the base table by DynamoDB.

### Users should be able to send/receive messages

To allow users to send/receive messages, we're going to need to start taking advantage of the websocket connection that we established. To keep things simple while we get off the ground, let's assume we have a single host for our Chat Server.

This is obviously a terrible solution for scale (and you might say so to your interviewer to keep them from itching), but it's a good starting point that will allow us to incrementally solve those problems as we go.

```text
For infrastructure-style interviews, I highly recommend reasoning 
about a solution on a single host first. 
Oftentimes the path to scale is straightforward from there.
On the other hand if you solve scale first without thinking about how the actual mechanics of your solution work underneath, 
you're likely to back yourself into a corner.
```

When users make Websocket connections to our Chat Server, we'll want to keep track of their connection with a simple hash map which will map a user id to a websocket connection. This way we know which users are connected and can send them messages.

To send a message:

- User sends a sendMessage message to the Chat Server.
- The Chat Server looks up all participants in the chat via the ChatParticipant table.
- The Chat Server looks up the websocket connection for each participant in its internal hash table and sends the message via each connection.

We're making some really strong assumptions here! We're assuming all users are online, connected to the same Chat Server, and that we have a websocket connection for each of them. But under those conditions we're moving, so let's keep going.

### Users should be able to receive messages sent while they are not online (up to 30 days).

With our next requirement, we're forced to undo some of those assumptions. We're going to need to start storing messages in our database so that we can deliver them to users even when they're offline. We'll take this as an opportunity to add some robustness to our system.

Let's keep an "Inbox" for each user which will contain all undelivered messages. When messages are sent, we'll write them to the inbox of each recipient user. If they're already online, we can go ahead and try to deliver the message immediately. If they're not online, we'll store the message and wait for them to come back later.

So, to send a message:

- User sends a sendMessage message to the Chat Server.
- The Chat Server looks up all participants in the chat via the ChatParticipant table.
- The Chat Server creates a transaction which both (a) writes the message to our Message table and (b) creates an entry in our Inbox table for each recipient.
- The Chat Server returns a SUCCESS or FAILURE to the user with the final message id.
- The Chat Server looks up the websocket connection for each participant and attempts to deliver the message to each of them via newMessage.
- (For connected clients) Upon receipt, the client will send an ack message to the Chat Server to indicate they've received the message. The Chat Server will then delete the message from the Inbox table.

For clients who aren't connected, we'll keep the messages in the Inbox table. Once the client connects to our service later, we'll:

- Look up the user's Inbox and find any undelivered message IDs.
- For each message ID, look up the message in the Message table.
- Write those messages to the client's connection via the newMessage message.
- Upon receipt, the client will send an ack message to the Chat Server to indicate they've received the message.
- The Chat Server will then delete the message from the Inbox table.

Finally, we'll need to periodically clean up the old messages in the Inbox and messages tables. We can do this with a simple cron job which will delete messages older than 30 days.

### Users should be able to send/receive media in their messages.

Our final requirement is that users should be able to send/receive media in their messages.
Users sending and receiving media is annoying. It's bandwidth- and storage- intensive. While we could potentially do this with our Chat Server and database, it's better to use purpose-built technologies for this. This is in fact how Whatsapp actually works: attachments are uploaded via a separate HTTP service.

- Bad Solution: Store attachments directly in the Message table as blobs.

- Good Solution: A straightforward approach is to have the Chat Server accept the attachment media, then push it off to blob storage with a TTL of 30 days (remember we don't need to keep messages forever!).
Users who want to retrieve a particular attachment can then query the blob storage directly (via a pre-signed URL for authorization). Ideally, we'd find a way to expire the media once it had been received by all recipients. While we could put a CDN in front of our blob storage, since we're capped at 100 participants the cache benefits are going to be relatively small.

- Best Solution: A better approach is to have the client upload the attachment directly to blob storage. This way we don't need to handle the bandwidth of the upload at all! The client can request a pre-signed URL from the Chat Server, then upload the media directly to blob storage. Once uploaded, the user will have a URL for the attachment which they can send to the Chat Server as an opaque URL.

## Deep dives

### How can we handle billions of simultaneous users?

Our single-host system is convenient but unrealistic. Serving billions of users via a single machine isn't possible and it would make deployments and failures a nightmare. So what can we do? The obvious answer is to try to scale out the number of Chat Servers we have.
If we have 1b users, we might expect 200m of them to be connected at any one time. Whatsapp famously served 1-2m users per host, but this will require us to have hundreds of chat servers. That's a lot of simultaneous connections (!).

**Note that I've included some back-of-the-envelope calculations here. Your interviewer will likely expect them, but you'll get more mileage from your calculations by doing them just-in-time: when you need to figure out a scaling bottleneck.**

Adding more chat servers also introduces some new problems: now the sending and receiving users might be connected to different hosts. If User A is trying to send a message to User B and C, but User B and C are connected to different Chat Servers, we're going to have a problem.

- Good solution: Consistent hashing. We can use consistent hashing to map users to Chat Servers. Another approach for us to use is to always assign users to a specific Chat Server based on their user ID. If we do this correctly, we'll always know which Chat Server is responsible for a given user so, when we need to send them messages, we can do so directly.
To do this we'll need to keep a central registry of how many Chat Servers we have, their addresses, and the which segments of a consistent hash space they own. We might use a service like ZooKeeper or Etcd to do this.
When a request comes in, we'll connect them to the Chat Server they are assigned to based on their user id. When a new event is created, Chat Servers will connect directly with the Chat Server that "owns" that user id, then call an API which delivers a notification the connected user (if they're connected).

- Best solution: Offload to a Pub/Sub system. A better approach is to use a Pub/Sub system to decouple the Chat Servers from each other. When a user connects, the Chat Server will subscribe to a topic for that user id. When a message is sent, the Chat Server will publish the message to the topics for each recipient user id. The Pub/Sub system will then deliver the message to the appropriate Chat Server which can then deliver it to the connected user.

### What do we do to handle multiple clients for a given user?

To this point we've assumed a user has a single device, but many users have multiple devices: a phone, a tablet, a desktop or laptop - maybe even a work computer. Imagine my phone had received the latest message but my laptop was off. When I wake it up, I want to make sure that all of the latest messages are delivered to my laptop so that it's in sync. We can no longer rely on the user-level "Inbox" table to keep track of delivery!

Having multiple clients/devices introduces some new problems:

- First, we'll need to add a way for our design to resolve a user to 1 or more clients that may be active at any one time.
- Second, we need a way to deactivate clients so that we're not unnecessarily storing messages for a client which does not exist any longer.
- Lastly, we need to update our message delivery system so that it can handle multiple clients.

Let's see if we can account for this with minimal changes to our design.

- We'll need to create a new Clients table to keep track of clients by user id.
- When we look up participants for a chat, we'll need to look up all of the clients for that user.
- We'll need to update our Inbox table to be per-client rather than per-user.
- When we send a message, we'll need to send it to all of the clients for that user.
- On the pub/sub side, nothing needs to change. Chat servers will continue to subscribe to a topic with the userId.

We'll probably want to introduce some limits (3 clients per account) to avoid blowing up our storage and throughput.
