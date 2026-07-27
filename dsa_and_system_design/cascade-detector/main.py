from typing import List, Dict, Set
from collections import OrderedDict
from enum import Enum

class Service:
    def __init__(self, name: str):
        self.name = name
        self.dependents: List['Service'] = []
        self.total_deps = 0
        self.unhealthy_deps = 0
        self.is_healthy = True

    def add_dependency(self, service: 'Service'):
        self.dependents.append(service)

    def toggle_health_status(self):
        self.is_healthy = not self.is_healthy
    
class CascadeDetector:
    def __init__(self):
       self.unhealthy_services: Set[Service] = set()
       self.at_risk_services: Dict[Service, bool] = OrderedDict()
       self.services: Dict[str, Service] = {}

    def add_service(self, name: str):
        self.services[name] = Service(name)

    def add_dependency(self, service: str, depends_on: str):
        to_service = self.services.get(service, None)

        from_service = self.services.get(depends_on, None)

        if from_service is None or to_service is None:
            return
        
        from_service.add_dependency(to_service)
        to_service.total_deps += 1

    def report_status(self, service_name: str, timestamp: int, healthy: bool):
        service = self.services.get(service_name, None)

        if service is None:
            return

        if service.is_healthy == healthy:
            return
        
        service.toggle_health_status()
        if not service.is_healthy:
            self.unhealthy_services.add(service)
        else:
            if service in self.unhealthy_services:
                self.unhealthy_services.remove(service)

        for dependent in service.dependents:
            if not service.is_healthy:
                dependent.unhealthy_deps += 1
            else:
                dependent.unhealthy_deps -= 1

            if dependent.unhealthy_deps * 2 >= dependent.total_deps:
                self.at_risk_services[dependent] = True
            else:
                if dependent in self.at_risk_services:
                    self.at_risk_services.pop(dependent)

    def get_at_risk_services(self) -> List[str]:
        return [service.name for service in self.at_risk_services]

    def get_root_causes(self) -> List[str]:
        return [service.name for service in self.unhealthy_services if service.unhealthy_deps == 0]


            