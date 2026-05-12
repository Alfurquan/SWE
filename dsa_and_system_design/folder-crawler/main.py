from typing import List, Set
from dataclasses import dataclass

@dataclass
class Entry:
    id: str
    is_file: bool
    is_public: bool
    children: List[str] = []

class ApiClient:
    def get_metadata(self, id: str) -> Entry:
        pass

class CloudCrawler:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def crawl(self, folder_id: str) -> List[str]:
        visited: Set[str] = set()

        result: Set[str] = set()

        todo_stack: List[str] = [folder_id]
        visited.add(folder_id)

        while todo_stack:
            entry_id = todo_stack.pop()

            entry = self.api_client.get_metadata(entry_id)

            if entry.is_file and entry.is_public:
                result.add(entry.id)
                continue

            if not entry.is_public:
                continue

            for next_entry_id in entry.children:
                if next_entry_id not in visited:
                    todo_stack.append(next_entry_id)
                    visited.add(next_entry_id)

        return list(result)

