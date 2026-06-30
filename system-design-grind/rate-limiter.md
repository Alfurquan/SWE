# Rate limiter

## The Interview Prompt
"We have a massive public-facing API. I want you to design a distributed rate limiter that prevents any single user from overwhelming our backend servers."

## Phase 1: Requirements and scope

### Clarifying questions asked

- Is the rate limit per user id or per ip address
- Do we just need rate limiting for one API or multiple APIs
- What is the expected traffic per second hitting the API
- Do we need accurate rate limiting or short bursts are allowed
- In case of failures in rate limiter, do we want to stop user requests till the system becomes healthy or do we prefer availability and allow users to still reach the servers as we fix the rate limiter 

### Functional requirements

- System should be able to apply rate limit to user requests based on user id on auth end points and fallback to ip address for non auth endpoints

- Different rate limit rules for different API endpoints. For example, /login might be limited to 5 requests per minute, while /read_feed might allow 100 requests per second.

### Non Functional requirements

- Latency: System should support low latency of around 1-2 ms for rate limiting check. We do not want to hang user requests too long for applying rate limiting rules

- Availability: System should be highly available. If the rate limiter infrastructure goes down, we drop the limits and let traffic flow to the backend servers while we page the on-call engineer.

- Scale: The global system handles about 1 Million requests per second (QPS) across all users and endpoints.

- Strictness: Short bursts are allowed. If a user's limit is 10 requests per minute, they should be able to fire all 10 in the first second without being blocked, as long as they don't exceed the total limit within that minute.

## Phase 2: Architecture & Algorithm

### Placement of the rate limiter

Now once the requirements are locked in, we can tackle the architecture of the system. 

Now there are two places we can have the rate limiter in 

- Inside app server code
- Inside the API gateway

I would prefer placing the rate limiter as part the API gateway. This would separate the concerns of app bussiness logic code from the infrastructure code like rate limiter. 

Further app servers can scale differently than rate limiters so placing them seprately makes sense.

So this is how the high level flow would look like

Clinet -> API Gateway -> App Server
                |
          Rate Limiter

- The rate limiter here acts as traffic manager
    - It extracts the user id from the request headers which has JWT token for auth endpoints, in case of unauth endpoints, it extracts the ip address from the request headers
    - Looks up for the rate limiting rules for the endpoint 
    - Checks if the request should be allowed to pass or not.


### Core Algorithm

Now for the core algorithm for the rate limiter, we have quite a few choices. Namely I will describe two and then pick one based on our requirements

#### Token bucket

For this algorithm, the user is assigned a fixed no of tokens based on the rules, the tokens get refilled at some rate. For each user request, we check if the user has any tokens left, if yes, one token gets used and the user request is allowed, if not the user request is not allowed.

Pros

- Simpler to implement
- Consumes less memory

Cons

- Allows short bursts and then proceeds at a steady rate.  If a user's limit is 10 requests per minute, they can fire all 10 in first second without being blocked. Though this is a con of token bucket, but for our requirements, it fits best.

#### Sliding window log

In this algorithm, each user has a maximum no of requests in a time window. For each request, we check if the user no of requests is less than the max no of requests in the time window. If yes, we add the request and allow the request. If not, we do not allow the request. For each request, we also remove older requests from earlier time windows.

Pros

- More accurate than token bucket
- No chances of any requests bursts at the boundary of request window

Cons

- Consumes more memory as reach request is stored
- Complex to implement.

For our use case since we can allow bursts, we would go with token bucket as the core algorithm as i allowes bursts and is memory efficient.

## Phase 3: Deep Dives & State Management
You have successfully defined the core algorithm (Token Bucket) and the placement (API Gateway).

At 1 Million QPS, we will have a fleet of distributed API Gateway nodes.

My question for this phase: If User A sends 5 requests to Gateway 1, and then sends 5 requests to Gateway 2, how does your system ensure that Gateway 2 knows about the first 5 requests? Walk me through how you want to design and manage the state (the token buckets) across a distributed fleet of gateways. The floor is yours.

### Approach

- We would use a redis cluster to store the user requests and counts.
- This way all the gateway servers would communicate with the redis cluster which holds and manages the state (the token buckets)
- Each gateway server would check the redis cluster for the user request count and decide whether to allow or block the request based on the token bucket algorithm.
- The redis cluster would be designed to handle the high read and write throughput required for 1 Million QPS, with appropriate sharding and replication for scalability and availability.
- To prevent concurrency issues, we would use atomic operations provided by redis to update the token buckets, ensuring that multiple gateway servers can safely update the same user's token bucket without conflicts. That is we can wrap the token bucket logic in a lua script and execute it atomically in redis.

---

Interviewer: "Using a Redis cluster with Lua scripts solves our concurrency and centralized state issues beautifully. However, let's do some back-of-the-napkin math on the memory footprint. If we have 100 million Daily Active Users (DAU), and we track limits across 5 distinct API endpoints per user, that's up to 500 million unique keys in our Redis cluster. Redis stores everything in RAM, which gets incredibly expensive. How would you structure the Redis keys and values to ensure this cluster's memory usage remains as lean as possible?"

How do you want to design the data types and keys inside Redis to minimize memory consumption?

### Approach

To minimize memory consumption in Redis, we can use the following strategies for structuring our keys and values:

- **Use Hashes for User Data**: Instead of creating separate keys for each user and endpoint, we can use Redis hashes to store the token bucket information for each user. For example, we can have a key like `user:{user_id}` which is a hash that contains fields for each endpoint, such as `login`, `read_feed`, etc. Each field would store the current token count and the last refill timestamp.

- **Use Bitmaps for Token Buckets**: For endpoints with simple on/off limits (e.g., 10 requests per minute), we can use Redis bitmaps to represent the token bucket. Each bit can represent a request, and we can use bit operations to check and update the token count efficiently.

- **Expire Keys**: We can set an expiration time on the keys to automatically clean up data for inactive users. For example, if a user has not made any requests in the last hour, we can set the key to expire after 1 hour of inactivity.

For our use case, I would go with hashes for use data and add expire keys to make sure we do not keep data for inactive users. This way we can efficiently manage the state of token buckets while keeping memory usage in check.

---

## Phase 4: Resilience & Cascading Failures

Interviewer: "Let's say our entire Redis cluster experiences a catastrophic network partition and goes offline. Our API Gateways do exactly as designed: they fail-open and stop checking rate limits. Suddenly, the full force of 1 Million QPS hits our backend application servers directly.

If our backend servers and databases cannot safely process 1 Million QPS without melting down, how do we design our API Gateways to honor the 'fail-open' availability requirement without instantly causing a cascading failure that crashes the entire backend infrastructure?"

### Approach

Firstly for fail open scenario we need to be precise, we can have fail open on some endpoints like /feed but /login must be fail closed, we do not want the login endpoint to be flooded with 1 million QPS in case of redis failure.

For the fail open endpoints, we can implement a circuit breaker pattern in the API Gateway. The circuit breaker would monitor the health of the Redis cluster and if it detects that Redis is down, it would switch to a fail-open mode for the affected endpoints.

In fail-open mode, the API Gateway would allow all requests to pass through without checking the rate limits. However, to prevent overwhelming the backend servers, we can implement a secondary rate limiting mechanism at the API Gateway level that is less precise but can still provide some level of protection. For example, we can have a global rate limit for all requests that is set to a safe threshold (e.g., 100,000 QPS) that the backend servers can handle.

This way, even if Redis is down, we can still protect our backend servers from being overwhelmed by a sudden surge of traffic.