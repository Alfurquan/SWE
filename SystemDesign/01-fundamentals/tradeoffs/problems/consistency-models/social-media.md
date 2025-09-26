# Social Media Platform

## Question

You're designing a social media platform with global reach. Consider these features:

- Post creation and news feed generation
- Friend/follower relationships
- Like/comment counters
- Private messaging
- Account settings and privacy controls

For each feature, determine whether strong or eventual consistency is more appropriate. Then, design a hybrid system that optimizes for both correctness and user experience. Address specific challenges like:

- How would you handle message delivery status?
- How would you ensure privacy settings are applied correctly?
- How would you handle count discrepancies for likes/comments?

Please provide a detailed answer considering tradeoffs, implementation approaches, and specific techniques you would use to balance consistency requirements with performance and user experience.

## Answer

We are designing a social media platform with global reach. Here are strategies for below features along with the consistency model we can follow for them.

### Post creation and news feed generation

For post creation and news feed generation we will favour eventual consistency over strong consistency.

Analysis and reasoning:

- In CAP theorem, we want availability over consistency when failure happens. Its fine if users see stale data for sometime than no data or longer wait times.
- Data criticality is low, as it is acceptable for users to see stale data for sometime.
- We want low latency for quick reads, so we will be favoring eventual consistency as strong consistency can lead to high latency if we wait for the changes to propagate to all replicas.
- For post creation we will use read your writes consistency where the user will see his post instantly while it takes time for changes to propagate to others.
- For feed generation, we can use caching at different layers (CDN, edge serves, in memory via redis) to serve data faster and reduce load on main databases.
- We will use fan out on write approach where when a user creates a post, we will push the post to all his followers' feeds. This will ensure that followers see the post in their feed quickly.
- We can use techniques like sharding and partitioning to scale the databases to handle large number of reads and writes.

### Friend/Follower relationships

For friend/follower relationships we will again favour eventual consistency rather than strong consistency.

Analysis and reasoning:

- In CAP theorem, we want availability over consistency when failure happens. Its fine if users see stale data for sometime than no data or longer wait times.
- Data criticality is low, as it is acceptable for users to see stale data for sometime.
- We want low latency for quick reads, so we will be favoring eventual consistency as strong consistency can lead to high latency if we wait for the changes to propagate to all replicas.

### Like/comment counters

We will favour eventual consistency rather than strong consistency

Analysis and reasoning:

- In CAP theorem, we want availability over consistency when failure happens. Its fine if users see stale data for sometime than no data or longer wait times.
- Data criticality is low, as it is acceptable for users to see stale data for sometime.
- We want low latency for quick reads, so we will be favoring eventual consistency as strong consistency can lead to high latency if we wait for the changes to propagate to all replicas.
- For like and comments, we will use read your writes consistency where the user see their like and comment instantly while it takes time for changes to propagate to others.
- Also we will be using casual consistency for comments to make sure that comments appear in order when anyone sees them.
- For conflict resolution when users simultaneously like or comment on the post, we can use strategies like CRDTs to merge these changes in order.
- For low latency we can use caching at different layers - CDNs, edge servers, redis etc.

### Account settings and privacy controls

For this we will be using hybrid of strong and eventual consistency. When the user changes any settings or privacy control, we want the changes to be persisted by favoring consistency over availability in CAP theorem.

For the changes to propagate to other friends, we can use eventual consistency.
Analysis and reasoning:

- For user experience we can use read your writes consistency where the user will see their changes instantly while it takes time for changes to propagate to other friends.
- Also if people try to access the private account, we will check the privacy settings from redis first and if not found we will check from k-v database.

### Private messaging

We want strong consistency in case of private messaging as we do not want users to see stale messages or out of order messages. Data is critical here and in CAP theorem we will favor consistency over availability when failures happen.

- We can use techniques like message queues to ensure messages are delivered in order and not lost.
- We can use acknowledgements to ensure messages are delivered and seen by the recipient.
- We can use techniques like sharding and partitioning to scale the databases to handle large number of reads and writes.
- We can use caching at different layers - CDN, edge servers, redis etc. to serve data faster and reduce load on main databases.

### How would you handle message delivery status?

For messaging, we can use websockets as a bi directional communication mechanism. If the user is online the message gets delivered to them instantly.

However if the user is facing network glitches or is offline, we will be using a message queue and will hold off the messages in the message queue and deliver the message to user when their network recovers or they come back online.
Message queue offers at least once guarantee which is what we want for message delivery.

For user experience we can rely on single tick if message is not delivered, double ticks if message is delivered and blue double ticks if message is read unless the recipient has not turned off read receipts.

### How would you ensure privacy settings are applied correctly?

To ensure privacy settings are applied correctly, we can store a boolean flag in the database table for private account. When the user want to switch to a private account, we will toggle this flag in the database. This is a simple solution.
However using a database to do this operation can be costly at large scale, we can use key value store like redis to store privacy settings where key will be lets say user id and value can be boolean to indicate if its private account.

Now redis has limited capacity, so we can store this data in a k-v database like dynamo db and also on redis for faster access.

For user experience we can use read your writes consistency where the user will see their changes instantly while it takes time for changes to propagate to other friends.
Also if people try to access the private account, we will check the privacy settings from redis first and if not found we will check from k-v database.

### How would you handle count discrepancies for likes/comments?

For like and comment counter as we mentioned above we will be using eventual consistency along with read your writes consistency. This will mean some users will see stale data for sometime.

- To handle such count discrepancies, we can use background jobs to update the counts in the database and also use caching at different layers - CDN, edge servers, redis etc. to serve data faster and reduce load on main databases.
- We can also use techniques like batching to update counts in background jobs to reduce load on main databases.
- We can also use CRDTs to merge changes when users simultaneously like or comment on the post.
- We can also use techniques like sharding and partitioning to scale the databases to handle large number of reads and writes.
- We can also use write through cache to update the cache along with the database to ensure that cache is always in sync with the database.

