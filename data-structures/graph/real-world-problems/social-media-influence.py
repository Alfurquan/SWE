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
    
    def __repr__(self) -> str:
        return self.name
    
class SocialMediaGraph:
    def __init__(self):
        self.users: Dict[str, User] = {}
        
    def add_user(self, user_name: str):
        self.users[user_name] = User(user_name)
        
    def get_users(self) -> List[User]:
        return self.users.values()
        
    def add_follower_relationship(self, followee_name: str, follower_name: str):
        followee_user = self.users.get(followee_name, None)
        follower_user = self.users.get(follower_name, None)
        
        if followee_user is None:
            print(f"User with name {followee_name} not present")
            return
        
        if follower_user is None:
            print(f"User with name {follower_name} not present")
            return
        
        followee_user.add_follower(follower_user)
        
def find_influential_user_groups(graph: SocialMediaGraph) -> List[List[User]]:
    finish_order = find_finish_order(graph)
    return find_groups(transpose(graph), finish_order)

def find_finish_order(graph: SocialMediaGraph) -> List[User]:
    users = graph.get_users()
    user_states: Dict[User, TraversalState] = {}
    
    for user in users:
        user_states[user] = TraversalState.NOT_STARTED
        
    finish_order: List[User] = []
    
    for user in users:
        if user_states[user] == TraversalState.NOT_STARTED:
            dfs(user, user_states, finish_order)
            
    return finish_order

def dfs(user: User, user_states: Dict[User, TraversalState], finish_order: List[User]):
    user_states[user] = TraversalState.VISITING
    
    for follower in user.get_followers():
        if user_states[follower] == TraversalState.NOT_STARTED:
            dfs(follower, user_states, finish_order)
            
    user_states[user] = TraversalState.VISITED
    finish_order.append(user)
        
def transpose(graph: SocialMediaGraph) -> SocialMediaGraph:
    new_graph = SocialMediaGraph()
    
    for user in graph.get_users():
        new_graph.add_user(user.name)
        
    for user in graph.get_users():
        for follower in user.get_followers():
            new_graph.add_follower_relationship(follower.name, user.name)
            
    return new_graph

def find_groups(graph: SocialMediaGraph, finish_order: List[User]) -> List[List[User]]:
    users = graph.get_users()
    user_states: Dict[User, TraversalState] = {}
    
    for user in users:
        user_states[user] = TraversalState.NOT_STARTED
        
    groups: List[List[User]] = []
    
    for user in reversed(finish_order):
        group: List[User] = []
        transposed_user = graph.users[user.name]
        if user_states[transposed_user] == TraversalState.NOT_STARTED:
            _find_groups(transposed_user, user_states, group)
            groups.append(group)
    
    return groups

def _find_groups(user: User, user_states: Dict[User, TraversalState], group: List[User]):
    user_states[user] = TraversalState.VISITING
    group.append(user)
    
    for follower in user.get_followers():
        if user_states[follower] == TraversalState.NOT_STARTED:
            _find_groups(follower, user_states, group)
            
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
