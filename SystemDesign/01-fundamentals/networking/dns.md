# DNS

When you enter a domain name in your browser, a series of steps occur to translate that name into an IP address.

- User Request: You type the URL into your browser.
- DNS Resolver (Recursive Resolver): Your computer sends the request to a DNS resolver provided by your Internet Service Provider (ISP) or a public DNS service (like Google DNS or Cloudflare).

- Root Name Server Query: The resolver first queries a root name server, which doesn’t know the exact IP but can direct the resolver to the appropriate Top-Level Domain (TLD) server.

- TLD Name Server Query: The resolver then contacts the TLD server (for .com in our example) to get further guidance.

- Authoritative Name Server Query: Finally, the resolver queries the authoritative name server for  to obtain the precise IP address.

- Response to User: The IP address is returned to your browser, and you’re directed to the website.