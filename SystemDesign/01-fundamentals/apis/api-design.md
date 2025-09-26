# API Design

API design follows predictable patterns. You'll pick a protocol, define your resources, and specify how clients pass data and get responses back.

## API Types

- REST: REST uses standard HTTP methods (GET, POST, PUT, DELETE) to manipulate resources identified by URLs. For standard CRUD operations in web and mobile applications, REST maps naturally to your database operations and HTTP semantics, making it the go-to protocol for most web services. This should be your default choice.

- GraphQL: Unlike REST's fixed endpoints, GraphQL uses a single endpoint with a query language that lets clients specify exactly what data they need. Think about a mobile app that needs only basic user information versus a web dashboard that displays comprehensive analytics - with REST, you'd either create multiple endpoints or force clients to fetch more data than they need, but GraphQL lets each client request exactly what it needs in a single query. If your interviewer mentions "flexible data fetching" or talks about avoiding over-fetching and under-fetching, they're signaling you to consider GraphQL.

- gRPC: RPC protocols like gRPC use binary serialization and HTTP/2 for efficient communication between services. While REST treats everything as resources, RPC lets you think in terms of actions and procedures - when your user service needs to quickly validate permissions with your auth service, an RPC call like checkPermission(userId, resource) is more natural than trying to model this as a REST resource. If the interviewer specifically mentions microservices or internal APIs, consider RPC for those high-performance connections. Use RPC when performance is critical.

## REST

Since REST is your default choice, let's spend most of our time here understanding how to design REST APIs that work well in system design interviews.

### Resource modelling

The foundation of good REST API design is identifying your resources correctly. Take Ticketmaster as an example. Your core entities might be events, venues, tickets, and bookings. These naturally map to REST resources.

```shell
GET /events                    # Get all events
GET /events/{id}               # Get a specific event
GET /venues/{id}               # Get a specific venue
GET /events/{id}/tickets       # Get available tickets for an event
POST /events/{id}/bookings     # Create a new booking for an event
GET /bookings/{id}             # Get a specific booking
```

Importantly, REST resources should represent things in your system, not actions. Instead of thinking about what users can do (like "book" or "purchase"), think about what exists in your system (events, venues, tickets, bookings).

### HTTP methods

- GET is for retrieving data without changing anything. Use GET for /events/{id} to fetch event details or /events to list all events.

- POST creates new resources. When a user books tickets, you'd POST to /events/{id}/bookings with the booking details in the request body. The server assigns an ID and returns the newly created booking. POST is neither safe nor idempotent. In other words, calling it multiple times creates multiple bookings.

- PUT replaces an entire resource with what you send. If you're updating a user's profile completely, PUT to /users/{id} with the full user object. Unlike POST, PUT is idempotent, so sending the same data multiple times results in the same final state.

- PATCH updates part of a resource. When a user changes just their email address, PATCH to /users/{id} with only the email field. Like PUT, PATCH is idempotent.

- DELETE removes a resource. DELETE /bookings/{id} cancels a booking. It's idempotent - deleting an already-deleted resource should return the same result.

### Passing Data to APIs

API endpoints need input to tell the server what to do. This can be which resources to fetch, what data to update in the database, or how to filter results. Understanding where to put different types of input is crucial for designing clean, intuitive APIs.

You have three main options for passing data to your REST API, and each serves a different purpose.

- Path parameters identify which specific resource you're working with. When you want to get event details, you put the event ID in the path: /events/123. The ID is part of the URL structure itself, making it clear that you're asking for a specific event, not a collection of events. Use path parameters when the value is required to identify the resource - without it, the request doesn't make sense.

- Query parameters filter, sort, or modify how you retrieve resources. When you want to search for events in a specific city or date range, you use query parameters: /events?city=NYC&date=2024-01-01. These are optional - you could ask for all events without any filters, or apply multiple filters together. Query parameters work well for pagination too: /events?page=2&limit=20. Note that the first option is separated via a ? and all subsequent parameters are separated by &.

- Request body contains the actual data you're sending to create or update resources. When a user books tickets, you POST to /events/{id}/bookings with the booking details in the request body. Things like how many tickets, seating preferences, and so on. The request body is where you put complex data structures and anything that might be too large or sensitive for a URL.

Each type of input serves a different role in the API's contract. Path parameters are structural, they determine which endpoint you're hitting. Query parameters are modifiers, they change how the endpoint behaves. Request body is payload, it's the data you're actually working with.

### Returning data

An API response is made up of two parts:

- The status code, which indicates whether the request was successful or not.
- The response body, which contains the data you're returning to the client (typically JSON).

For status codes, stick to the common ones: 200 for success, 201 for created resources, 400 for bad requests, 401 for authentication required, 404 for not found, and 500 for server errors.

## GraphQL

