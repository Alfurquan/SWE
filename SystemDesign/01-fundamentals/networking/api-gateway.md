# API Gateway

APIs, or Application Programming Interfaces, are a set of rules and protocols that allows two software applications or services to communicate with each other.

An API Gateway acts as a central server that sits between clients (e.g., browsers, mobile apps) and backend services.
Instead of clients interacting with multiple microservices directly, they send their requests to the API Gateway. The gateway processes these requests, enforces security, and forwards them to the appropriate microservices.

## Why Do We Need an API Gateway?

Modern applications, especially those built using microservices architecture, have multiple backend services managing different functionalities.

For example, in an e-commerce service:

- One service handles user accounts.
- Another handles payments.
- Another manages product inventory.

Without an API Gateway:

- Clients would need to know the location and details of all backend services.
- Developers would need to manage authentication, rate limiting, and security for each service individually.

With an API Gateway:

- Clients send all requests to one place – the API Gateway.
- The API Gateway takes care of routing, authentication, security, and other operational tasks, simplifying both client interactions and backend management.

## Core features of an API Gateway

- Authentication and Authorization: API Gateway secures the backend systems by ensuring only authorized users and clients can access backend services. It handles tasks like:
**Authentication:** Verifying the identity of the client using tokens (e.g., OAuth, JWT), API keys, or certificates.
**Authorization:** Checking the client’s permissions to access specific services or resources.
By centralizing these tasks, the API gateway eliminates the need for individual services to handle authentication, reducing redundancy and ensuring consistent access control across the system.

- Rate Limiting: To prevent abuse and ensure fair usage of resources, most API Gateways implement rate limiting. For example, a public API might allow a maximum of 100 requests per minute per user. If a client exceeds this limit, the API Gateway will block additional requests until the rate resets.

- Load Balancing: High-traffic applications rely on load balancing to distribute incoming requests evenly across multiple instances of a service.

- Caching: To improve response times and reduce the strain on backend services, most API Gateways provide caching. Caching helps in reducing latency and enhancing user experience while lowering the operational cost of backend services.

- Request Transformation: In systems with diverse clients and backend services, request transformation is essential for compatibility.For instance, it might convert XML responses from a legacy service into JSON for modern frontend applications.

- Circuit Breaking: Circuit breaking is a mechanism that temporarily stops sending requests to a backend service when it detects persistent failures, such as:
Slow responses or timeouts.
Server errors (e.g., HTTP 500 status codes).
High latency or unavailability of a service.
The API Gateway continuously monitors the health and performance of backend services and uses circuit breaking to block requests to a failing service.

## How does an API Gateway work ?

Imagine you're using a food delivery app to order dinner. When you tap "Place Order" your phone makes an API request. But instead of talking directly to various backend services, it communicates with an API Gateway first.

### Step 1: Request Reception

When you tap "Place Order," the app sends a request to the API Gateway, asking it to process your order.

This request includes things like:

- Your user ID
- Selected restaurant and menu items
- Delivery address
- Payment method
- Authentication tokens

The API Gateway receives the request as the single entry point to the backend system.

### Step 2: Request Validation

Before forwarding the request, the API Gateway validates it to ensure:

- The required parameters or headers are present.
- The data is in the correct format (e.g., JSON).
- The request conforms to the expected structure or schema.

```javascript
// Example of initial request handling
app.post('/api/v1/orders', async (req, res) => {
  // Check if request has required headers
  if (!req.headers['content-type'].includes('application/json')) {
    return res.status(400).send('Invalid content type');
  }
  // Continue processing...
});
```

If any information is missing or incorrect, the gateway immediately rejects the request and notifies the app with an appropriate error message.

### Step 3: Authentication & Authorization

The gateway now verifies your identity and permissions to ensures only legitimate users can place orders:

- It forwards your authentication token (e.g., OAuth or JWT) to an identity provider to confirm your identity.
- It checks your permissions to ensure you’re authorized to use the app for placing an order.

