from enum import Enum


class NodeState(Enum):
    NOT_STARTED = 'Not Started'
    VISITING = 'Visiting'
    VISITED = 'Visited'