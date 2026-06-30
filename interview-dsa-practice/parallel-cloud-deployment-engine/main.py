from typing import Dict, List, Deque
from collections import deque

class Resource:
    def __init__(self, name: str):
        self.name = name
        self.dependencies = []

    def add_dependency(self, dependency: 'Resource'):
        self.dependencies.append(dependency)

    def get_dependencies(self) -> List['Resource']:
        return self.dependencies
    
class CloudDeploymentEngine:
    def __init__(self):
        self.resources: Dict[str, Resource] = {}

    def add_resource(self, name: str):
        self.resources[name] = Resource(name)

    def add_dependency(self, from_name: str, to_name: str):
        from_resource = self.resources.get(from_name, None)
        to_resource = self.resources.get(to_name, None)

        if from_resource is None or to_resource is None:
            return
        
        to_resource.add_dependency(from_resource)

    def get_order(self) -> List[str]:
        queue: Deque[Resource] = deque()

        order: List[str] = []

        in_degree: Dict[Resource, int] = {resource : 0 for resource in self.resources.values()}

        for resource in self.resources.values():
            for dependency in resource.get_dependencies():
                in_degree[dependency] += 1

        for resource in self.resources.values():
            if in_degree[resource] == 0:
                queue.append(resource)

        while queue:
            resource = queue.popleft()

            order.append(resource.name)

            for next_resource in resource.get_dependencies():
                in_degree[next_resource] -= 1

                if in_degree[next_resource] == 0:
                    queue.append(next_resource)

        
        return [] if len(order) != len(self.resources) else order
    
    def get_stages(self) -> List[List[str]]:
        queue: Deque[Resource] = deque()

        stages: List[List[str]] = []

        in_degree: Dict[Resource, int] = {resource : 0 for resource in self.resources.values()}

        for resource in self.resources.values():
            for dependency in resource.get_dependencies():
                in_degree[dependency] += 1

        for resource in self.resources.values():
            if in_degree[resource] == 0:
                queue.append(resource)

        while queue:
            stage_size = len(queue)
            stage: List[str] = []

            for _ in range(stage_size):
                resource = queue.popleft()

                stage.append(resource.name)

                for next_resource in resource.get_dependencies():
                    in_degree[next_resource] -= 1

                    if in_degree[next_resource] == 0:
                        queue.append(next_resource)

            stages.append(stage)
        
        return [] if sum(len(stage) for stage in stages) != len(self.resources) else stages
    

deployment_engine = CloudDeploymentEngine()
deployment_engine.add_resource("VM")
deployment_engine.add_resource("VNet")
deployment_engine.add_resource("Subnet")
deployment_engine.add_resource("StorageAccount")
deployment_engine.add_dependency("VM", "Subnet")
deployment_engine.add_dependency("Subnet", "VNet")
# deployment_engine.add_dependency("Subnet", "VM")

print(deployment_engine.get_order())
print(deployment_engine.get_stages())