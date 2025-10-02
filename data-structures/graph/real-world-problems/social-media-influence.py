"""
**Problem 1: Social Media Influence Analysis**
You're building a feature for a social media platform to identify influential user groups. 
Given a directed graph where edges represent "follows" relationships, 
design an algorithm to find groups of users who all follow each other (directly or indirectly through the group).
These groups represent echo chambers where information circulates within the group but doesn't easily escape to other parts of the network.

**Follow-up**: How would you handle millions of users? What if the graph changes frequently?
"""

from typing import List, Dict
from enum import Enum

class TraversalState(Enum):
    NOT_STARTED = "Not Started"
    VISITING = "Visiting"
    VISITED = "Visited"

class User:
    def __init__(self, name: str):
        self.name = name
        self.followers: List['User'] = []
        
    def add_follower(self, user: 'User'):
        self.followers.append(user)
        
    def get_followers(self) -> List['User']:
        return self.followers

class SocialMediaGraph:
    def __init__(self):
        self.users: Dict[str, User] = {}
        
    def add_user(self, name: str):
        self.users[name] = User(name)
        
    def get_users(self) -> List[User]:
        return self.users.values()
    
    def add_follower_relationship(self, followee_name: str, follower_name: str):
        followee = self.users[followee_name]
        follower = self.users[follower_name]
        
        if followee is None or follower is None:
            return
        
        followee.add_follower(follower)
        
def transpose_graph(graph: SocialMediaGraph) -> SocialMediaGraph:
    transposed_graph = SocialMediaGraph()
    
    users = graph.get_users()
    
    for user in users:
        transposed_graph.add_user(user.name)
        
    for user in users:
        for follower in user.get_followers():
            transposed_graph.add_follower_relationship(follower.name, user.name)
    
    return transposed_graph

def find_influential_user_groups(graph: SocialMediaGraph) -> List[List[User]]:
    finish_order = find_finish_order(graph)
    return find_groups(graph, finish_order)

def find_finish_order(graph: SocialMediaGraph) -> List[User]:
    users = graph.get_users()
    
    user_states: Dict[User, TraversalState] = {}
    
    for user in users:
        user_states[user] = TraversalState.NOT_STARTED
        
    order: List[User] = []
    
    for user in users:
        if user_states[user] == TraversalState.NOT_STARTED:
            _find_finish_order(user, user_states, order)
            
    return order

def _find_finish_order(user: User, user_states: Dict[User, TraversalState], order: List[User]):
    user_states[user] = TraversalState.VISITING
    
    for follower in user.get_followers():
        if user_states[follower] == TraversalState.NOT_STARTED:
            _find_finish_order(follower, user_states, order)
            
    order.append(user)
    user_states[user] = TraversalState.VISITED
    
def find_groups(graph: SocialMediaGraph, order: List[User]) -> List[List[User]]:
    result: List[List[User]] = []
    
    user_states: Dict[User, TraversalState] = {}
    
    transposed_graph = transpose_graph(graph)
    
    users = transposed_graph.get_users()
    
    for user in users:
        user_states[user] = TraversalState.NOT_STARTED
        
    for user in reversed(order):
        group: List[User] = []
        transposed_user = transposed_graph.users[user.name]
        if user_states[transposed_user] == TraversalState.NOT_STARTED:
            _find_group(transposed_user, user_states, group)
            result.append(group)
            
    return result

def _find_group(user: User, user_states: Dict[User, TraversalState], group: List[User]):
    group.append(user)
    user_states[user] = TraversalState.VISITING
    
    for follower in user.get_followers():
        if user_states[follower] == TraversalState.NOT_STARTED:
            _find_group(follower, user_states, group)
    
    user_states[user] = TraversalState.VISITED

def main():
    graph = build_social_media_graph()
    influential_groups = find_influential_user_groups(graph)
    print("Influential User Groups:")
    for group in influential_groups:
        print([user.name for user in group])

def build_social_media_graph() -> SocialMediaGraph:
    graph = SocialMediaGraph()
    graph.add_user("Alice")
    graph.add_user("Bob")
    graph.add_user("Charlie")
    graph.add_user("David")
    graph.add_user("Eve")

    graph.add_follower_relationship("Alice", "Bob")
    graph.add_follower_relationship("Bob", "Charlie")
    graph.add_follower_relationship("Charlie", "Alice")
    graph.add_follower_relationship("David", "Eve")
    graph.add_follower_relationship("Eve", "David")
    graph.add_follower_relationship("David", "Alice")
    

    return graph

if __name__ == "__main__":
    main()
    
