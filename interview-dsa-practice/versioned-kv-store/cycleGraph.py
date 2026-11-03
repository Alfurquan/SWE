from typing import List, Dict
from collections import defaultdict
from enum import Enum

class TraversalState(Enum):
    Not_Visited = "NotVisited"
    Visiting = "Visiting"
    Visited = "Visited"

def find_cycle(components: List[str], dependencies: List[List[str]]) -> List[str]:
    adj_list: Dict[str, List[str]] = defaultdict(list)

    states: Dict[str, TraversalState] = {comp: TraversalState.Not_Visited for comp in components}

    path: List[str] = []
    comp_to_index: Dict[str, int] = {}
    cycle: List[str] = []

    for dependency in dependencies:
        adj_list[dependency[1]].append(dependency[0])

    for comp in components:
        if states[comp] == TraversalState.Not_Visited:
            path = []
            comp_to_index = {}
            cycle = []
            if cycle_exists(comp, adj_list, states, path, 0, comp_to_index, cycle):
                return cycle

    return []


def cycle_exists(comp: str, adj_list: Dict[str, List[str]], states: Dict[str, TraversalState], path: List[str], index: int, comp_to_index: Dict[str, int], cycle: List[str]) -> bool:
    states[comp] = TraversalState.Visiting
    path.append(comp)
    comp_to_index[comp] = index

    for next_comp in adj_list[comp]:
        if states[next_comp] == TraversalState.Not_Visited:
            if cycle_exists(next_comp, adj_list, states, path, index + 1, comp_to_index, cycle):
                return True
        elif states[next_comp] == TraversalState.Visiting:
            next_comp_index_in_path = comp_to_index[next_comp]
            cycle[:] = path[next_comp_index_in_path:] + [next_comp]
            return True

    states[comp] = TraversalState.Visited
    return False
    