from typing import List, Dict
from enum import Enum

class TraversalState(Enum):
    NOT_STARTED = "Not Started"
    VISITING = "Visiting"
    VISITED = "Visited"
    
class Server:
    def __init__(self, name: str):
        self.name = name
        self.connections: List['Server'] = []
        
    def add_connections(self, server: 'Server'):
        self.connections.append(server)
        
    def get_connections(self) -> List['Server']:
        return self.connections
    
    def __repr__(self):
        return self.name
    
class NetworkGraph:
    def __init__(self):
        self.servers: Dict[str, Server] = {}
        
    def add_server(self, server_name):
        self.servers[server_name] = Server(server_name)
        
    def get_servers(self) -> List[Server]:
        return self.servers.values()
    
    def add_connection(self, from_server_name: str, to_server_name: str):
        from_server = self.servers.get(from_server_name, None)
        to_server = self.servers.get(to_server_name, None)
        
        if from_server == None:
            print(f"Server with name {from_server_name} not found")
            return
        
        if to_server is None:
            print(f"Server with name {to_server_name} not found")
            return
        
        from_server.add_connections(to_server)
        to_server.add_connections(from_server)
        

def find_critical_connections(graph: NetworkGraph) -> List[List[Server]]:
    server_states: Dict[Server, TraversalState] = {}
    disc: Dict[Server, int] = {}
    low: Dict[Server, int] = {}
    result: List[List[Server]] = []
    
    servers = graph.get_servers()
    
    for server in servers:
        server_states[server] = TraversalState.NOT_STARTED
    
    for server in servers:
        if server_states[server] == TraversalState.NOT_STARTED:
            _find_critical_connections(server, disc, low, server_states, None, 0, result)
            
    return result

def _find_critical_connections(server: Server,
                               disc: Dict[Server, int],
                               low: Dict[Server, int],
                               server_states: Dict[Server, TraversalState],
                               parent: Server,
                               time: int, 
                               result: List[List[Server]]):
    
    disc[server] = time
    low[server] = time
    server_states[server] = TraversalState.VISITING
    
    for connection in server.get_connections():
        if connection == parent:
            continue
        
        if server_states[connection] == TraversalState.NOT_STARTED:
            _find_critical_connections(connection, disc, low, server_states, server, time + 1, result)
            
            low[server] = min(low[server], low[connection])
            
            if low[connection] > disc[server]:
                result.append([server, connection])
                
        else:
            low[server] = min(low[server], low[connection])
            
    
    server_states[server] = TraversalState.VISITED
    
def main():
    graph = build_network_graph()
    critical_connections = find_critical_connections(graph)
    if len(critical_connections) == 0:
        print("No critical connections found")
    
    else:    
        print("Critical Connections:")
        for conn in critical_connections:
            print(f" - {conn[0].name} <-> {conn[1].name}")

    graph = build_graph_having_critical_connections()
    critical_connections = find_critical_connections(graph)
    if len(critical_connections) == 0:
        print("No critical connections found")
    else:
        print("Critical Connections in Graph")
        for conn in critical_connections:
            print(f" - {conn[0].name} <-> {conn[1].name}")

def build_network_graph() -> NetworkGraph:
    graph = NetworkGraph()
    
    graph.add_server("A")
    graph.add_server("B")
    graph.add_server("C")
    graph.add_server("D")

    graph.add_connection("A", "B")
    graph.add_connection("B", "C")
    graph.add_connection("C", "D")
    graph.add_connection("D", "A")

    return graph

def build_graph_having_critical_connections() -> NetworkGraph:
    graph = NetworkGraph()
    graph.add_server("A")
    graph.add_server("B")
    graph.add_server("C")
    graph.add_server("D")
    graph.add_server("E")
    graph.add_server("F")

    graph.add_connection("A", "B")
    graph.add_connection("B", "C")
    graph.add_connection("C", "D")
    graph.add_connection("D", "A")
    graph.add_connection("D", "E")
    graph.add_connection("E", "F")
 
    return graph

if __name__ == "__main__":
    main()

    