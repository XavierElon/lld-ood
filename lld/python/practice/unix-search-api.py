from abc import ABC, abstractmethod
from collections import deque

class IEntry(ABC):
    """Interface representing a file system entry (file or directory)."""

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


class Entry(IEntry):
    """
    Abstract base class for File and Directory.
    Holds a 'name' property and implements get_name/set_name.
    """

    def __init__(self):
        self.name = None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name


class File(Entry):
    """Represents a file with content (as bytes)."""

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
    """Represents a directory that can hold other files or directories."""

    def __init__(self):
        super().__init__()
        self.entries = []  # List of File or Directory objects

    def add_entry(self, entry: Entry):
        self.entries.append(entry)

    def get_size(self) -> int:
        return sum(entry.get_size() for entry in self.entries)

    def is_directory(self) -> bool:
        return True


class SearchParams:
    """
    Holds various filter parameters:
    - extension: restrict files by extension
    - min_size: restrict files by minimum size
    - max_size: restrict files by maximum size
    - name: restrict files by exact name
    """
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
    """
    Aggregates multiple filters and checks if a file satisfies *all* of them.
    """

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
    """
    Searches files in a directory (and subdirectories) using a queue (BFS)
    and checks each file against the aggregated FileFilter.
    """

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
                    # entry is a File
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
