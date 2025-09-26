# Quad Tree

In modern computing, applications like Google Maps, game development, and geospatial databases require efficient ways to store and retrieve spatial data. Traditional data structures like arrays and trees work well for one-dimensional data, but they struggle when handling 2D and 3D spatial queries efficiently.

A QuadTree is a tree-based spatial partitioning data structure that recursively divides a 2D space into four quadrants (hence the name "Quad"). It allows efficient spatial indexing, range queries, and collision detection.

## What is a Quad Tree ?

A Quad Tree is a tree data structure where:

- Each node represents a rectangular region of 2D space.
- The root node represent the entire space.
- If a node contains more than a certain number of points, it subdivides into four equal quadrants (children).
- The subdivision continues recursively until each region contains only a few points or reaches a pre defined depth.

## How does Quad Tree work ?

### Structure of a Quad Tree node

Each node in a Quad tree contains

- A bounding box (x_min, y_min, x_max, y_max).
- A list of points within the node.
- Four child nodes: top-left, top-right, bottom-left, bottom-right

If the number of points in a node exceeds a predefined threshold (e.g., 4 points per node), the node splits into four smaller quadrants, distributing the points among them.

### Operations in a Quad Tree

1. Insertion

- If the node has space, insert the point.
- If the node is full, split it into four quadrants and redistribute the points.

2. Search (Range Query)

- Check if the query region overlaps with the node’s bounding box.
- If yes, check points inside the node.
- Recursively search relevant quadrants.

3. Deletion

- Locate the point and remove it.
- If a node becomes empty, merge its quadrants back.

## Real world applications

### Geographic Information Systems (GIS)

- Used in Google Maps, OpenStreetMap to store location-based data efficiently.
- Helps in zooming operations by retrieving relevant map sections.

### Image Processing (Compression & Storage)

- Used in image compression by dividing images into quadrants based on color similarity.
- Helps in efficient storage of large images.

## Benefits

Quad trees offer several key benefits, especially for spatial data and 2D applications:

1. Efficient Spatial Queries
Quad trees allow fast searching for points or objects within a region, making range queries and nearest neighbor searches much quicker than scanning all data.

2. Optimized Storage
They store sparse data efficiently by subdividing only where needed, reducing memory usage for large, mostly empty spaces.

3. Fast Insertions and Deletions
Inserting and removing points is efficient, as operations are localized to relevant quadrants.

4. Improved Performance for Graphics and Games
Quad trees speed up collision detection, rendering, and visibility checks by limiting calculations to relevant areas.

5. Scalable for Large Datasets
As data grows, quad trees adapt by subdividing space, maintaining performance even with millions of points.

6. Useful for Map and Location Services
Services like Google Maps, Uber, and GIS platforms use quad trees to index and retrieve spatial data quickly.

## Time Complexity of Quad Tree Operations

1. Insertion:

When you add a point, the quad tree checks which quadrant it belongs to and may subdivide nodes if needed.

- For evenly distributed data, this usually takes O(log n) time, where n is the number of points.

- In the worst case (if all points fall into the same quadrant repeatedly), it can take O(n) time.

2. Range Query (Search):

To find all points in a region, the quad tree only searches relevant quadrants, skipping large empty areas.

- Average case: O(log n + k), where k is the number of points found.
- Worst case: O(n), if the query region overlaps many nodes or the tree is unbalanced.

3. Deletion:

Removing a point is similar to insertion—locate the point, remove it, and possibly merge nodes.

- Average case: O(log n)
- Worst case: O(n)
