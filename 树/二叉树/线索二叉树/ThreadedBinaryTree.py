import threading

class Node(object):
    def __init__(self, element):
        self._lock = threading.Lock()
        self._inorder_threading_previous = None

        self._element = element
        self._left = None
        self._right = None
        self._ltag = False
        self._rtag = False

    def get_element(self):
        return self._element

    def get_left(self):
        if not self._ltag:
            return self._left
        return None

    def get_right(self):
        if not self._rtag:
            return self._right
        return None

    def get_previous(self):
        if self._ltag:
            return self._left
        return None

    def get_next(self):
        if self._rtag:
            return self._right
        return None

    def set_left(self, left):
        self._left = left
        self._ltag = False
        return self

    def set_right(self, right):
        self._right = right
        self._rtag = False
        return self

    def set_previous(self, previous):
        self._left = previous
        self._ltag = True
        return self

    def set_next(self, next):
        self._right = next
        self._rtag = True
        return self

    def inorder_threading(self):
        with self._lock:
            self._inorder_threading_previous = None
            self._inorder_threading(self)

    def _inorder_threading(self, root):
        if not root:
            return

        self._inorder_threading(root.get_left())
        
        if not root.get_left():
            root.set_previous(self._inorder_threading_previous)
        if self._inorder_threading_previous and \
            not self._inorder_threading_previous.get_right():
            self._inorder_threading_previous.set_next(root)
        self._inorder_threading_previous = root

        self._inorder_threading(root.get_right())

    def inorder_traverse1(self):
        if self.get_left():
            self.get_left().inorder_traverse1()
        print self
        if self.get_right():
            self.get_right().inorder_traverse1()

    def inorder_traverse2(self):
        p = self
        while p:
            while p.get_left():
                p = p.get_left()
            print p
            while p.get_next():
                p = p.get_next()
                print p
            p = p.get_right()

    def __str__(self):
        return str(self._element)

if __name__ == "__main__":
    root = Node(1)
    root.set_left(Node(2)).set_right(Node(3))
    root.get_left().set_left(Node(4)).set_right(Node(5))
    root.get_right().set_right(Node(7))

    root.inorder_traverse1()
    root.inorder_threading()
    root.inorder_traverse2()

