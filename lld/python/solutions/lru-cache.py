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
        self.head = Node(None, None)
        self.tail = Node(None, None)
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
    cache = LRUCache(3)
    
    cache.put(1, '1')
    cache.put(2, '2')
    cache.put(3, '3')
    
    print(cache.get(1))
    print(cache.get(2))
    
    cache.put(4, '4')
    
    print(cache.get(3))
    print(cache.get(4))
    
    cache.put(2, '23')
    
    print(cache.get(1))
    print(cache.get(2))