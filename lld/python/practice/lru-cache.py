class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self.capacity = capacity
        self.cache = {}
        self.head = Node(None, None)  # Dummy head node
        self.tail = Node(None, None)  # Dummy tail node
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
        return None

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                removed_node = self._remove_tail()
                del self.cache[removed_node.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

    def _add_to_head(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self):
        node = self.tail.prev
        self._remove_node(node)
        return node


if __name__ == "__main__":
    # Demonstration with test cases
    cache = LRUCache(3)

    cache.put(1, "Value 1")
    cache.put(2, "Value 2")
    cache.put(3, "Value 3")

    print(cache.get(1))  # Output: Value 1 (Moves 1 to front)
    print(cache.get(2))  # Output: Value 2 (Moves 2 to front)

    cache.put(4, "Value 4")  # Evicts 3 (least recently used)

    print(cache.get(3))  # Output: None (Evicted)
    print(cache.get(4))  # Output: Value 4

    cache.put(2, "Updated Value 2")  # Updates existing value

    print(cache.get(1))  # Output: Value 1 (Still exists)
    print(cache.get(2))  # Output: Updated Value 2 (Now at front)