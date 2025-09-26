# Change data capture (CDC)

Modern applications often rely on multiple systems (e.g., search engines, caches, data lakes, microservices), all of which need up-to-date data.

Change Data Capture (CDC) is a design pattern used to track and capture changes in a database (inserts, updates, deletes) and stream those changes in real time to downstream systems.

This ensures downstream systems remain in sync without needing expensive batch jobs.

## How CDC works ?

- At a high level, CDC works by continuously monitoring a database for data changes (insertions, updates, and deletions).
- When a change occurs, CDC captures the change event and makes the information available for processing.

The process typically involves:

- Monitoring: Detecting changes from source systems. This can be achieved through database triggers, reading transaction logs, or using specialized CDC tools.
- Capturing: Extracting details about the change event (such as before and after values) along with metadata (e.g., timestamp, changed table).
- Delivering: Transmitting the change event to consumers, which might include message queues, data pipelines, or real-time analytics systems.

## CDC implementation approaches

### Time based CDC

- This approach relies on adding a last_updated or last_modified column to your database tables.
- Every time a row is inserted or modified, this column is updated with the current timestamp. Applications then query the table for rows where the last_updated time is later than the last sync time.

### Trigger based CDC

- Trigger-Based CDC involves setting up database triggers that automatically log changes to a separate audit table whenever an insert, update, or delete operation occurs.
- This audit table then serves as a reliable source of change records, which can be pushed to other systems as needed.

### Log-Based CDC

- Log-Based CDC reads changes directly from the database’s write-ahead log (WAL) or binary log (binlog).
- This method intercepts the low-level database operations, enabling it to capture every change made to the database without interfering with the application’s normal workflow.

**In modern applications, Log-based CDC is generally preferred because it efficiently captures all types of changes (inserts, updates, and deletes) directly from transaction logs, minimizes impact on the primary database, and scales well with high data volumes.**

## Real world use cases of CDC

### Microservice communication

- In a microservices architecture, individual services often need to communicate and share state changes without being tightly coupled.
- With CDC in place, the change is captured and propagated via a messaging system (such as Kafka) so that each microservice can stay updated on the relevant changes in other services' databases without needing direct service-to-service calls.

### Event sourcing

- Event sourcing involves recording every change to an application state as a sequence of events.
- CDC can be leveraged to capture these changes in real time, building a complete log of all modifications.

### Cache Invalidation

- Caches are used to improve application performance by storing frequently accessed data. However, stale cache data can cause issues, leading to outdated or incorrect information being displayed.
- CDC can trigger cache updates automatically whenever the underlying data changes.
