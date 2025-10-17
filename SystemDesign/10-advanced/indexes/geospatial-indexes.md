# Geospatial Indexes

Here's an interesting quirk of system design interviews: while geospatial indexes are fairly specialized in practice - you might never touch them unless you're working with location data - they've become a common focus in interviews. Why? The rise of location-based services like Uber, Yelp, and Find My Friends has made proximity search a favorite interview topic.

## The Challenge with Location Data

Say we're building a restaurant discovery app like Yelp. We have millions of restaurants in our database, each with a latitude and longitude. A user opens the app and wants to find "restaurants within 5 miles of me." Seems simple enough, right?

The naive approach would be to use standard B-tree indexes on latitude and longitude:

```sql
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

CREATE INDEX idx_lat ON restaurants(latitude);
CREATE INDEX idx_lng ON restaurants(longitude);
```

But this falls apart quickly when we try to execute a proximity search. Think about how a B-tree index on latitude and longitude actually works. We're essentially trying to solve a 2D spatial problem (finding points within a circle) using two separate 1D indexes.

When we query "restaurants within 5 miles," we'll inevitably hit one of two performance problems:

- If we use the latitude index first, we'll find all restaurants in the right latitude range - but that's a long strip spanning the entire globe at that latitude! Then for each of those restaurants, we need to check if they're also in the right longitude range. Our index on longitude isn't helping because we're not doing a range scan - we're doing point lookups for each restaurant we found in the latitude range.

- If we try to be clever and use both indexes together (via an index intersection), the database still has to merge two large sets of results - all restaurants in the right latitude range and all restaurants in the right longitude range. This creates a rectangular search area much larger than our actual circular search radius, and we still need to filter out results that are too far away.

This is why we need indexes that understand 2D spatial relationships. Rather than treating latitude and longitude as independent dimensions, spatial indexes let us organize points based on their actual proximity in 2D space.

## Core Approaches

There are three main approaches you'll encounter in interviews: geohashes, quadtrees, and R-trees. Each has its own strengths and trade-offs, but all solve our fundamental problem: they preserve spatial relationships in our index structure.

We'll explore each one, but remember - while this seems like a lot of specialized knowledge, interviewers mainly want to see that you understand the basic problem (why regular indexes fall short) and can reason about at least one solution. You don't need deep expertise in all three approaches unless you're interviewing for a role that specifically works with location data.

### Geohash

We'll start with geohash - it's the simplest spatial index to understand and implement, which is why it's often the default choice in many databases. The core idea is beautifully simple: convert a 2D location into a 1D string in a way that preserves proximity.

Imagine dividing the world into four squares and labeling them 0-3. Then divide each of those squares into four smaller squares, and so on. Each division adds more precision to our location description. A geohash is essentially this process, but using a base32 encoding that creates strings like "dr5ru" for locations. The longer the string, the more precise the location:

- "dr" might represent all of San Francisco
- "dr5" narrows it down to the Mission District
- "dr5ru" might pinpoint a specific city block

What makes geohash clever is that locations that are close to each other usually share similar prefix strings. Two restaurants on the same block might have geohashes that start with "dr5ru", while a restaurant in a different neighborhood might start with "dr5rv".

And here's the real elegance: once we've converted our 2D locations into these ordered strings, we can use a regular B-tree index to handle our spatial queries. Remember how B-trees excel at prefix matching and range queries? That's exactly what we need for proximity searches.

When we index the geohash strings with a B-tree:

```sql
CREATE INDEX idx_geohash ON restaurants(geohash);
```

Finding nearby locations becomes as simple as finding strings with matching prefixes. If we're looking for restaurants near geohash "dr5ru", we can do a range scan in our B-tree for entries between "dr5ru" and "dr5ru~" (where ~ is the highest possible character). This lets us leverage all the optimizations that databases already have for B-trees - no special spatial data structure needed.

This is why Redis's geospatial commands use this approach internally. When you run:

```shell
GEOADD restaurants 37.7749 -122.4194 "Restaurant A"
GEORADIUS restaurants -122.4194 37.7749 5 mi
```

