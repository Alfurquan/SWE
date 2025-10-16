# E-commerce Platform (Hard)

You're building Amazon. Core features:

- Product catalog with millions of items (read-heavy)
- Real-time inventory updates across sellers
- Order processing with payment workflows
- Product image/video uploads
- Daily sales analytics reports

Question: Design the system handling catalog browsing, inventory management, and order processing.

## Solution

In this problem, we will be designing an ecommerce platform like `Amazon` combining all the patterns we studied. We will design the features listing the patterns and how they work.

Before going ahead with the features, lets briefly touch on the core entities of the system.

### Core Entities

#### User

- id
- name
- email
- password (Stored in hash)

#### Product

- id
- title
- description
- price
- quantity

#### ProductMedia

- productId
- mediaURL
- uploadStatus
- uploadTime

#### Order

- id
- userId
- orderItemId
- totalPrice
- placedAt

#### OrderItem

- id
- productId
- quantity
- price

Note that we have just outlined the rough attributes that these entities can have, they can have even more attributes, but we will keep things simple for now.

Next up, we will go through the features, list down what pattern applies and how they will work

### Upload photos/videos (1MB - 2GB)

#### Pattern: Handling large blobs

For uploading photos and videos, we will be using the handling blobs pattern.

#### How will this work ?

- Client sends a POST request to upload a photo or video for the post. 
- The API server accepts the request, generates a presigned url for the media upload, it also inserts a row in the ProductMedia table with productId and upload status as pending.
- The API server returns the presigned URL back to the client. We can inforce size limits and media type in the pre signed URL so as to prevent a client from uploading lets say a PDF or and exe file instead of image or video.
- The Client uses the presigned URL to upload the file to and object store directly. We can use S3 here for the object store.
- For large files, the upload can happen in chunks so that in case upload fails, it can be safely retried from the failed chunk. The client can use the chunks, and track progress to show a good progress bar UI to the users.
- Once upload is completed, the object storage sends a notification to the API server and it updates the upload status in ProductMedia table to success.
- For download, we will be serving the photos and videos from CDN and edge servers closer to the users to reduce latency.

### Product catalog with millions of items

#### Pattern: Scaling Reads

For showing product catalog with millions of items, we will use the scaling reads pattern. Below is how it will work

To handle read load, we can use caching like redis to cache popular items and frequently viewed items. We will use CDNs to serve media content to users from geographically nearest servers to reduce latency.

To handle searches for products, we will use a powerful search engine like elastic search. We will be storing product titles, descriptions etc to enable faster searches for products. Any changes made to product details are synced to elastic search using CDC (Change data capture).

- Client Sends a GET call to view the products by a search.
- The API server will receive the call, forwards the call to our search service which uses elastic search to fetch all products matching the search term.
- The matching products are returned back to the API server, which uses a paginated API to return back the response to the client. The paginated API helps in not sending all the data back to the client at once so that the client does not get overwhelmed with the response.
- The API server also caches the most frequently viewed products in an in memory cache like redis for faster retrieval later.
- The Media for the products are served from CDN to reduce latency.

### Inventory Management

#### Pattern: Dealing with contention

For inventory management, we will be using the dealing with contention pattern. We will specifically be covering the scenario where lets say one item is left and multiple people try buying the same item.

We can use optimistic concurrency for inventory updates with the current stock count as our version, but we should also implement application-level coordination for shopping cart "holds" to improve user experience and reduce contention at checkout. We can use a distributed lock like redis to lock shopping cart holds.

This is how it will work

- When lets say, only one quantity of a product item is left and multiple people are trying to buy it. 
- The person adds the item to the cart, it tries to acquire a lock in redis for the product item. The lock is set a TTL to expire after sometime lets say 10 minutes. When someone else tries to add the same product item to cart, they will be unable to acquire the lock on the same product instance. This will help reduce contention even before they occur.
- The user goes ahead and completes the payment and purchases the item. We will employ transactions to make sure the order creation and inventory update happens atomically, i.e. both of them pass or both of them fail.
- On the database end, we will be using optimistic concurrency control for inventory updates with quantity as our version.
- If lets say the user does not complete the payment, or abandons the purchase, the redis lock expires and someone else can go ahead and purchase it.
- This works fine if database is on a single node, for multiple nodes, we can use SAGA pattern for distributed transactions.

### Order processing with payment workflows

#### Pattern: Multi Step process

For order processing with payment workflows we will be using multi step process pattern.

We can use message queues like kafka for storing messages between different components. Here's how this will work

- Client sends a POST call to /order to create an order. The API call carries the product and payment details.
- The API server receives the API call, places and order create event on the message queue.
- A background worker picks the message, processes it and creates an order entry in the database with status as payment_pending. The worker also updates the product inventory.
- The background worker places another event on the message queue to process the payment.
- Another background worker picks up the event, goes ahead and calls the third party gateway to proceed with the payment.
- The worker can use polling to keep polling the third party gateway for payment status.
- Once payment succeeds, the worker goes ahead and updates the status for the order and places another event on the message queue to send notification to the user.
- Another worker picks up this event from the message queue and goes ahead and sends notification to the users via email/sms
- Using this mechanism we have employed an event driven architecture to process payment and orders. If at any step, failure happens, we will be rolling back previous steps.
- We can also employ idempotency keys in the orders API to prevent double orders.

### Daily Sales Analytics Reports

#### Pattern: Managing long running tasks

For Daily sales analytics reports we can use long running tasks pattern.

We can use message queues like kafka for storing events for background processing.

Here's how this will work

- Whenever a transaction happens, we will place an event in the message queue to be processed asynchronously and return back to the user.
- A background worker will pick up the event and generate the analytics reports.
- If the worker crashes, another one can pick up the event.

---