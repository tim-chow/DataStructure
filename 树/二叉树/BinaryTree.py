# coding: utf8


class BinaryTreeNode(object):
    def __init__(self, element, left=None, right=None):
        self.element = element
        self.left = left
        self.right = right

########## 下面是先序、中序、后序遍历的递归实现 ##########


def preorder_traverse(root):
    if root is None:
        return []

    nodes = [root.element]
    nodes.extend(preorder_traverse(root.left))
    nodes.extend(preorder_traverse(root.right))

    return nodes

def inorder_traverse(root):
    if root is None:
        return []

    nodes = []
    nodes.extend(inorder_traverse(root.left))
    nodes.append(root.element)
    nodes.extend(inorder_traverse(root.right))

    return nodes

def postorder_traverse(root):
    if root is None:
        return []

    nodes = []
    nodes.extend(postorder_traverse(root.left))
    nodes.extend(postorder_traverse(root.right))
    nodes.append(root.element)

    return nodes

########## 下面是先序、中序、后序遍历的非递归实现 ##########
########## 请参考：http://timd.cn/eliminate-recursive/ ##########

class Frame(object):
    def __init__(self, root, return_address=0):
        self.root = root
        self.return_address = return_address
        self.result = []

    def run(self):
        address = 0
        value = None
        stack = [self.__class__(self.root)]

        while stack:
            active_frame = stack[-1]
            next_frame = active_frame.execute(address, value)
            if next_frame is None:
                # 进入返回段
                address = active_frame.return_address
                value = active_frame.result
                stack.pop(-1)
                continue
            # 进入前进段
            stack.append(next_frame)
            address = 0
            value = None

        return value

    def execute(self, address, value):
        raise NotImplementedError("should be overridden")


class PreorderTraverseFrame(Frame):
    def execute(self, address, value):
        if self.root is None:
            return
        if address == 0:
            self.result.append(self.root.element)
            return PreorderTraverseFrame(self.root.left, 1)
        elif address == 1:
            self.result.extend(value)
            return PreorderTraverseFrame(self.root.right, 2)
        elif address == 2:
            self.result.extend(value)


class InorderTraverseFrame(Frame):
    def execute(self, address, value):
        if self.root is None:
            return
        if address == 0:
            return InorderTraverseFrame(self.root.left, 1)
        elif address == 1:
            self.result.extend(value)
            self.result.append(self.root.element)
            return InorderTraverseFrame(self.root.right, 2)
        elif address == 2:
            self.result.extend(value)
            return


class PostorderTraverseFrame(Frame):
    def execute(self, address, value):
        if self.root is None:
            return

        if address == 0:
            return PostorderTraverseFrame(self.root.left, 1)
        elif address == 1:
            self.result.extend(value)
            return PostorderTraverseFrame(self.root.right, 2)
        elif address == 2:
            self.result.extend(value)
            self.result.append(self.root.element)

########## 下面是广度优先遍历的非递归实现 ##########


def bfs(root):
    elements = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            continue
        elements.append(node.element)
        queue.append(node.left)
        queue.append(node.right)
    return elements

########## 下面是广度优先遍历的递归实现


def bfs_recursive(nodes):
    if isinstance(nodes, BinaryTreeNode):
        nodes = [nodes]

    # 先将本层的节点保存到结果列表，然后生成下层的节点列表
    elements = []
    next_nodes = []
    for node in nodes:
        if node is None:
            continue
        elements.append(node.element)
        next_nodes.append(node.left)
        next_nodes.append(node.right)
    # 如果没有下一层，则返回；否则，递归地遍历下一层
    if next_nodes:
        elements.extend(bfs_recursive(next_nodes))
    return elements


if __name__ == "__main__":
    import unittest

    class BinaryTreeTest(unittest.TestCase):
        def setUp(self):
            ######################
            #          0         #
            #       /    \       #
            #      1      2      #
            #      \    /  \     #
            #       3  4    5    #
            ######################
            nodes = [BinaryTreeNode(ind) for ind in range(6)]
            nodes[0].left = nodes[1]
            nodes[0].right = nodes[2]
            nodes[1].right = nodes[3]
            nodes[2].left = nodes[4]
            nodes[2].right = nodes[5]
            self.root = nodes[0]
            del nodes

        def testPreorderTraverse(self):
            result = [0, 1, 3, 2, 4, 5]
            self.assertEqual(preorder_traverse(self.root), result)
            self.assertEqual(PreorderTraverseFrame(self.root).run(), result)

        def testInorderTraverse(self):
            result = [1, 3, 0, 4, 2, 5]
            self.assertEqual(inorder_traverse(self.root), result)
            self.assertEqual(InorderTraverseFrame(self.root).run(), result)

        def testPostorderTraverse(self):
            result = [3, 1, 4, 5, 2, 0]
            self.assertEqual(postorder_traverse(self.root), result)
            self.assertEqual(PostorderTraverseFrame(self.root).run(), result)

        def testBFS(self):
            result = [0, 1, 2, 3, 4, 5]
            self.assertEqual(bfs(self.root), result)
            self.assertEqual(bfs_recursive(self.root), result)


    unittest.main()
