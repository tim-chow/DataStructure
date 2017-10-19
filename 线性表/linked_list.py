class LinkedList(object):
    class Node(object):
        def __init__(self, element, next=None):
            self._element = element
            self._next = next

        @property
        def element(self):
            return self._element

        @element.setter
        def element(self, element):
            self._element = element

        @property
        def next(self):
            return self._next

        @next.setter
        def next(self, next):
            self._next = next

    def __init__(self):
        self._head = self.Node(None, None)
        self._size = 0

    def add(self, element):
        node = self._head
        while node.next:
            node = node.next
        node.next = self.Node(element)
        self._size = self._size + 1

    def insert(self, index, element):
        if self._size == 0:
            self._head.next = self.Node(element)
            self._size = self._size + 1
            return

        if index < 0:
            index = 0
        if index >= self._size:
            self.add(element)
            return

        node = self._head
        for _ in range(index + 1):
            node = node.next
        new_node = self.Node(node.element)
        new_node.next = node.next
        node.element = element
        node.next = new_node
        self._size = self._size + 1

    def delete(self, index):
        if self._size == 0 or index < 0 or index >= self._size:
            return

        prev_node = self._head
        for i in range(index):
            prev_node = prev_node.next

        deleted_node = prev_node.next
        prev_node.next = deleted_node.next
        self._size = self._size - 1

    def __str__(self):
        node = self._head.next
        result = []
        while node:
            result.append(node.element)
            node = node.next
        return ", ".join(map(str, result))

    def find(self, element):
        node = self._head
        for index in range(self._size):
            node = node.next
            if node.element == element:
                return index
        return -1

if __name__ == "__main__":
    list = LinkedList()
    list.insert(-1, 1)
    list.insert(1, 2)
    list.insert(100, 4)
    list.insert(2, 3)
    list.insert(1, 1.5)
    list.insert(0, 0.5)
    list.insert(5, 3.5)
    list.insert(6, 3.75)
    list.insert(8, 5)
    print list.find(3.75)