GraphQL emerged from Facebook in 2012 to solve a specific problem: their mobile app needed different data than their web app, but they were stuck with REST endpoints that returned fixed data structures. The mobile team kept asking for new endpoints or modifications to existing ones and this was slowing down development on both sides.

With REST, you typically have two unpleasant choices when different clients need different data. You can create multiple endpoints for different use cases, leading to endpoint proliferation and maintenance headaches. Or you can make your endpoints return everything any client might need, leading to over-fetching where mobile clients download megabytes of data they don't use.

GraphQL consolidates resource endpoints into a single endpoint that accepts queries describing exactly what data you want. The client specifies the shape of the response, and the server returns data in that exact format.

### How GraphQL works ?

Here's a simple example using our Ticketmaster scenario. Instead of separate REST endpoints for events, venues, and tickets, you'd have a single GraphQL endpoint that can handle queries like this:

```shell
query {
  event(id: "123") {
    name
    date
    venue {
      name
      address
    }
    tickets {
      section
      price
      available
    }
  }
}
```

### When to Use GraphQL in Interviews ?

- GraphQL is the right choice when you have diverse clients with different data needs. If your interviewer mentions scenarios like "the mobile app needs different data than the web app" or asks about "avoiding over-fetching and under-fetching," they're likely looking for you to bring up GraphQL.

### GraphQL Schema Design

For our Ticketmaster example, you'd start by modeling your core entities as GraphQL types

```shell
type Event {
  id: ID!
  name: String!
  date: DateTime!
  venue: Venue!
  tickets: [Ticket!]!
}

type Venue {
  id: ID!
  name: String!
  address: String!
}

type Query {
  event(id: ID!): Event
  events(limit: Int, after: String): [Event!]!
}
```

`In interviews, mention GraphQL when you see clear over-fetching or under-fetching problems, but don't default to it. Most interviewers appreciate that you know about GraphQL, but they usually prefer to see you solve the core architectural challenges with simpler tools first.`

## gRPC

RPC (Remote Procedure Call) is a protocol that allows a client to call a procedure on a server and wait for a response without the client having to understand the underlying network details. It's faster than HTTP for service communication, especially when you need high performance and low latency.

### When to Use RPC in Interviews ?

RPC shines in microservice architectures where services need to communicate frequently and efficiently. If your interviewer mentions internal service communication, high-performance requirements, or polyglot environments (different services in different languages), RPC is likely a good choice.

Consider RPC when:

- Performance is critical: Binary serialization and HTTP/2 make RPC significantly faster than JSON REST
- Type safety matters: Generated client code prevents many runtime errors
- Service-to-service communication: Internal APIs between your own services don't need REST's resource semantics
- Streaming is needed: gRPC supports bidirectional streaming for real-time features

For our Ticketmaster example, you might use REST APIs for your public endpoints that mobile apps and web clients consume, but use gRPC for internal communication between your booking service, payment service, and inventory service.

## Common API patterns

Regardless of whether you choose REST, GraphQL, or RPC, there are some patterns that apply across all API types.

### Pagination

When you're dealing with large datasets, you can't return everything at once. Imagine an API that returns all events ever created, that could be millions of records which would be many gigabytes of data.
Instead, you need pagination to break large result sets into manageable chunks. There are two main approaches to pagination: offset-based and cursor-based.

- Offset-based Pagination

Offset-based pagination is the simplest approach and used by most websites. You specify how many records to skip and how many to return: /events?offset=20&limit=10 gets records 21-30. This is intuitive and easy to implement, but it has problems with large datasets. If someone adds a new event while you're paginating through results, you might see duplicates or miss records as the data shifts.

- Cursor-based Pagination

Cursor-based pagination solves this by using a pointer to a specific record instead of counting from the beginning. Here's how it works in practice:
First request: /events?limit=10
Response includes the events plus a cursor pointing to the last record:

```shell
{
  "events": [...],
  "next_cursor": "cmd9atj3p000007ky19w1dpy2"
}
```

`Next request: /events?cursor=cmd9atj3p000007ky19w1dpy2&limit=10`

### Versioning Strategies

APIs evolve over time, and you need a strategy for handling changes without breaking existing clients. This is particularly important for public APIs where you can't control when clients update their code

The most common approach is URL versioning, where you include the version number in the path: /v1/events or /v2/events. This is explicit and easy to understand. Clients know exactly which version they're using just by looking at the URL. It's also simple to implement since you can route different versions to different code paths.

Header versioning puts the version in an HTTP header instead: Accept-Version: v2 or API-Version: 2. This keeps URLs cleaner and follows HTTP standards better, but it's less obvious to developers and harder to test in browsers.

For interviews, URL versioning is usually the safer choice because it's more widely understood and easier to explain quickly. Unless the interviewer specifically asks about header versioning, stick with the URL approach.
