# coding: utf8


class Node(object):
    """
    先序和中序线索二叉树的节点
    """
    def __init__(self,
                 keyword,
                 left=None,
                 right=None,
                 ltag=False,
                 rtag=False):
        self.keyword = keyword
        self.left = left
        self.right = right
        self.ltag = ltag
        self.rtag = rtag

    def __str__(self):
        return "%s{keyword=%s, left=%s, right=%s, ltag=%s, rtag=%s}" % (
            self.__class__.__name__,
            self.keyword,
            self.left and self.left.keyword,
            self.right and self.right.keyword,
            self.ltag,
            self.rtag
        )


class PostorderThreadingNode(Node):
    """
    后序线索二叉树的节点
    """
    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        # 增加指向父节点的指针
        self.parent = None

########## 中序线索二叉树的构建以及遍历 ##########


def find_inorder_first_node(p):
    """
    找到子树 p 的中序序列的第一个节点
    """
    if p is None:
        return None

    # p 的中序序列的第一个节点是 p 的最左孩子
    node = p
    while not node.ltag and node.left is not None:
        node = node.left
    return node


def find_inorder_next_node(p):
    """
    找到 p 在中序序列中的下一个节点
    """
    if p is None:
        return None

    if p.rtag:
        return p.right

    # 返回 p 的右子树的中序序列的第一个节点
    return find_inorder_first_node(p.right)


def inorder_traverse(p):
    """
    中序遍历
    """
    keywords = []
    node = find_inorder_first_node(p)
    while node is not None:
        keywords.append(node.keyword)
        node = find_inorder_next_node(node)

    return keywords


def inorder_threading(p):
    """
    构建中序线索二叉树
    """
    visited = [None]

    def _inorder_threading(p):
        if p is None:
            return

        _inorder_threading(p.left)

        if p.left is None:
            p.left = visited[0]
            p.ltag = True
        if visited[0] is not None and visited[0].right is None:
            visited[0].right = p
            visited[0].rtag = True
        visited[0] = p

        _inorder_threading(p.right)

    _inorder_threading(p)

########## end 中序线索二叉树 ##########

########## 后序线索二叉树的构建和遍历 ##########


def postorder_threading(p):
    """
    构建后序线索二叉树
    """
    visited = [None]

    def _postorder_threading(p):
        if p is None:
            return

        _postorder_threading(p.left)

        _postorder_threading(p.right)

        if p.left is None:
            p.left = visited[0]
            p.ltag = True
        if visited[0] is not None and visited[0].right is None:
            visited[0].right = p
            visited[0].rtag = True
        visited[0] = p

    _postorder_threading(p)


def find_postorder_first_node(p):
    """
    找到子树 p 的后序序列的第一个节点
    """
    node = p
    while node is not None:
        # 先找到最左节点
        while not node.ltag and node.left is not None:
            node = node.left
        # 如果最左节点没有右孩子，则它就是第一个节点
        if node.rtag or node.right is None:
            break
        # 否则，去节点的右子树上去找
        node = node.right
    return node


def find_postorder_next_node(p, root):
    """
    找到 p 在后序序列中的下一个节点
    """
    # 如果 p 是根节点，那么返回 None
    if p is None or p is root:
        return None

    # 返回后继
    if p.rtag:
        return p.right

    parent = p.parent
    # 如果 p 是其父的右孩子，那么其父即为下一个节点
    if p is parent.right:
        return parent
    # 如果 p 是其父的左孩子，但是其父没有右孩子，那么其父即为下一个节点
    if p is parent.left and (parent.rtag or parent.right is None):
        return parent
    # 否则，返回其父的右孩子的后序序列的第一个节点
    else:
        return find_postorder_first_node(parent.right)


def postorder_traverse(p):
    """
    后序遍历
    """
    node = find_postorder_first_node(p)
    keywords = []
    while node is not None:
        keywords.append(node.keyword)
        node = find_postorder_next_node(node, p)
    return keywords

########## end 后序线索二叉树 ##########

########## 先序线索二叉树的构建和遍历 ##########


def find_preorder_first_node(p):
    if p is None:
        return None
    return p


def find_preorder_next_node(p):
    if p is None:
        return None

    if not p.ltag and p.left is not None:
        return p.left
    return p.right


def preorder_threading(p):
    visited = [None]

    def _preorder_threading(p):
        if p is None:
            return

        if p.left is None:
            p.left = visited[0]
            p.ltag = True
        if visited[0] is not None and visited[0].right is None:
            visited[0].right = p
            visited[0].rtag = True
        visited[0] = p

        _preorder_threading(p.left if not p.ltag else None)

        _preorder_threading(p.right if not p.rtag else None)

    _preorder_threading(p)


def preorder_traverse(p):
    node = find_preorder_first_node(p)
    keywords = []
    while node is not None:
        keywords.append(node.keyword)
        node = find_preorder_next_node(node)
    return keywords

########## end 先序线索二叉树 ##########


if __name__ == "__main__":
    import unittest

    class ThreadingBinaryTreeTest(unittest.TestCase):
        def setUp(self):
            nodes = [PostorderThreadingNode(ind) for ind in range(11)]
            nodes[0].left = nodes[1]
            nodes[0].right = nodes[2]

            nodes[1].parent = nodes[0]
            nodes[1].left = nodes[3]

            nodes[2].parent = nodes[0]
            nodes[2].left = nodes[4]
            nodes[2].right = nodes[5]

            nodes[3].parent = nodes[1]
            nodes[3].left = nodes[8]
            nodes[3].right = nodes[9]

            nodes[4].parent = nodes[2]
            nodes[4].right = nodes[7]

            nodes[5].parent = nodes[2]
            nodes[5].left = nodes[6]

            nodes[6].parent = nodes[5]

            nodes[7].parent = nodes[4]

            nodes[8].parent = nodes[3]
            nodes[8].right = nodes[10]

            nodes[9].parent = nodes[3]

            nodes[10].parent = nodes[8]

            self.root = nodes[0]

        def testInorderThreading(self):
            inorder_threading(self.root)
            self.assertEqual(inorder_traverse(self.root),
                             [8, 10, 3, 9, 1, 0, 4, 7, 2, 6, 5])

        def testPostorderThreading(self):
            postorder_threading(self.root)
            self.assertEqual(postorder_traverse(self.root),
                             [10, 8, 9, 3, 1, 7, 4, 6, 5, 2, 0])

        def testPreorderThreading(self):
            preorder_threading(self.root)
            self.assertEqual(preorder_traverse(self.root),
                             [0, 1, 3, 8, 10, 9, 2, 4, 7, 5, 6])

    unittest.main()