```javascript
const authenticateRequest = async (req) => {
  // Extract JWT token from header
  const token = req.headers.authorization?.split(' ')[1];

  // Verify token and get user details
  const user = await verifyToken(token);

  // Check if user has permission to place orders
  return user.permissions.includes('place_orders');
};
```

If authentication or authorization fails, the API Gateway sends a 401 Unauthorized or 403 Forbidden error back to the app.

### Step 4: Rate Limiting

To prevent abuse, the API Gateway checks how many requests you’ve made recently. For example:

If you’ve made 10 "Place Order" requests in the last minute (maybe by accident), the gateway might block additional requests temporarily and return 429 Too Many Requests response.

```javascript
const checkRateLimit = async (userId) => {
  const key = `rate_limit:order:${userId}`;
  const current = await redis.incr(key);

  // If first request in window, set expiry
  if (current === 1) {
    await redis.expire(key, 60); // 1 minute window
  }

  return current <= 10; // Allow 10 order requests per minute
};
```

### Step 5: Request Transformation (if needed)

If any of these backend services require specific data formats or additional details, the API Gateway transforms the request.
For example: The app sends the delivery address in plain text, but the Delivery Service expects GPS coordinates. The API Gateway converts the address into coordinates before forwarding the request.

```javascript
const transformRequest = async (originalRequest) => {
  const address = originalRequest.deliveryAddress;

  // Convert address to GPS coordinates using a geocoding API
  const coordinates = await getCoordinatesFromAddress(address);

  if (!coordinates) {
    throw new Error('Failed to fetch GPS coordinates');
  }

  // Transform the request for the Delivery Service
  return {
    orderId: originalRequest.orderId,
    customerName: originalRequest.customerName,
    deliveryLocation: {
      latitude: coordinates.lat,
      longitude: coordinates.lng
    },
    deliveryInstructions: originalRequest.instructions || ""
  };
};
```

### Step 6: Request Routing

The API Gateway now needs to coordinate several backend services to process your order.

Using service discovery, it identifies:

- Order Service: To create a new order record.
- Inventory Service: To check if the restaurant has your selected items available.
- Payment Service: To process your payment.
- Delivery Service: To assign a delivery driver to your order.

The gateway dynamically routes the request to these services using a load balancing algorithm, ensuring it connects to available and healthy service instances.

```javascript
const routeRequest = async (req, serviceType) => {
  // Get service registry
  const services = await serviceDiscovery.getServices(serviceType);

  // Select instance
  const targetService = selectServiceInstance(services);

  // Forward request
  return await axios.post(
    `${targetService.url}/api/orders`,
    req.body,
    { headers: req.headers }
  );
};
```

### Step 7: Response Handling

Once the API Gateway receives the response(s) from the backend service(s), it performs the following tasks:

- Transformation: Adjusts the response format or structure to match the client’s requirements.
- Caching (Optional): Stores the response temporarily for frequently accessed data, reducing future latency.

```javascript
const handleResponse = async (serviceResponse) => {
  // Transform response if needed
  const transformedResponse = {
    orderId: serviceResponse.order_reference,
    estimatedDelivery: serviceResponse.eta,
    status: serviceResponse.current_status
  };

  // Cache response if applicable
  if (serviceResponse.cacheable) {
    await cacheResponse(
      transformedResponse.orderId,
      transformedResponse
    );
  }

  return transformedResponse;
};
```

Finally, the API Gateway sends the processed response back to the client in a format they can easily understand.

### Step 8: Logging and Monitoring

Throughout this process, the gateway records important metrics to track each request:

```javascript
const logRequest = async (req, res, timing) => {
  await logger.log({
    timestamp: new Date(),
    path: req.path,
    method: req.method,
    responseTime: timing,
    statusCode: res.statusCode,
    userId: req.user?.id
  });
};
```