Redis is using geohash under the hood to efficiently find nearby points. MongoDB also supports geohash-based indexes, though they abstract away the details.

The main limitation of geohash is that locations near each other in reality might not share similar prefixes if they happen to fall on different sides of a major grid division - like two restaurants on opposite sides of a street that marks a geohash boundary. But for most applications, this edge case isn't significant enough to matter.

This elegance - turning a complex 2D problem into simple string prefix matching that can leverage existing B-tree implementations - is why geohash is such a popular choice. It's easy to understand, implement, and use with existing database systems that already know how to handle strings efficiently.

### Quadtree

While less common in production databases today, quadtrees represent a fundamental tree-based approach to indexing 2D space that has shaped how we think about spatial indexing. Unlike geohash which transforms coordinates into strings, quadtrees directly partition space by recursively subdividing regions into four quadrants.

Here's how it works: Start with one square covering your entire area. When a square contains more than some threshold of points (typically 4-8), split it into four equal quadrants. Continue this recursive subdivision until reaching a maximum depth or achieving the desired point density per node:

For proximity searches, navigate down the tree to find the target quadrant, check neighboring quadrants at the same level, and adjust the search radius by moving up or down tree levels as needed.

The key advantage of quadtrees is their adaptive resolution - dense areas get subdivided more finely while sparse regions maintain larger quadrants. However, unlike geohash which leverages existing B-tree implementations, quadtrees require specialized tree structures. This implementation complexity explains why most modern databases prefer geohash or R-tree variants.

### R-Tree

R-trees have emerged as the default spatial index in modern databases like PostgreSQL/PostGIS and MySQL. While both quadtrees and R-trees organize spatial data hierarchically, R-trees take a fundamentally different approach to how they divide space.

Instead of splitting space into fixed quadrants, R-trees work with flexible, overlapping rectangles. Where a quadtree rigidly divides each region into four equal parts regardless of data distribution, R-trees adapt their rectangles to the actual data. Think of organizing photos on a table - a quadtree approach would divide the table into equal quarters and keep subdividing, while an R-tree would let you create natural, overlapping groupings of nearby photos.

When searching for nearby restaurants in San Francisco, an R-tree might first identify the large rectangle containing the city, then drill down through progressively smaller, overlapping rectangles until reaching individual restaurant locations. These rectangles aren't constrained to fixed sizes or positions - they adapt to wherever your data actually clusters. A quadtree, in contrast, would force you to navigate through a rigid grid of increasingly smaller squares, potentially requiring more steps to reach the same destinations.

This flexibility offers a crucial advantage: R-trees can efficiently handle both points and larger shapes in the same index structure. A single R-tree can index everything from individual restaurant locations to delivery zone polygons and road networks. The rectangles simply adjust their size to bound whatever shapes they contain. Quadtrees struggle with this mixed data - they keep subdividing until they can isolate each shape, leading to deeper trees and more complex traversal.

The trade-off for this flexibility is that overlapping rectangles sometimes force us to search multiple branches of the tree. Modern R-tree implementations use smart algorithms to balance this overlap against tree depth, tuning for how databases actually read data from disk. This balance of flexibility and disk efficiency is why R-trees have become the standard choice for production spatial indexes.

If you're asked about geospatial indexing in an interview, focus on explaining the problem clearly and contrasting a tree-based approach with a hash-based approach.
For example, you could say something like:

"Traditional indexes like B-trees don't work well for spatial data because they treat latitude and longitude as independent dimensions. To efficiently search for nearby locations, we need an index that understands spatial relationships. Geohash is a hash-based approach that converts 2D coordinates into a 1D string, preserving proximity. This allows us to use a regular B-tree index on the geohash strings for efficient proximity searches. However, tree-based approaches like R-trees can offer more flexibility and accuracy by grouping nearby objects into overlapping rectangles, creating a hierarchy of bounding boxes."

By contrasting these two approaches, you demonstrate a deeper understanding of the trade-offs involved in geospatial indexing.