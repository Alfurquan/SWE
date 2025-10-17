from dataclasses import dataclass
from typing import List, Dict
import hashlib
import bisect

@dataclass
class Server:
    id: str
    
class HashRing:
    def __init__(self, servers: List[Server], num_replicas = 3):
        self.num_replicas = num_replicas
        self.ring: List[int] = []
        self.servers: Dict[str, Server] = {}
        self.hash_to_server: Dict[int, str] = {}
        
        for server in servers:
            self.servers[server.id] = server
        
        self._build_ring()
    
    def get_server(self, key: str) -> Server:
        hash_val = self._hash(key)
        index = bisect.bisect(self.ring, hash_val) % len(self.ring)
        
        server_hash = self.ring[index]
        return self.servers[self.hash_to_server[server_hash]]
    
    def add_server(self, server: Server):
        self.servers[server.id] = server
        for replica in range(self.num_replicas):
            server_key = f"{server.id}#{replica}"
            hash_val = self._hash(server_key)
            bisect.insort(self.ring, hash_val)
            self.hash_to_server[hash_val] = server.id
            
    def remove_server(self, server_id: str):
        if server_id not in self.servers:
            return
        
        self.servers.pop(server_id)
        for replica in range(self.num_replicas):
            server_key = f"{server_id}#{replica}"
            hash_val = self._hash(server_key)
            self.hash_to_server.pop(hash_val)
            self.ring.remove(hash_val)
    
    def _build_ring(self):
        for server in self.servers.values():
            for replica in range(self.num_replicas):
                server_key = f"{server.id}#{replica}"
                hash_val = self._hash(server_key)
                self.hash_to_server[hash_val] = server.id
                self.ring.append(hash_val)
        
        self.ring.sort()
    
    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    
def main():
    servers: List[Server] = [Server("S0"), Server("S1"), Server("S2"), Server("S3"), Server("S4"), Server("S5")]
    consistent_hashing = HashRing(servers)
    print("Original assignment")
    print(consistent_hashing.get_server("UserA"))
    print(consistent_hashing.get_server("UserB"))

    consistent_hashing.add_server(Server("S6"))
    print("After adding server S6")
    print(consistent_hashing.get_server("UserA"))
    print(consistent_hashing.get_server("UserB"))
    
    print('After removing server S4')
    consistent_hashing.remove_server("S4")
    print(consistent_hashing.get_server("UserA"))
    print(consistent_hashing.get_server("UserB"))

if __name__ == '__main__':
    main()
    
    
    