from collections import defaultdict, deque
from typing import List, Dict
from enum import Enum
from dataclasses import dataclass, field

class TraversalState(Enum):
    NOT_STARTED = "Not Started"
    VISITING = "Visiting"
    VISITED = "Visited"
    
class Microservice:
    def __init__(self, name: str):
        self.name = name
        self.dependencies: List['Microservice'] = []
        
    def add_dependency(self, service: 'Microservice'):
        self.dependencies.append(service)

    def get_dependencies(self) -> List['Microservice']:
        return self.dependencies
    
    def __repr__(self) -> str:
        return self.name
    
@dataclass
class Deployment:
    is_possible: bool
    order: List[Microservice] = field(default_factory=list)

@dataclass
class LevelOrderDeployment:
    level: str
    services: List[Microservice]

class MicroserviceGraph:
    def __init__(self):
        self.microservices: Dict[str, Microservice] = {}
        
    def add_microservice(self, name:str):
        self.microservices[name] = Microservice(name)
    
    def get_microservices(self) -> List[Microservice]:
        return self.microservices.values()
    
    def add_dependency(self, from_microservice_name: str, to_microservice_name: str):
        from_microservice = self.microservices.get(from_microservice_name, None)
        to_microservice = self.microservices.get(to_microservice_name, None)
        
        if from_microservice == None:
            print(f"Microservice with name {from_microservice_name} not found")
            return
        
        if to_microservice == None:
            print(f"Microservice with name {to_microservice_name} not found")
            return
        
        from_microservice.add_dependency(to_microservice)
        
def deploy(graph: MicroserviceGraph) -> Deployment:
    service_states: Dict[Microservice, TraversalState] = {}
    services = graph.get_microservices()
    
    for service in services:
        service_states[service] = TraversalState.NOT_STARTED
        
    order: List[Microservice] = []
    
    for service in services:
        if service_states[service] == TraversalState.NOT_STARTED:
            if find_deployment_order(service, service_states, order) == False:
                return Deployment(is_possible=False, order=[])
        
    return Deployment(is_possible=True, order=order)

def find_deployment_order(service: Microservice, 
                          service_states: Dict[Microservice, TraversalState], 
                          order: List[Microservice]) -> bool:
    
    service_states[service] = TraversalState.VISITING
    
    for dependency in service.get_dependencies():
        if service_states[dependency] == TraversalState.VISITING:
            return False
        
        elif service_states[dependency] == TraversalState.NOT_STARTED and find_deployment_order(dependency, service_states, order) == False:
            return False
        
    order.append(service)
    service_states[service] = TraversalState.VISITED
    return True

def find_parallel_deployment_order(graph: MicroserviceGraph) -> List[LevelOrderDeployment]:
    services = graph.get_microservices()
    in_degree: Dict[Microservice, int] = {}
    deployments : List[LevelOrderDeployment] = []
    dependents_map: Dict[Microservice, List[Microservice]] = defaultdict(list)
    
    for service in services:
        in_degree[service] = len(service.get_dependencies())
        for dep in service.get_dependencies():
            dependents_map[dep].append(service)
        
    queue = deque([s for s in services if in_degree[s] == 0])
    level = 0
    print(queue)
    while queue:
        current_level = []
        size = len(queue)
        while size > 0:
            service = queue.popleft()
            current_level.append(service)
            
            for dependent in dependents_map[service]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
                    
            size -= 1

        deployments.append(LevelOrderDeployment(f"Level {level}", current_level))
        level += 1        
        
    return deployments

def main():
    # Test with cyclical graph
    print("=== Testing Cyclical Dependencies ===")
    graph = build_microservice_graph()
    deployment = deploy(graph)
    if deployment.is_possible:
        print("Deployment is possible")
        print("Deployment Order:")
        for service in deployment.order:
            print(f" - {service.name}")
    else:
        print("Deployment is not possible due to circular dependencies")
    
    # Test with valid graph for parallel deployment
    print("\n=== Testing Parallel Deployment ===")
    valid_graph = build_valid_microservice_graph()
    valid_deployment = deploy(valid_graph)
    if valid_deployment.is_possible:
        print("Deployment is possible")
        print("\nSequential Order:")
        for service in valid_deployment.order:
            print(f" - {service.name}")
        
        print("\nParallel Deployment Levels:")
        parallel_deployments = find_parallel_deployment_order(valid_graph)
        for level_deployment in parallel_deployments:
            service_names = [service.name for service in level_deployment.services]
            print(f"{level_deployment.level}: {service_names}")
    else:
        print("Deployment is not possible")

def build_microservice_graph() -> MicroserviceGraph:
    graph = MicroserviceGraph()
    graph.add_microservice("ServiceA")
    graph.add_microservice("ServiceB")
    graph.add_microservice("ServiceC")
    graph.add_microservice("ServiceD")

    graph.add_dependency("ServiceA", "ServiceB")
    graph.add_dependency("ServiceB", "ServiceC")
    graph.add_dependency("ServiceC", "ServiceD")
    graph.add_dependency("ServiceD", "ServiceA")  # This creates a circular dependency

    return graph

def build_valid_microservice_graph() -> MicroserviceGraph:
    """Build a graph without cycles for testing parallel deployment"""
    graph = MicroserviceGraph()
    graph.add_microservice("Database")
    graph.add_microservice("AuthService") 
    graph.add_microservice("UserService")
    graph.add_microservice("OrderService")
    graph.add_microservice("PaymentService")
    graph.add_microservice("WebUI")

    # Database has no dependencies (Level 0)
    # AuthService depends on Database (Level 1)
    graph.add_dependency("AuthService", "Database")
    
    # UserService and PaymentService depend on Database (Level 1)
    graph.add_dependency("UserService", "Database")
    graph.add_dependency("PaymentService", "Database")
    
    # OrderService depends on UserService and PaymentService (Level 2)
    graph.add_dependency("OrderService", "UserService")
    graph.add_dependency("OrderService", "PaymentService")
    
    # WebUI depends on AuthService and OrderService (Level 3)
    graph.add_dependency("WebUI", "AuthService")
    graph.add_dependency("WebUI", "OrderService")

    return graph

if __name__ == "__main__":
    main()