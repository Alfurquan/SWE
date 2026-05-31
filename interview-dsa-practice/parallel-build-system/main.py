from typing import List, Dict, Deque, Tuple
from collections import deque

class Package:
    def __init__(self, name: str, build_time: int, dependents: List['Package'] = None):
        self.name = name
        self.build_time = build_time
        self.dependents = dependents if dependents else []

    def add_dependent(self, dependent: 'Package'):
        self.dependents.append(dependent)

class BuildSystem:
    def __init__(self):
        self.packages: Dict[str, Package] = {}

    def add_package(self, name: str, build_time: int):
        if name in self.packages:
            raise ValueError(f"Package '{name}' already exists.")
        
        package = Package(name, build_time)
        self.packages[name] = package
        
    def add_dependent(self, package_name: str, dependent_name: str):
        if package_name not in self.packages:
            raise ValueError(f"Package '{package_name}' does not exist.")
        if dependent_name not in self.packages:
            raise ValueError(f"Dependent '{dependent_name}' does not exist.")
        
        package = self.packages[package_name]
        dependent = self.packages[dependent_name]
        
        package.add_dependent(dependent)

    def get_min_total_build_time(self) -> int:
        in_degree: Dict[str, int] = {
            package_name: 0 for package_name in self.packages
        }
        package_start_times: Dict[Package, int] = {}

        for package in self.packages.values():
            for dependent in package.dependents:
                in_degree[dependent.name] += 1
            
        queue: Deque[Tuple[Package, int]] = deque()

        for package_name in in_degree:
            if in_degree[package_name] == 0:
                package = self.packages[package_name]
                queue.append((package, package.build_time))

        min_completion_time = 0
        order: List[Package] = []

        while queue:
            package, completion_time = queue.popleft()

            min_completion_time = max(min_completion_time, completion_time)
            order.append(package)

            for dependent in package.dependents:
                if dependent not in package_start_times:
                    package_start_times[dependent] = 0
                
                package_start_times[dependent] = max(package_start_times[dependent], completion_time)

                in_degree[dependent.name] -=1

                if in_degree[dependent.name] == 0:
                    queue.append((dependent, package_start_times[dependent] + dependent.build_time))

        return -1 if len(order) != len(self.packages) else min_completion_time
