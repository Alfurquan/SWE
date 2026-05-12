from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
import heapq

@dataclass
class NetworkEdge:
    to_server: str
    latency_ms: int

@dataclass
class Server:
    label: str
    edges: List[NetworkEdge] = []

    def add_edge(self, edge: NetworkEdge):
        self.edges.append(edge)

    def sync_file_changes(self, file_id: str):
        # Placeholder method for syncing file changes
        print(f"Syncing file changes for file_id: {file_id} on server {self.label}")

class NetworkGraph:
    def __init__(self):
        self.servers: Dict[str, Server] = {}

    def add_server(self, label: str):
        self.servers[label] = Server(label)
    
    def add_link(self, server_u_label: str, server_v_label: str, latency_ms: int):
        server_u = self.servers.get(server_u_label, None)
        server_v = self.servers.get(server_v_label, None)

        if server_u is None or server_v is None:
            return
        
        server_u.add_edge(NetworkEdge(server_v_label, latency_ms))
        server_v.add_edge(NetworkEdge(server_u_label, latency_ms))

    def get_sync_path(self, start_server: str) -> List[Tuple[str, str]]:
        visited: Dict[Server, bool] = {server: False for server in self.servers.values()}
        min_heap: List[Tuple[int, Server, str]] = [(0, self.servers[start_server], None)]
        mst: List[Tuple[str, str]] = []

        while min_heap:
            latency, server, parent = heapq.heappop(min_heap)

            if not visited[server]:
                visited[server] = True
                if parent != None:
                    mst.append((parent, server.label))
                
                for edge in server.edges:
                    next_server = self.servers[edge.to_server]
                    if not visited[next_server]:
                        heapq.heappush(min_heap, (edge.latency_ms, next_server, server))

        return mst
    
    def broadcast_update(self, file_id: str, start_server: str):
        sync_path: List[Tuple[str, str]] = self.get_sync_path(start_server)

        for _, to_server in sync_path:
            next_server = self.servers[to_server]
            next_server.sync_file_changes(file_id)