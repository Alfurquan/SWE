# Scenario A: Social Media Platform (Medium-Hard)

You're building Instagram. Users can:

- Upload photos/videos (1MB-2GB files)
- Follow other users and see real-time feed updates
- Like/comment on posts (high write volume)
- Search and browse content (read-heavy)
- Get push notifications for interactions

Question: Design the complete system covering uploads, feed generation, real-time updates, and scaling.

## Solution

This problem involves designing a social media platform like Instagram combining all the patterns which we have studied. I will design all the features listed by mentioning which pattern fits here and how it will work.

Before diving into the features one by one, lets first lay down the core entities of the system

### Core Entities

#### User

- id
- name
- email
- password (Stored as hash)

#### Followers

- followeeId
- followerId

#### Post

- id
- title
- content
- authorId
- createdAt

#### PostMedia

- postId
- mediaURL
- uploadStatus
- timestamp

#### Comments

- id
- postId
- text
- authorId
- commentedAt

#### Likes

- id
- postId
- authorId

Note that we have just outlined the rough attributes that these entities can have, they can have even more attributes, but we will keep things simple for now.

Next up, we will go through the features, list down what pattern applies and how they will work

### Upload photos/videos (1MB - 2GB)

#### Pattern: Handling large blobs

For uploading photos and videos, we will be using the handling blobs pattern.

#### How will this work ?

- Client sends a POST request to upload a photo or video for the post. 
- The API server accepts the request, generates a presigned url for the media upload, it also inserts a row in the PostMedia table with postId and upload status as pending.
- The API server returns the presigned URL back to the client. We can inforce size limits and media type in the pre signed URL so as to prevent a client from uploading lets say a PDF or and exe file instead of image or video.
- The Client uses the presigned URL to upload the file to and object store directly. We can use S3 here for the object store.
- For large files, the upload can happen in chunks so that in case upload fails, it can be safely retried from the failed chunk. The client can use the chunks, and track progress to show a good progress bar UI to the users.
- Once upload is completed, the object storage sends a notification to the API server and it updates the upload status in post media table to success.
- For download, we will be serving the photos and videos from CDN and edge servers closer to the users to reduce latency.

### Feed generation

#### Pattern: Scaling read pattern

Now feed generation will be coming under the scaling reads pattern as feed data will be huge for users following lots of other users.

#### How will it work ?

Simple solution

Now to generate the feed, lets start with a very simple solution. To generate the feed for a user, first we will look up the followings for the user, fetch the post for each of them, merge and show the results in reverse timestamp order (Recent first)

This is a very simple solution which will not well scale well for users following 1M users. We can perform some optimizations to it.

- We can add indexes on the authorId column of the post table to speed up the query we run to fetch the posts for a user. This will improve the performance but not to a large extent.
- Instead of fetching the results everytime users want to see their feed, we can somehow precompute the results and show them directly. Well there is a way to do that and we will discuss that next.
- We will use fanout on write, that is whenever a use creates a post we can asynchronously add the post to a new table - `Feed` which will be having the precomputed posts for each user. Now whenever, a user request feed, we can look up the precomputed `Feed` table for them and show the posts to them. This works great but has a problem. For users like Justin Bieber who have millions of followers, writing their post to millions of rows is not feasible. 
- To solve above issue, we can use a hybrid approach, where we can add a boolean column to followers table - `isPrecomputed`. We set this to false for users having millions of followers. 
- Now when lets say, a user like Justin Bieber posts, we do not write their posts to millions of rows in precomputed feed table. Instead when any of their followers request their feed, we fetch some results from the precomputed feed table and posts from followee having `isPrecomputed` as False, merge them and return the results back.
- This hybrid approach works best for feed generation.

### Like and comment

#### Pattern: Scaling writes pattern

For the like and comment features, we will be using the scaling writes pattern.

#### How will it work ?

We have already segregated the like and comments table from the post table so that we can scale writes to these tables independently.

This is how it will work

- When a user likes or comments on a post, we make an API call to the API server to record the new like or comment.
- We use optimistic UI updates where we immediately show the like/comment to the user who posted it.
- When the API server receives the request, it places the request in a message queue like Kafka and returns immediately back to the client.
- We chose Kafka here as it provides great durability, low latency and ensures our events are not lost.
- We have background workers, which pick up the events from the message queue and update the like and comments in the database.
- In case any worker crashes before updating the database, any other worker can pickup the event and update the database.
- To improve performance, we can also perform batch writes, where we can batch the events for a post and process them in batches from kafka.
- The whole process guarantees eventual consistency, where some of the users around the world may not see a like or comment updated recently but they will eventually see it. This is a big tradeoff we make and it is acceptable for a social media app having millions of users.

### Search and browse content

#### Pattern: Scaling Reads pattern

For the search and browse content, we will be using the scaling reads pattern.

#### How will it work ?

- For the search functionality, we will be using a high throughput search engine like Elastic Search. Users will mostly be searching users by name, posts with title. We can place user names, post titles etc in elastic search and it will give search results faster. To keep elastic search in sync with main database we can use CDC (Change data capture) where on any DB update, we can trigger an update in the elastic search as well.
- We can also use a cache like redis to search most frequent content in redis to serve it faster to the users.
- We can also employ CDNs to serve data to users from geographically nearest edge servers. This can help reduce latency and improve read performance.

### Push Notifications

#### Pattern: Real time updates

For the search and browse content, we will be using the Real time updates pattern

#### How will it work ?

- For Push notifications, we can use a pub-sub model where users can subscribe to notifications for likes, comments on their posts.
- When a user likes or comments on a post, we publish an event to a message queue like Kafka. The event contains details like userId, postId, type of interaction (like/comment)
- We have background workers which consume these events and send push notifications to the users using services like Firebase Cloud Messaging or Apple Push Notification Service.
- We can also use web sockets to send real time notifications to users who are online on the platform.
- To handle high volume of notifications, we can use a priority queue where high priority notifications like comments are processed first and low priority notifications like likes are processed later.

---
