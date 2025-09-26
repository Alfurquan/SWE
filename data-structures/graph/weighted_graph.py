from graph import Graph, WeightedEdge

class WeightedGraph(Graph):
    def add_undirected_edge(self, from_node_label: str, to_node_label: str, weight: float = 1.0):
        from_node = self.nodes.get(from_node_label, None)
        to_node = self.nodes.get(to_node_label, None)
        
        if from_node == None:
            print(f"Node with label {from_node_label} not found")
            return
        
        if to_node == None:
            print(f"Node with label {to_node_label} not found")
            return
        
        from_node.add_edge(WeightedEdge(from_node, to_node, weight))
        to_node.add_edge(WeightedEdge(to_node, from_node, weight)) 
        
    def add_directed_edge(self, from_node_label: str, to_node_label: str, weight: float = 1.0):
        from_node = self.nodes.get(from_node_label, None)
        to_node = self.nodes.get(to_node_label, None)
        
        if from_node == None:
            print(f"Node with label {from_node_label} not found")
            return
        
        if to_node == None:
            print(f"Node with label {to_node_label} not found")
            return
        
        from_node.add_edge(WeightedEdge(from_node, to_node, weight))
        
    def add_edge(self, from_node_label: str, to_node_label: str, weight: float = 1.0):
        """Default implementation delegates to undirected edge for compatibility"""
        self.add_undirected_edge(from_node_label, to_node_label, weight)
        
    def create_transpose(self):
        pass
    
    def detect_cycle(self):
        pass