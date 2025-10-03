# Navigation System

Design a navigation system like Google Maps that allows users to:

- Search for locations and points of interest (POIs)
- Get turn-by-turn navigation with optimal route calculation
- View real-time traffic conditions and route adjustments
- Estimate travel time for different transportation modes (driving, walking, public transit)
- Get alternative route suggestions
- Share location and ETA with others
- Save favorite locations and recent searches
- Work in offline mode for downloaded map areas

The system should handle millions of users requesting routes simultaneously, provide real-time traffic updates, support global map data, and deliver sub-second route calculations with accurate ETAs.

## Solution

Before going ahead and discussing the design lets take a moment first to understand the requirements for the app we are going to design. Thats is lets first note down "What" we need to design rather than the "How" and "Whys".

### Functional Requirements

- Users should be able to search for locations and points of interest (POIs)
- Users should be able to put in destination location, and get route details along with ETA.
- Users should be able to get turn-by-turn navigation with optimal route calculation with real-time traffic conditions and route adjustments
- Users should be able to get an estimate travel time for different transportation modes.

Out of scope requirements

- Get alternative route suggestions
- Share location and ETA with others
- Save favorite locations and recent searches
- Work in offline mode for downloaded map areas

We can always work with the interviewer to bring these to scope.

### Non functional requirements

- Scale: Millions of users requesting routes simultaneously
- Latency: Sub-second route calculations with accurate ETAs.
- Real time updates to routes as user navigates.
- Availability: System should be highly available in case of failures.

### Core Entities

Once we have the requirements listed down, we will go ahead and list down the core entities of the system.

#### Location

- latitude
- longitude

#### Place

- id
- address
- location: Location

#### Route

- id
- eta
- source: Location
- destination: Location
- roads: Road[]
- distance: number
- travelMode: can be an enum which stores travel modes like walk, car, bike etc

#### Navigation

- id
- currentLocation: Location
- destination: Location
- route: Route
- startTime
- estimatedEndTime

#### Road

- id
- points: Location[]
- length

#### Map

- id
- roads: Road[]
- places: Place[]

### Data characteristics

- Map data is mostly read-heavy with occasional updates for new roads, places, and traffic conditions.
- Route calculations are read-heavy, especially during peak hours. We can use a noSQL database for storing map data and a graph database for route calculations.
- Road and place data is relatively static, we can use a NoSQL database like MongoDB or Cassandra for storing this data.
- Location data is dynamic and needs to be updated frequently. We can use a write-optimized database like PostgreSQL with PostGIS extension for storing location data.
- Route data is dynamic and needs to be updated frequently. We can use a graph database like Neo4j or Amazon Neptune for storing route data.

### API Design

#### Search API

- GET /search?{query}
  returns Places []

#### Route Calculation API

- Post /route
  {
    source: Location,
    destination: Location
  }

  Returns Route details

#### Navigation API

- ws /navigation
  {
    currentLocation: Location,
    destination: Location,
    route: Route
  }

  Returns Navigation details

This will be a request over websockets as we want real time updates to routes as user location changes.

I feel these APIs suffice for now. We can always come back and add more or update them as we go deep in the design.

### High level architecture

We will start very basic and have the requirements working and then work on deep dives.

1. Users should be able to search for locations and points of interest (POIs)

- Users input destination place and send GET request to /search API
- The request is received by the API gateway which does some sanity checks and routes the request to search service.
- The search service calls the places service to get the details of the the places which match the query params passed.
- The places service gets data from places and location data, compute the results and sends it back to search service.
- The results are then routed back to the API gateway which then sends it back to the client.

2. Users should be able to put in destination location, and get route details along with ETA.

- Users input the destination location and send a POST request to /route API, passing the source and destination location in the request body.
- The request is received by the API gateway which does some sanity checks and routes the request to route service.
- The route service calls the places service to get details about the destination place.
- The route service fetches traffic data and computes the best route along with eta and sends it back to API gateway which forwards it to the client.
- The route service uses uses route optimization to compute the best and shortest route. We will not go into the details of the algorithm.

3. Users should be able to get turn-by-turn navigation with optimal route calculation with real-time traffic conditions and route adjustments

- Users select the route suggested by the system and then select start button
- This establishes a websocket connection with the server. The user sends real time location via the connection. They also send the destination details and route selected.
- The navigation service fetches real time data, and uses route optimization algorithms to compute the navigation details and send it back to the users in real time.

Here's the high level diagram of the architecture. Note that this is a very basic architecture and we will be handling deep dives in the next section.

![Architecture](../scenario-questions/imgs/navigation-system.png)

### Addressing Scalability and Reliability

- Global map data distribution and updates: We can use a CDN to distribute map data globally. We can also use a pub-sub system to push updates to map data to all the regions.

- Real-time traffic updates: We can use a pub-sub system to push real-time traffic updates to all the regions. We can also use a stream processing system like Apache Kafka or AWS Kinesis to process real-time traffic data.

- Efficient route calculation at scale: We can use a graph database like Neo4j or Amazon Neptune to store route data. We can also use a caching layer like Redis or Memcached to cache frequently accessed routes. We will be using route optimization algorithms to compute the best and shortest route. We use a stream processing system to process real-time traffic data and update the routes accordingly.

- Sub-second response times: We can use a caching layer like Redis or Memcached to cache frequently accessed routes. We can also use a load balancer to distribute the load across multiple instances of the route service.

- Map tile caching and CDN usage: We can use a CDN to distribute map tiles globally. We can also use a caching layer like Redis or Memcached to cache frequently accessed map tiles.

---