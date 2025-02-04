# Composite Pattern (for File/Directory structure)
# We treat both File and Directory as Entry objects (IEntry interface/Entry base class).
# A Directory can contain multiple Entry objects (which themselves can be either File or Directory). This is a classic Composite structure: “part-whole” hierarchies where clients treat individual objects (files) and compositions of objects (directories) uniformly.

# Strategy (and Filter Aggregation)
# Each filter (NameFilter, MinSizeFilter, MaxSizeFilter, ExtensionFilter) implements the same interface (IFilter), defining a single method is_valid.
# This is akin to the Strategy pattern: each filter is an interchangeable “strategy” for validating a file.
# The FileFilter class aggregates these strategies and applies them in sequence, effectively creating a chain of checks (“Chain of Responsibility”-like behavior). If any filter fails, the file is excluded.

# Breadth-First Search (BFS) for Traversing Directories
# The FileSearcher uses a queue (deque) to perform a BFS over directories, enqueuing subdirectories and collecting valid files.
# This detail is more of an algorithmic choice than a design pattern, but it cleanly handles nested directories without a deep recursion.
# Together, these patterns make the design flexible, modular, and easy to extend. You can add more filters (or different search methods) without disrupting the existing code structure.

from abc import ABC, abstractmethod
from collections import deque

# Interface
class IEntry(ABC):
    @abstractmethod
    def get_name(self):
        pass
    
    @abstractmethod
    def set_name(self, name):
        pass

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def is_directory(self):
        pass

# Abstract Base Class
class Entry(IEntry):
    def __init__(self):
        self.name = None
    
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        
class File(Entry):
    def __init__(self):
        super().__init__()
        self.content = b""
        
    def set_content(self, content: bytes):
        self.content = content
    
    def get_content(self) -> bytes:
        return self.content
    
    def get_size(self) -> int:
        return len(self.content)
    
    def get_extension(self) -> str:
        if "." in self.name:
            return self.name[self.name.rfind(".") + 1:]
        return ""

    def is_directory(self) -> bool:
        return False

    def __str__(self):
        return f"File{{name='{self.name}'}}"
    

class Directory(Entry):
    def __init__(self):
        super().__init__()
        self.entries = []
        
    def add_entry(self, entry: Entry):
        self.entries.append(entry)
        
    def get_size(self) -> int:
        return sum(entry.get_size() for entry in self.entries)
    
    def is_directory(self) -> bool:
        return True

class SearchParams:
    def __init__(self):
        self.extension = None
        self.min_size = None
        self.max_size = None
        self.name = None
        
# -- Filters (Strategy/Chain-of-Responsibility-like) -----------------

class IFilter(ABC):
    """Interface for a file filter (strategy)."""

    @abstractmethod
    def is_valid(self, params: SearchParams, file: File) -> bool:
        pass


class NameFilter(IFilter):
    """Filter by exact filename."""

    def is_valid(self, params: SearchParams, file: File) -> bool:
        if params.name is None:
            return True
        return file.get_name() == params.name


class MinSizeFilter(IFilter):
    """Filter by minimum file size."""

    def is_valid(self, params: SearchParams, file: File) -> bool:
        if params.min_size is None:
            return True
        return file.get_size() >= params.min_size


class MaxSizeFilter(IFilter):
    """Filter by maximum file size."""

    def is_valid(self, params: SearchParams, file: File) -> bool:
        if params.max_size is None:
            return True
        return file.get_size() <= params.max_size


class ExtensionFilter(IFilter):
    """Filter by file extension."""

    def is_valid(self, params: SearchParams, file: File) -> bool:
        if params.extension is None:
            return True
        return file.get_extension() == params.extension
    
class FileFilter:
    def __init__(self):
        self.filters = [
            NameFilter(),
            MaxSizeFilter(),
            MinSizeFilter(),
            ExtensionFilter()
        ]
        
    def is_valid(self, params: SearchParams, file: File) -> bool:
        for f in self.filters:
            if not f.is_valid(params, file):
                return False
        return True

class FileSearcher:
    def __init__(self):
        self.file_filter = FileFilter()
        
    def search(self, directory: Directory, params: SearchParams):
        found_files = []
        queue = deque([directory])
        
        while queue:
            current_dir = queue.popleft()
            
            for entry in current_dir.entries:
                if entry.is_directory():
                    queue.append(entry)
                else:
                    if self.file_filter.is_valid(params, entry):
                        found_files.append(entry)
        return found_files
    
def main():
    # Create sample SearchParams
    params = SearchParams()
    params.extension = "xml"
    params.min_size = 2
    params.max_size = 100

    # Create File objects
    xml_file = File()
    xml_file.set_name("aaa.xml")
    xml_file.set_content(b"aaa.xml")

    txt_file = File()
    txt_file.set_name("bbb.txt")
    txt_file.set_content(b"bbb.txt")

    json_file = File()
    json_file.set_name("ccc.json")
    json_file.set_content(b"ccc.json")

    # Build directory hierarchy
    dir1 = Directory()
    dir1.set_name("dir1")
    dir1.add_entry(txt_file)
    dir1.add_entry(xml_file)

    dir0 = Directory()
    dir0.set_name("dir0")
    dir0.add_entry(json_file)
    dir0.add_entry(dir1)

    # Search
    searcher = FileSearcher()
    results = searcher.search(dir0, params)
    print("Search results:", results)


if __name__ == "__main__":
    main()