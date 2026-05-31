from typing import List, Dict, Set
from collections import defaultdict

class Solution:
    def profileStitching(self, profiles: List[List[str]]) -> List[List[str]]:
        if not profiles:
            return []
        
        profile_graph: Dict[str, List[str]] = defaultdict(list)
        email_to_name: Dict[str, str] = {}

        result: List[List[str]] = []
        temp_result: Set[str] = set()
        visited: Set[str] = set()

        for profile in profiles:
            name = ""
            for email in profile:
                if name == "":
                    name = email
                    continue

                profile_graph[profile[1]].append(email)
                profile_graph[email].append(profile[1])
                email_to_name[email] = name

        for email in profile_graph:
            if email not in visited:
                temp_result = set()
                self.dfs(email, profile_graph, temp_result, visited)
                sorted_emails = sorted(temp_result)
                name = email_to_name[email]
                result.append([name] + list(sorted_emails))

        return result
    
    def dfs(self, email: str, profile_graph: Dict[str, List[str]], temp_result: Set[str], visited: Set[str]):
        temp_result.add(email)
        visited.add(email)

        for next_email in profile_graph[email]:
            if next_email not in visited:
                self.dfs(next_email, profile_graph, temp_result, visited)