# Exercise 1: Global User Profile Service (Replication Choice)

## Problem

Design a User Profile Service with:

- Users in US, EU, India
- Low-latency reads locally
- Users can update profile from any region
- Data: name, photo, preferences (moderate write frequency, not financial)

## Your Task (keep it concise)

Do both designs:

### A. Single-Leader Replication

Explain:

- Where the leader is (or how it’s chosen)
- Where reads go
- How replication happens
- What happens if:

    - A region goes down
    - Network partition
    - User updates profile during failure

### B. Multi-Leader Replication

Explain the same four points, plus:

- How conflicts are detected
- How conflicts are resolved
- One real risk of this approach

---

## Solution

### A. Single Leader Replication

- Where the leader is: The leader here will be in a single datacenter which will be chosen as the global datacenter. Write requests for all the users around the world will go to this single leader in the global datacenter.

- Where reads go: Each regional datacenters will have followers, which will be serving read requests from users in the same regions. For e.g all Indian users read requests will be served by followers in datacenter located in India. Morever the data for Indian users will also be replicated to lets say Americas data center which will be used as backup in case the datacenter in India goes down. Serving read requests from regional datancenters ensure low latency and faster reads.

- How replication happens: Whenever a user updates their profile, the write requests goes to the single leader in the global datacenter. The leader writes the requests in a WAL and then updates its local copy. Now replication happens and it can happen both synchronously as well asynchronously. If it happens synchronously, the leader will wait for all replicas (followers) to respond and then send the success message back to the user for the write requests. If any of the follower is having failures, the write request will be halted. In case of asynchronous replication, the leader immediately returns back to the user after updating its local copy. Replication happens in the background, where the leader sends the replication log to the followers. 

- What happens if
    - A region goes down: Lets say a region, India goes down. Now users sending read requests to read their profiles from India would be impacted. Since their data is replicated across multiple datacenters, the requests will be served from US datacenter till the time India datacenter is down. This will increase the latency for read requests, but gives a better user experience and makes the application highly available. 
    Now what happens to replication process if a region is down, then to tackle that, each follower in a region will maintain a log of the updates they have applied. When the region comes back up again, the followers in that region, will request the leader of all the changes till the last update log they have applied. This way they can keep up with the updates that happened when they were down.

    - Network Parition: In case of network partition, both the replication process across regions and the write request will be impacted. For the write requests, if the user is trying to update their profile from a region which is partitioned from the leader, the write request will fail. The user will get an error message indicating that the service is unavailable. For replication process, if a follower is partitioned from the leader, it will not be able to receive the replication logs. The leader will keep track of the followers which are partitioned and when they come back online, it will send all the updates that happened during the partition to those followers.

    - User updates profile during failure: If a user tries to update their profile during a failure (like region down or network partition), the write request will fail. The user will receive an error message indicating that the service is unavailable. The user can retry the update once the service is back online.


### B. Multi-Leader Replication

- Where the leaders are: In multi-leader replication, each region (US, EU, India) will have its own leader. Users in each region will send their write requests to the local leader in their respective regions.

- Where reads go: Similar to single-leader replication, read requests will be served by followers in the same region as the user. This ensures low-latency reads.

- How replication happens: Whenever a user updates their profile, the write request goes to the local leader in their region. The leader updates its local copy and then replicates the changes to other leaders in different regions asynchronously. Each leader will also replicate the changes to its local followers for serving read requests.

- What happens if
    - A region goes down: If a region goes down, users in that region will not be able to send write requests as their local leader is down. However, they can still send read requests which will be served by followers in other regions. Once the region comes back up, the local leader will synchronize with other leaders to get the latest updates.

    - Network Partition: In case of network partition, leaders in different regions may not be able to communicate with each other. This can lead to inconsistencies as updates made in one region may not be propagated to other regions. Users in partitioned regions can still send write requests to their local leaders, but those updates may not be reflected in other regions until the partition is resolved.

    - User updates profile during failure: If a user tries to update their profile during a failure (like region down or network partition), the write request will go to the local leader if it is available. If the local leader is down, the write request will fail. If the local leader is available but partitioned from other leaders, the update will be applied locally but may not be propagated to other regions until the partition is resolved.

- How conflicts are detected: Conflicts can be detected using versioning or timestamps. Each update can carry a version number or timestamp, and when a leader receives an update from another leader, it can compare the version/timestamp to determine if there is a conflict.

- How conflicts are resolved: Conflicts can be resolved using strategies like "last write wins" where the update with the latest timestamp is accepted, or by merging changes if possible. For example, if two users update different fields of the profile simultaneously, both changes can be merged.

- One real risk of this approach: One real risk of multi-leader replication is data inconsistency. Since updates can be made in multiple regions simultaneously, there is a risk that conflicting updates may not be resolved correctly, leading to inconsistent user profiles across different regions. This can result in a poor user experience and potential data integrity issues. Also for resolving conflicts if we choose "last write wins" strategy, it may lead to loss of important updates made by users in different regions.

---

## Followups

### Scenario

We chose Single-Leader Replication (Leader in US, Followers in EU/India). Constraint: The Product Manager says, "It is unacceptable for an Indian user to update their profile and see the old photo immediately after."

### Task

Propose 2 specific solutions to ensure Read-Your-Own-Writes consistency for this Indian user, and explain the trade-off of each.

### Answer

Here are the two specific solutions to ensure Read-Your-Own-Writes consistency for this Indian user

#### Solution 1: Read from the leader

First solution here is to read from the leader till atleast 1 minute after making changes to the profile to ensure the user sees the updated information as the data is getting replicated across to the followers. 

Trade offs

- Increased Latency: Reading from the leader can increase the latency for read requests, especially for users located far from the leader's datacenter. This can lead to a poor user experience.
- Load on Leader: This approach can increase the load on the leader as it will be handling both read and write requests. This can lead to performance degradation if the leader is not scaled properly.
- Stale Reads: If the user reads from the followers after the 1 minute window, they may still see stale data if the replication is delayed.

Mostly this approach is suitable for scenarios where the user is okay with slightly increased latency for the sake of consistency. Also this approach takes into account the fact that other users can continue to see old data till the replication is complete, like its fine for other users to see old data, but the user who made the update should see the latest data.

#### Solution 2: Client remembering write timestamp

Second solution here is to have the client remember the timestamp of the last write operation. When the user makes an update to their profile, the client stores the timestamp of that update. For subsequent read requests, the client includes this timestamp in the request. The read request will then be directed to the follower having data at least as recent as the provided timestamp. If the follower does not have the latest data, the request can be redirected to the leader or a more up-to-date follower. The routing will be handled by the load balancer or a middleware layer.

Trade offs

- Increased Complexity: This approach adds complexity to the client-side logic, as the client needs to manage timestamps and handle redirection of read requests based on data freshness.

- Potential Increased Latency: If the read request needs to be redirected to the leader or a more up-to-date follower, it can increase the latency for read requests.

- Scalability: This approach can help in distributing the read load across followers, as not all read requests will go to the leader. Only those requests that require the latest data will be redirected to the leader or up-to-date followers.

This approach is suitable for scenarios where the user expects low latency for most read requests, but also wants to ensure consistency for their own updates. It allows for better scalability as read requests can be served by followers when possible.





