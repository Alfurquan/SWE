# GeoHashing

Imagine you’re building a system like Uber, Google Maps, or a nearby restaurant finder.

You need to store and query millions or even billions of location points to find what's "close" to a specific point? And you want to do it fast.

But querying latitude and longitude ranges can get messy and slow, especially at scale.

That’s where GeoHashing comes in.

## Problem: Finding Nearby Entities Efficiently

Imagine you have a database table of restaurants, with columns for latitude and longitude. A user at (lat: 34.0523, lon: -118.2438) wants to find all restaurants within a 1km radius.

How would you write this query?

A naive approach might be a "bounding box" query:

```sql
SELECT * FROM restaurants
WHERE latitude BETWEEN 34.0433 AND 34.0613
AND longitude BETWEEN -118.2528 AND -118.2348;
```

This works, but it has major performance problems at scale:

Most databases use B-tree indexes, which are fantastic for one-dimensional data. But they struggle with 2D queries. The database can use an index on latitude, but then it has to do a full scan of all matching rows to filter by longitude (or vice-versa).

A composite index on (latitude, longitude) helps, but it still doesn't truly understand spatial locality.

We need a way to represent 2D proximity in a 1D format that a standard database index can efficiently search. That’s what GeoHashing is about.

## What is GeoHashing?

GeoHashing is a method of encoding geographic coordinates (latitude, longitude) into a short alphanumeric string.

Example: The coordinates for downtown San Francisco (37.7749, -122.4194) can be encoded as the geohash: 9q8yyf.

This hash looks like just a random string of characters but it has two magical properties:

### Spatial Locality

The more characters two GeoHashes share at the beginning (i.e., the longer their common prefix), the closer those two locations are geographically.

This means: Nearby points will usually have similar GeoHash prefixes. Far-apart points will have completely different prefixes.

GeoHashes are hierarchical: each additional character in the hash zooms in to a more precise region.

Example:

- 9q8yyf and 9q9pvu share the first three characters → they belong to neighboring regions but are not immediately adjacent.

- 9q8yyf and 9q5ctr share only the first two characters → they are farther apart, likely hundreds of kilometers.

- a2sed7 → starts with a completely different prefix. It represents a geographically distant region, possibly on another continent.

### One-Dimensional and Indexable

GeoHashes convert 2D coordinates (latitude, longitude) into a 1D string. This string can be stored in a VARCHAR or TEXT field in a relational or NoSQL database, and indexed efficiently using a B-tree or Trie.

This allows for:

- Fast lookups of nearby places
- Easy sharding based on location
- Efficient sorting and filtering using standard indexes

## How GeoHashing Works ?

GeoHashing may look like magic at first glance, but it’s built on a simple and elegant idea: convert a 2D geographic point into a 1D string through binary encoding and interleaving.

## Why Use GeoHashing?

GeoHashing offers benefits that are highly valuable in location-based services:

### Efficient Proximity Search

Instead of range queries on lat/lon, you can:

- Use GeoHash prefix matching
- Search within a bounding box by comparing string prefixes

### Indexing in Databases

Databases like PostgreSQL, Cassandra, and MongoDB can:

- Index strings faster than floating-point pairs
- Use trie or B-tree-based lookups for prefix search

### Spatial Sharding

GeoHashes are great for sharding data in distributed systems:

- Assign prefixes to different servers/partitions
- Keep nearby data close together

## Real-World Applications

GeoHashing is widely used in location-based apps and geospatial databases.

Here are some real-world examples where GeoHashing shines:

### Ridesharing Platforms (e.g., Uber, Lyft)

GeoHashes can be used to group drivers and riders into spatial buckets based on their current location.

- When a rider requests a trip, the system calculates their GeoHash (e.g., to 6 or 7 characters).

- It then quickly finds drivers in the same or neighboring GeoHash cells, drastically reducing the search space.

- This enables real-time proximity matching without scanning all active drivers.

### Food Delivery Services (e.g., Swiggy, Zomato)

When a user opens the app to browse nearby restaurants:

- Their coordinates are converted into a GeoHash.

- The backend queries all restaurants whose stored GeoHashes match that prefix or its neighbors.

- This allows the system to serve relevant results instantly, even with millions of entries in the database.

### Geospatial Databases (e.g., Elasticsearch, MongoDB)

GeoHashing is often used under the hood in spatial indexing strategies.

- Elasticsearch supports geohash_grid aggregations to efficiently bucket documents by location.

MongoDB can store GeoHashes for fast, prefix-based querying on 2D location fields.