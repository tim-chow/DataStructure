#coding: utf8

class BaseFrame(object):
    @staticmethod
    def run(first_frame):
        stack = [first_frame]
        address, value = 0, None
        while stack:
            next_frame = stack[-1].execute(address, value)
            if not next_frame:
                frame = stack.pop(-1)
                address = frame.get_return_address()
                value = frame.get_result()
            else:
                stack.append(next_frame)
                address, value = 0, None
        return value

class TreeFrame(BaseFrame):
    def __init__(self, return_address, root):
        self._return_address = return_address
        self._root = root
        self._nodes = []

    def get_return_address(self):
        return self._return_address

    def get_result(self):
        return self._nodes

def preorder_traverse1(root):
    if not root:
        return []
    nodes = [root.element]
    nodes.extend(preorder_traverse2(root.left))
    nodes.extend(preorder_traverse2(root.right))
    return nodes

def preorder_traverse2(root):
    class Frame(TreeFrame):
        def __init__(self, return_address, root):
            super(self.__class__, self).__init__(return_address, root)

        def execute(self, address, value):
            if not self._root:
                return

            if address == 0:
                self._nodes.append(self._root.element)
                return Frame(1, self._root.left)
            if address == 1:
                self._nodes.extend(value)
                return Frame(2, self._root.right)
            if address == 2:
                self._nodes.extend(value)
            return
    return Frame.run(Frame(-1, root))

def postorder_traverse1(root):
    if not root:
        return []
    nodes = []
    nodes.extend(postorder_traverse1(root.left))
    nodes.extend(postorder_traverse1(root.right))
    nodes.append(root.element)
    return nodes

def postorder_traverse2(root):
    class Frame(TreeFrame):
        def __init__(self, return_address, root):
            super(self.__class__, self).__init__(return_address, root)

        def execute(self, address, value):
            if not self._root:
                return
            if address == 0:
                return Frame(1, self._root.left)
            if address == 1:
                self._nodes.extend(value)
                return Frame(2, self._root.right)
            if address == 2:
                self._nodes.extend(value)
                self._nodes.append(self._root.element)
            return
    return Frame.run(Frame(-1, root))

def inorder_traverse1(root):
    if not root:
        return []
    nodes = []
    nodes.extend(inorder_traverse1(root.left))
    nodes.append(root.element)
    nodes.extend(inorder_traverse1(root.right))
    return nodes

def inorder_traverse2(root):
    class Frame(TreeFrame):
        def __init__(self, *a, **kw):
            super(self.__class__, self).__init__(*a, **kw)

        def execute(self, address, value):
            if not self._root:
                return 
            if address == 0:
                return Frame(1, self._root.left)
            if address == 1:
                self._nodes.extend(value)
                self._nodes.append(self._root.element)
                return Frame(2, self._root.right)
            if address == 2:
                self._nodes.extend(value)
            return
    return Frame.run(Frame(-1, root))

class BinaryTreeNode(object):
    def __init__(self, element, right=None, left=None):
        self._element = element
        self._right = right
        self._left = left

    @property
    def element(self):
        return self._element

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        self._right = right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._left = left

    def preorder_traverse(self):
        nodes = []
        nodes.append(self.element)
        if self.left:
            nodes.extend(self.left.preorder_traverse())
        if self.right:
            nodes.extend(self.right.preorder_traverse())
        return nodes


    def inorder_traverse(self):
        nodes = []
        if self.left:
            nodes.extend(self.left.inorder_traverse())
        nodes.append(self.element)
        if self.right:
            nodes.extend(self.right.inorder_traverse())
        return nodes

    def postorder_traverse(self):
        nodes = []
        if self.left:
            nodes.extend(self.left.postorder_traverse())
        if self.right:
            nodes.extend(self.right.postorder_traverse())
        nodes.append(self.element)
        return nodes

    @staticmethod
    def BFS(root):
        queue = [root]
        ind = 0
        while ind < len(queue):
            node = queue[ind]
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
            ind = ind + 1
        return queue

    def __str__(self):
        return str(self._element)
    __repr__ = __str__

def test():
    root = BinaryTreeNode(100)
    root.left = BinaryTreeNode(200)
    root.right = BinaryTreeNode(300)

    root.left.left = BinaryTreeNode(400)
    root.left.right = None
    root.right.left = BinaryTreeNode(500)
    root.right.right = BinaryTreeNode(600)

    print "preorder..."
    print root.preorder_traverse()
    print preorder_traverse1(root)
    print preorder_traverse2(root)
    print "\n"
    print "inorder..."
    print root.inorder_traverse()
    print inorder_traverse1(root)
    print inorder_traverse2(root)
    print "\n"
    print "postorder..."
    print root.postorder_traverse()
    print postorder_traverse1(root)
    print postorder_traverse2(root)
    print "\n"
    print "BFS..."
    print BinaryTreeNode.BFS(root)

if __name__ == "__main__":
    test()

