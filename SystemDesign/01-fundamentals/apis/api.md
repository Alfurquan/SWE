# API

API stands for Application Programming Interface.

At its core, an API is a bunch of code that takes an input and gives you predictable outputs.

When engineers build APIs, they clearly define what inputs the API accepts and what outputs it produces, ensuring consistent behavior across different applications.

APIs follow a simple request-response model:

- A client (such as a web app or mobile app) makes a request to an API.
- The API (hosted on an API server) processes the request, interacts with the necessary databases or services, and prepares a response.
- The API sends the response back to the client in a structured format (usually JSON or XML).

Most applications follow the frontend/backend architecture, where:

- The backend consists of APIs that handle data processing, business logic, and communication with databases.
- The frontend is a graphical user interface (GUI) that interacts with these APIs, making applications user-friendly and accessible without requiring users to write code.

## Real world example

Let’s break this down with a real-world example: Uber.

### Backend

Before the Uber app existed as a sleek, user-friendly experience, the company first built the core APIs that power ride-hailing services:

- Finding Nearby Drivers
- Calculating Fares & Routes
- Process Payment
- Real-Time Tracking
- Matching Riders & Drivers

These APIs run on Uber’s servers, forming the backend infrastructure. Every time you request a ride, track your driver, or make a payment, these backend APIs handle the request.

### Frontend

The backend APIs handle all the complex logic, but they only work through code—which isn't practical for everyday users. That’s why companies build a frontend (user interface) on top of these APIs, allowing users to interact with the system visually and intuitively.

Example: When you enter your pickup & destination address, the frontend sends an API request to find nearby drivers and displays available cars.

## API Communication Methods

APIs communicate using different protocols and architectures that define how requests are sent, how responses are formatted, and how data is exchanged between systems.

### REST (Representational State Transfer)

REST is the most widely used API communication method today. It is lightweight, stateless, and scalable, making it perfect for web services and mobile applications.

REST APIs follow a set of design principles and use HTTP methods (GET, POST, PUT, DELETE) to perform operations.

REST APIs are based on resources, and each resource is accessed through a URL (endpoint). The API follows the client-server model, meaning the client sends a request, and the server processes it and sends a response.

### GraphQL

GraphQL is an alternative to REST that allows clients to request exactly the data they need, making it more efficient for modern applications. Unlike REST, which requires multiple API calls to fetch related data, GraphQL can fetch all necessary data in a single request.

Instead of predefined endpoints, GraphQL exposes a single API endpoint, and the client sends queries to request specific fields.

### gRPC

gRPC (Google Remote Procedure Call) is a high-performance API communication method that uses Protocol Buffers (Protobuf) instead of JSON or XML, making it faster and more efficient.

gRPC uses binary data format instead of text-based formats, reducing payload size and it supports bidirectional streaming, meaning the client and server can send data at the same time.
