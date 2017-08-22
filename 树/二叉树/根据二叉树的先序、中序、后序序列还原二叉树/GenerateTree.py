import types
import threading

class NodeFactory:
    map = {}
    lock = threading.Lock()

    @classmethod
    def factory(cls, element):
        with cls.lock:
            if not element in cls.map:
                cls.map[element] = Node(element)
            return cls.map[element]

class Node(object):
    def __init__(self, element, left=None, right=None):
        self._element = element
        self._left = left
        self._right = right

    @property
    def element(self):
        return self._element

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def set_left(self, left):
        if isinstance(left, (types.NoneType, Node)):
            self._left = left
        return self

    def set_right(self, right):
        if isinstance(right, (types.NoneType, Node)):
            self._right = right
        return self

    def postorder_traverse(self):
        nodes = []
        if self.left:
            nodes.extend(self.left.postorder_traverse())
        if self.right:
            nodes.extend(self.right.postorder_traverse())
        nodes.append(self.element)
        return nodes

    def inorder_traverse(self):
        nodes = []
        if self.left:
            nodes.extend(self.left.inorder_traverse())
        nodes.append(self.element)
        if self.right:
            nodes.extend(self.right.inorder_traverse())
        return nodes

    def preorder_traverse(self):
        nodes = [self.element]
        if self.left:
            nodes.extend(self.left.preorder_traverse())
        if self.right:
            nodes.extend(self.right.preorder_traverse())
        return nodes
    
    @staticmethod
    def find_pos(sequence, element):
        for ind, one_element in enumerate(sequence):
            if one_element == element:
                return ind
        return -1

    @classmethod
    def generate_tree(cls, preorder, inorder, postorder):
        if len(preorder) == 0 or \
            len(preorder) != len(inorder) or \
            len(inorder) != len(postorder) or \
            len(preorder) != len(postorder):
            raise RuntimeError("invalid input")
        if len(preorder) == 1:
            return NodeFactory.factory(preorder[0])

        left_preorder, left_inorder, left_postorder = \
            [], [], []
        right_preorder, right_inorder, right_postorder = \
            [], [], []
        root = NodeFactory.factory(preorder[0])
        if preorder[0] == inorder[0]:
            root.set_left(None)
            right_preorder = preorder[1:]
            right_inorder = inorder[1:]
            right_postorder = postorder[:len(postorder)-1]
        else:
            root.set_left(NodeFactory.factory(
                preorder[1]))

        if preorder[0] == inorder[-1]:
            root.set_right(None)
            left_preorder = preorder[1:]
            left_inorder = inorder[:len(inorder)-1]
            left_postorder = postorder[:len(postorder)-1]
        else:
            root.set_right(NodeFactory.factory(
                postorder[-2]))

        if root.left and root.right:
            pos = cls.find_pos(preorder, postorder[-2]) 
            left_preorder = preorder[1:pos]
            right_preorder = preorder[pos:]

            pos = cls.find_pos(inorder, preorder[0])
            left_inorder = inorder[:pos]
            right_inorder = inorder[pos+1:]

            pos = cls.find_pos(postorder, preorder[1])
            left_postorder = postorder[:pos+1]
            right_postorder = postorder[pos+1:len(postorder)-1]

        if left_preorder:
            cls.generate_tree(left_preorder,
                left_inorder, left_postorder)
        if right_preorder:
            cls.generate_tree(right_preorder,
                right_inorder, right_postorder)
        return root

if __name__ == "__main__":
    root = Node(100)
    root.set_left(Node(200)).set_right(Node(300))
    root.left.set_left(Node(400))
    root.right.set_left(Node(500)).set_right(Node(600))
    root.right.left.set_right(700)
    root.right.right.set_left(800)

    preorder = root.preorder_traverse()
    inorder = root.inorder_traverse()
    postorder = root.postorder_traverse()
    print preorder, inorder, postorder
    print Node.generate_tree(preorder, inorder, postorder).preorder_traverse() == preorder

