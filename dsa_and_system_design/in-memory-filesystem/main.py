from typing import List, Dict, Tuple

class Entity:
    def __init__(self, name: str, is_file: bool = False, content: str = ""):
        self.name = name
        self.children: Dict[str, 'Entity'] = {}
        self.is_file = is_file
        self.content = content

    def has_child(self, name: str) -> bool:
        return name in self.children
    
    def get_child(self, name: str) -> 'Entity':
        return self.children[name]
    
    def add_child(self, name: str):
        self.children[name] = Entity(name)

    def get_children(self) -> List['Entity']:
        return self.children.values()

class FileSystem:
    def __init__(self):
        self.root = Entity("/")
    
    def mkdir(self, path: str):
        parts = [p for p in path.split("/") if p]
        current = self.root
        for part in parts:
            if not current.has_child(part):
                current.add_child(part)
            
            current = current.get_child(part)

    def add_content_to_file(self, path: str, content: str):
        parts = [p for p in path.split("/") if p]
        file_name = parts[len(parts) - 1]
        current = self.root
        for index in range(len(parts) - 1):
            part = parts[index]
            if not current.has_child(part):
                current.add_child(part)
            
            current = current.get_child(part)

        # File exists
        if current.has_child(file_name):
            current.get_child(file_name).content += content
            return
        
        # File does not exists
        current.add_child(file_name)
        current.get_child(file_name).is_file = True
        current.get_child(file_name).content = content

    def ls(self, path: str) -> List[str]:
        parts = [p for p in path.split("/") if p]
        current = self.root
        
        for part in parts:
            if not current.has_child(part):
                return []
            
            current = current.get_child(part)

        if current.is_file:
            return [current.name]
        
        return sorted(current.children.keys())

    def read_content_from_file(self, path: str) -> str:
        parts = [p for p in path.split("/") if p] 
        current = self.root
        
        for index in range(len(parts)):
            part = parts[index]
            if not current.has_child(part):
                return ""
            
            current = current.get_child(part)

        return "" if not current.is_file else current.content
    

def main():
    file_system = FileSystem()
    file_system.mkdir("/a/b/c")
    file_system.add_content_to_file("/a/b/file.txt", "hello")
    print(file_system.ls("/a/b"))
    print(file_system.read_content_from_file("/a/b/file.txt"))
    file_system.add_content_to_file("/a/b/file.txt", "world")
    print(file_system.read_content_from_file("/a/b/file.txt"))
    print(file_system.read_content_from_file("/a/b/foo.txt"))

if __name__ == '__main__':
    main()