# Load balancing algorithms

Load balancing is the process of distributing incoming network traffic across multiple servers to ensure that no single server is overwhelmed.

By evenly spreading the workload, load balancing aims to prevent overload on a single server, enhance performance by reducing response times and improve availability by rerouting traffic in case of server failures.

## Algorithm 1: Round robin

### How it works ?

- A request is sent to the first server in the list
- The next request is sent to the second server, and so on.
- After the last server in the list, the algorithm loops back to the first server.

### When to use ?

- When all servers have similar processing capabilities and are equally capable of handling requests.
- When simplicity and even distribution of load is more critical.

```python
class RoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = -1

    def get_next_server(self):
        self.current_index = (self.current_index + 1) % len(self.servers)
        return self.servers[self.current_index]

# Example usage
servers = ["Server1", "Server2", "Server3"]
load_balancer = RoundRobin(servers)

for i in range(6):
    server = load_balancer.get_next_server()
    print(f"Request {i + 1} -> {server}")
```

## Algorithm 2: Weighted Round Robin

### How it works ?

- Each server is assigned a weight based on their processing power or available resources.
- Servers with higher weights receive a proportionally larger share of incoming requests.

### When to use ?

- When servers have different processing capabilities or available resources.
- When you want to distribute load based on the capacity of the server.

```python
class WeightedRoundRobin:
    def __init__(self, servers, weights):
        self.servers = servers
        self.weights = weights
        self.current_index = -1
        self.current_weight = 0

    def get_next_server(self):
        while True:
            self.current_index = (self.current_index + 1) % len(self.servers)
            if self.current_index == 0:
                self.current_weight -= 1
                if self.current_weight <= 0:
                    self.current_weight = max(self.weights)
            if self.weights[self.current_index] >= self.current_weight:
                return self.servers[self.current_index]

# Example usage
servers = ["Server1", "Server2", "Server3"]
weights = [5, 1, 1]
load_balancer = WeightedRoundRobin(servers, weights)

for i in range(7):
    server = load_balancer.get_next_server()
    print(f"Request {i + 1} -> {server}")
```

## Algorithm 3: Least connections

### How it works ?

- Monitor the number of active connections on each server.
- Assigns incoming requests to the server with the least number of active connections.

### When to use it ?

- When you want to distribute the load based on the current number of active connections.
- When servers have similar processing capabilities but may have different levels of concurrent connections.

```python
import random

class LeastConnections:
    def __init__(self, servers):
        self.servers = {server: 0 for server in servers}

    def get_next_server(self):
        min_connections = min(self.servers.values())
        least_loaded = [server for server, count in self.servers.items() if count == min_connections]
        selected = random.choice(least_loaded)
        self.servers[selected] += 1
        return selected

    def release_connection(self, server):
        if self.servers[server] > 0:
            self.servers[server] -= 1

# Example usage
servers = ["Server1", "Server2", "Server3"]
load_balancer = LeastConnections(servers)

for i in range(6):
    server = load_balancer.get_next_server()
    print(f"Request {i + 1} -> {server}")
    load_balancer.release_connection(server)
```

## Algorithm 4: Least Response Time

### How it works ?

- Monitors the response time of each server
- Assigns incoming requests to the server with the fastest response time.

### When to use ?

- When you have servers with varying response times and want to route requests to the fastest server.

```python
import time
import random

class LeastResponseTime:
    def __init__(self, servers):
        self.servers = servers
        self.response_times = [0] * len(servers)

    def get_next_server(self):
        min_time = min(self.response_times)
        min_index = self.response_times.index(min_time)
        return self.servers[min_index]

    def update_response_time(self, server, response_time):
        index = self.servers.index(server)
        self.response_times[index] = response_time

def simulate_response_time():
    delay = random.uniform(0.1, 1.0)
    time.sleep(delay)
    return delay

# Example usage
servers = ["Server1", "Server2", "Server3"]
load_balancer = LeastResponseTime(servers)

for i in range(6):
    server = load_balancer.get_next_server()
    print(f"Request {i + 1} -> {server}")
    response_time = simulate_response_time()
    load_balancer.update_response_time(server, response_time)
    print(f"Response Time: {response_time:.2f}s")
```

## Algorithm 5: IP Hash

### How it works ?

- Calculates a hash value from the client’s IP address and uses it to determine the server to route the request.

### When to use ?

- When you need session persistence, as requests from the same client are always directed to the same server.

```python
import hashlib

class IPHash:
    def __init__(self, servers):
        self.servers = servers

    def get_next_server(self, client_ip):
        hash_value = hashlib.md5(client_ip.encode()).hexdigest()
        index = int(hash_value, 16) % len(self.servers)
        return self.servers[index]

# Example usage
servers = ["Server1", "Server2", "Server3"]
load_balancer = IPHash(servers)

client_ips = ["192.168.0.1", "192.168.0.2", "192.168.0.3", "192.168.0.4"]
for ip in client_ips:
    server = load_balancer.get_next_server(ip)
    print(f"Client {ip} -> {server}")
```

## Summary

- Round Robin: Simple and even distribution, best for homogeneous servers.
- Weighted Round Robin: Distributes based on server capacity, good for heterogeneous environments.
- Least Connections: Dynamically balances based on load, ideal for varying workloads.
- Least Response Time: Optimizes for fastest response, best for environments with varying server performance.
- IP Hash: Ensures session persistence, useful for stateful applications.
