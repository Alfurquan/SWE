# Proxy vs Reverse Proxy

Proxies and reverse proxies are servers that sit between clients and servers to improve security, privacy and performance.
A Proxy server (sometimes called a Forward proxy) acts on behalf of clients, while a Reverse Proxy acts on behalf of servers.

## What is a Proxy Server?

`A proxy is an entity that has the authority to act on behalf of another.`
In computer terms, a proxy (or a forward proxy) is a server that acts on behalf of clients on a network.

Let’s walk through a simplified example of how a proxy server handles a request:

- The user types a website URL into their browser. The request is intercepted by the proxy server instead of going directly to the website.
- The proxy server examines the request to decide if it should forward it, deny it, or serve a cached copy.
- If the proxy decides to forward the request, it contacts the target website. The website sees only the proxy server’s IP, not the user’s.
- When the target website responds, the proxy receives the response and relays it to the user.

## Benefits

- Privacy and Anonymity: Proxy servers hide your IP address by using their own, so the destination server cannot know your real location or identity.
- Access Control: Organizations use proxies to enforce content restrictions, monitor internet usage.
- Security: Proxies can filter out malicious content and block suspicious sites, providing an additional layer of security.
- Improved Performance: Proxies cache frequently accessed content, reducing latency and improving load times for websites.

## Real world applications

- Bypassing Geographic Restrictions: Streaming services, for instance, often offer different content based on a user’s location. With a proxy server based in the target region, you can access that region’s content library as if you were a local user.
Suppose you’re in India and want to access the US library of a streaming platform (eg.. Netflix). By connecting to a proxy server located in the US, your request to the streaming platform will appear to be coming from the US, allowing access to its content as if you were a US-based viewer.

- Speed and Performance Optimization (Caching): Proxies can store cached versions of frequently accessed content, enabling faster load times and reducing bandwidth usage.

## What is reverse proxy ?

A reverse proxy is the reverse of a forward proxy. It regulates traffic coming into a network.
It sits in front of servers, intercepts client requests and forwards them to backend servers based on predefined rules.
Think of a reverse proxy as a gatekeeper. Instead of hiding clients from the server, it hides servers from clients.

Let’s walk through a simplified example of how a proxy server handles a request:

- A user types a website URL into their browser, which sends a request to the server.
- The reverse proxy server receives the request before it reaches the backend servers.
- Based on predefined rules (like load balancing or server availability), the reverse proxy forwards the request to the appropriate backend server.
- The backend server processes the request and sends a response back to the reverse proxy.
- The reverse proxy relays the response to the client, with the client never directly interacting with the backend servers.

## Key benefits

- Enhanced Security: By acting as a protective layer, a reverse proxy hides backend servers from clients, reducing the risk of attacks directly targeting backend infrastructure.
- Load Balancing: A reverse proxy can distribute incoming requests evenly across multiple backend servers, improving system reliability and preventing server overload.
- Caching Static Content: Reverse proxies can cache static assets like images, CSS, and JavaScript, reducing the need to fetch these files from the backend repeatedly.