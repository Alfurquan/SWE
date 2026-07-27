# The Cascade Detector

You're building a service mesh health monitor. Services depend on other services, forming a directed acyclic graph. When a service goes unhealthy, services that depend on it may become "at risk."

Implement a CascadeDetector with these methods:

add_dependency(service, depends_on) — declare that service depends on depends_on
report_status(service, timestamp, healthy: bool) — report a health status change for a service
get_at_risk_services() -> List[str] — return all services where ≥50% of their direct dependencies are currently unhealthy. Ordered by the timestamp they first became at-risk.
get_root_causes() -> List[str] — return all unhealthy services that have no unhealthy dependencies themselves (the origin points of failure).

Example

```shell
add_dependency("api-gateway", "auth")
add_dependency("api-gateway", "payments")
add_dependency("api-gateway", "inventory")
add_dependency("payments", "database")
add_dependency("payments", "cache")

report_status("database", t=100, healthy=False)
report_status("cache", t=105, healthy=False)

# Now: "payments" has 2/2 deps unhealthy → at-risk (became at-risk at t=105)
# "api-gateway" has 1/3 deps unhealthy (just payments is at-risk, not unhealthy) → NOT at-risk
# root_causes → ["database", "cache"] (both unhealthy with no unhealthy deps of their own)

report_status("payments", t=110, healthy=False)  # payments actually goes down

# Now: "api-gateway" has 1/3 deps unhealthy (payments) → NOT at-risk (33% < 50%)
# "checkout" has 1/2 deps unhealthy (payments) → at-risk at t=110 (50% ≥ 50%)
# root_causes → ["database", "cache"] (payments is unhealthy BUT has unhealthy deps, so not a root cause)
```
---

## Approach

Here is a high level approach of how I am thinking about this problem
We will model the dependency relationship using a graph using a dictionary in python.

### Data Structures

- Dictionary to hold a service to a list of dependents. Basically, if lets say api-gateway is dependent on auth, payments. The dict will map auth -> [api-gateway], payments -> [api-gateway]. This will be useful and efficent to track changes to at risk status of services over time.
- Each service will also hold count of dependencies they have and count of unhealthy dependencies they have. This will be useful to track if a service is at risk or not. Basically like total_deps and unhealthy_deps count for each service.
- An ordered dict to store list of at risk services in ordered by the timestamp they became at risk
- A set of unhealthy services.

### Logic

- add_dependency(service, depends_on)
    - Update the list in the dictionary for depends_on to include service
    - Update count of service to increment by 1

- report_status(service, timestamp, healthy: bool)
    - If healthy is false, means service is unhealthy, add it to the set of unhealthy service, else remove from the set of unhealthy services
    - Propagate the health status using the dictionary to all the dependent services. The dependent services keep track of unhealthy dependencies using the count variable and update the count accordingly. If count becomes >= 50% of their total dependencies, add the service to the ordered dict of at risk service at the time passed in this function call. 
    If the count is less than 50%, remove the service from the ordered dict of at risk services if present, else do nothing.
    We only propagate if the health status only changes.

- get_at_risk_services() -> List[str]
    - Return all the services present in the at risk ordered dict.

- get_root_causes() -> List[str]
    - For all unhealthy services in the set of unhealthy services, if the service has unhealthy dependencies count as 0, return them in the result list

### Time complexity

- add_dependency: O(1) to update the dict
- report_status: O(n) where n is the number of dependent services for the service being reported. In worst case, it can be O(m) where m is the total number of services in the system.
- get_at_risk_services: O(k) where k is the number of at risk services
- get_root_causes: O(u) where u is the number of unhealthy services

### Space complexity

- O(m) where m is the total number of services in the system. We are storing the dependency graph, unhealthy services, and at risk services in memory.


