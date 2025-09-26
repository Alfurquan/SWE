# Service discovery

## What is Service Discovery?

Service discovery is a mechanism that allows services in a distributed system to find and communicate with each other dynamically.

Service discovery registers and maintains a record of all your services in a service registry. This service registry acts as a single source of truth that allows your services to query and communicate with each other.

## Service Registration Options

Service registration is the process where a service announces its availability to a service registry, making it discoverable by other services.

### Manual registration

In manual registration, service details are added to the registry manually by a developer or operator. This approach is simple but not suitable for dynamic systems where services scale or move frequently.

### Self registration

In self-registration, the service is responsible for registering itself with the service registry when it starts. The service includes logic to interact with the registry, such as sending API requests to register its details.

#### How it works ?

- When a service or an instance starts, it retrieves its own network information (e.g., IP address, port).
- It sends a registration request to the service registry (e.g., via HTTP or gRPC).
- To ensure the registry has up-to-date information, the service may periodically send heartbeat signals to confirm it is active and healthy.

### Third-Party Registration (Sidecar Pattern)

In third-party registration, an external agent or "sidecar" process handles service registration. The service itself does not directly interact with the registry. Instead, the sidecar detects the service and registers it on its behalf.

#### How it works ?

- The sidecar runs alongside the service (e.g., in the same container or on the same host).
- The sidecar detects when the service starts and gathers its network details.
- It sends the registration request to the service registry.

### Automatic Registration by Orchestrators

In modern orchestrated environments like Kubernetes, service registration happens automatically. The orchestration platform manages the lifecycle of services and updates the service registry as services start, stop, or scale.

## Types of service discovery

### Client-Side Discovery

In this model, the responsibility for discovering and connecting to a service lies entirely with the client.

#### How does this work ?

- Service Registration: Services (e.g., UserService, PaymentService) register themselves with a centralized service registry.
They provide their network details (IP address and port) along with metadata like service health or version.

- Client Queries the Registry: The client (a microservice or API gateway) sends a request to the service registry to find the instances of a target service (e.g., PaymentService). The registry responds with a list of available instances, including their IP addresses and ports.

- Client Routes the Request: Based on the information retrieved, the client selects one of the service instances (often using a load balancing algorithm) and connects directly to it.

#### Example Workflow

Let’s consider a real-world example of a food delivery app:

- A Payment Service has three instances running on different servers.
- When the Order Service needs to process a payment, it queries the service registry for the location of the Payment Service.
- The service registry responds with a list of available instances (e.g., IP1:Port1, IP2:Port2, IP3:Port3).
- The Order Service chooses an instance (e.g., IP1:Port1) and sends the payment request directly to it.

### Server-Side Discovery

In this model, the client delegates the responsibility of discovering and routing requests to a specific service instance to a centralized server or load balancer.

Unlike client-side discovery, the client does not need to query the service registry directly or perform any load balancing itself.

#### How does it work ?

- Service Registration: Services register themselves with a centralized service registry, similar to client-side discovery.
The service registry keeps track of all service instances, their IP addresses, ports, and metadata.

- Client Sends Request: The client sends a request to a load balancer or API gateway, specifying the service it wants to communicate with (e.g., payment-service).
The client does not query the service registry or know the specific location of the service instances.

- Server Queries the Service Registry: The load balancer or gateway queries the service registry to find available instances of the requested service.

- Routing: The load balancer selects a suitable service instance (based on factors like load, proximity, or health) and routes the client’s request to that instance.

- Response: The service instance processes the request and sends the response back to the client via the load balancer or gateway.

#### Workflow example

Let’s take an example of an e-commerce platform with microservices for "Order Management" and "Payment Processing."

- Registration: The PaymentService registers two instances with the service registry:
Instance 1: IP1:8080
Instance 2: IP2:8081

- Client Request: The OrderService sends a request to the load balancer or API gateway, specifying the PaymentService.

- Discovery and Routing: The load balancer queries the service registry and retrieves the list of available PaymentService instances.
It selects one instance (e.g., IP1:8080) and routes the request to it.

- Processing and Response: The selected instance of PaymentService processes the request and sends the response back to the OrderService via the load balancer.
