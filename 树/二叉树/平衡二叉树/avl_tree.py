# coding: utf8


class Node(object):
    """
    AVL 树的节点，使用三叉链表表示法
    """
    def __init__(self, keyword, parent=None, balance_factor=0):
        self.keyword = keyword
        self.parent = parent
        self.left = None
        self.right = None
        self.balance_factor = balance_factor


class AVLTree(object):
    """
    AVL 树实现
    """
    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    def insert_keyword(self, keyword):
        """
        向 AVL 树中插入关键字
        """
        if self._root is None:
            self._root = Node(keyword)
            return

        node = self._root
        while True:
            if keyword < node.keyword:
                if node.left is None:
                    node.left = Node(keyword, node)
                    self.rotate(node.left)
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(keyword, node)
                    self.rotate(node.right)
                    break
                node = node.right

    @classmethod
    def find_unbalance_node(cls, node):
        """"寻找第一个失衡点"""
        left = node is node.parent.left
        node = node.parent
        while node is not None:
            if left:
                if node.balance_factor == -1:
                    node.balance_factor = 0
                    return None
                if node.balance_factor == 1:
                    node.balance_factor = 2
                    return node
                node.balance_factor = 1
            else:
                if node.balance_factor == 1:
                    node.balance_factor = 0
                    return None
                if node.balance_factor == -1:
                    node.balance_factor = -2
                    return node
                node.balance_factor = -1
            if node.parent is not None:
                left = node is node.parent.left
            node = node.parent

    def rotate_ll(self, node):
        parent = node.parent
        A = node
        B = node.left
        BR = B.right

        B.parent = parent
        if parent is None:
            self._root = B
        else:
            if node is parent.left:
                parent.left = B
            else:
                parent.right = B
        B.right = A

        A.parent = B
        A.left = BR
        if BR:
            BR.parent = A

        A.balance_factor = 0
        B.balance_factor = 0

    def rotate_lr(self, node):
        parent = node.parent
        A = node
        B = node.left
        C = B.right
        CL = C.left
        CR = C.right

        C.parent = parent
        if parent is None:
            self._root = C
        else:
            if node is parent.left:
                parent.left = C
            else:
                parent.right = C
        C.left = B
        C.right = A

        B.parent = C
        B.right = CL
        if CL:
            CL.parent = B

        A.parent = C
        A.left = CR
        if CR:
            CR.parent = A

        if C.balance_factor == -1:
            A.balance_factor = 0
            B.balance_factor = 1
            C.balance_factor = 0
        elif C.balance_factor == 0:
            A.balance_factor = 0
            B.balance_factor = 0
            C.balance_factor = 0
        else:
            A.balance_factor = -1
            B.balance_factor = 0
            C.balance_factor = 0

    def rotate_rr(self, node):
        parent = node.parent
        A = node
        B = A.right
        BL = B.left

        B.parent = parent
        if parent is None:
            self._root = B
        else:
            if node is parent.left:
                parent.left = B
            else:
                parent.right = B
        B.left = A

        A.parent = B
        A.right = BL
        if BL:
            BL.parent = A

        A.balance_factor = 0
        B.balance_factor = 0

    def rotate_rl(self, node):
        parent = node.parent
        A = node
        B = A.right
        C = B.left
        CL = C.left
        CR = C.right

        C.parent = parent
        if parent is None:
            self._root = C
        else:
            if node is parent.left:
                parent.left = C
            else:
                parent.right = C
        C.left = A
        C.right = B

        A.parent = C
        A.right = CL
        if CL:
            CL.parent = A

        B.parent = C
        B.left = CR
        if CR:
            CR.parent = B

        if C.balance_factor == -1:
            A.balance_factor = 1
            B.balance_factor = 0
            C.balance_factor = 0
        elif C.balance_factor == 0:
            A.balance_factor = 0
            B.balance_factor = 0
            C.balance_factor = 0
        else:
            A.balance_factor = 0
            B.balance_factor = -1
            C.balance_factor = 0

    def rotate(self, node):
        unbalance_node = self.find_unbalance_node(node)
        if unbalance_node is None:
            return
        left = unbalance_node.left
        right = unbalance_node.right
        if unbalance_node.balance_factor > 0:
            if left.balance_factor > 0:
                self.rotate_ll(unbalance_node)
            else:
                self.rotate_lr(unbalance_node)
        else:
            if right.balance_factor < 0:
                self.rotate_rr(unbalance_node)
            else:
                self.rotate_rl(unbalance_node)

    @classmethod
    def get_height(cls, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        return max(cls.get_height(node.left), cls.get_height(node.right)) + 1

    def delete_keyword(self, keyword):
        """
        从 AVL 树中删除节点
        """
        # 找到待删除节点
        node = self._root
        while node is not None:
            if node.keyword == keyword:
                break
            if node.keyword > keyword:
                node = node.left
            else:
                node = node.right
        else:
            return

        # 如果待删除节点是根节点，并且其左子树或右子树为空，则将其非空子树接到根节点即可
        if node is self._root and (node.left is None or node.right is None):
            self._root = node.left or node.right
            return

        # 否则，找到左子树的最右节点，并使用其关键字替代待删除节点的关键字，然后将该节点删掉
        real_deleted_node = node
        if node.left is not None:
            real_deleted_node = node.left
            while real_deleted_node.right is not None:
                real_deleted_node = real_deleted_node.right
        node.keyword = real_deleted_node.keyword
        self.delete_and_rotate(real_deleted_node)

    def delete_and_rotate(self, real_deleted_node):
        # 将真正删除的节点的非空子树接到其父节点
        parent = real_deleted_node.parent
        subtree = real_deleted_node.left or real_deleted_node.right
        if real_deleted_node is parent.left:
            parent.left = subtree
            left = True
        else:
            parent.right = subtree
            left = False
        if subtree is not None:
            subtree.parent = parent

        # 从真正删除的节点的父节点开始，向根节点方向前进，调整所经过的节点的平衡因子
        node = parent
        while node is not None:
            # 旋转之后 node 的父节点会发生改变，所以提前保存其父节点
            next_node = node.parent
            next_left = False
            if next_node is not None:
                next_left = node is next_node.left

            if left:
                if node.balance_factor == 1:
                    node.balance_factor = 0
                elif node.balance_factor == 0:
                    node.balance_factor = -1
                    break
                else:
                    node.balance_factor = -2
                    if node.right.balance_factor > 0:
                        self.rotate_rl_when_delete(node)
                    elif node.right.balance_factor == 0:
                        # 旋转之后子树高度不变，无需继续向上调整
                        self.rotate_rr_when_delete(node)
                        break
                    else:
                        self.rotate_rr_when_delete(node)
            else:
                if node.balance_factor == 1:
                    node.balance_factor = 2
                    if node.left.balance_factor < 0:
                        self.rotate_lr_when_delete(node)
                    elif node.left.balance_factor == 0:
                        self.rotate_ll_when_delete(node)
                        break
                    else:
                        self.rotate_ll_when_delete(node)
                elif node.balance_factor == 0:
                    node.balance_factor = 1
                    break
                else:
                    node.balance_factor = 0

            node = next_node
            left = next_left

    def rotate_ll_when_delete(self, node):
        parent = node.parent
        A = node
        B = A.left
        BR = B.right

        B.parent = parent
        if parent is None:
            self._root = B
        else:
            if node is parent.left:
                parent.left = B
            else:
                parent.right = B
        B.right = A

        A.parent = B
        A.left = BR
        if BR:
            BR.parent = A

        if B.balance_factor == 0:
            A.balance_factor = 1
            B.balance_factor = -1
        else:
            A.balance_factor = 0
            B.balance_factor = 0

    def rotate_lr_when_delete(self, node):
        parent = node.parent
        A = node
        B = A.left
        C = B.right
        CL = C.left
        CR = C.right

        C.parent = parent
        if parent is None:
            self._root = C
        else:
            if node is parent.left:
                parent.left = C
            else:
                parent.right = C
        C.left = B
        C.right = A

        B.parent = C
        B.right = CL
        if CL:
            CL.parent = B

        A.parent = C
        A.left = CR
        if CR:
            CR.parent = A

        if C.balance_factor == -1:
            A.balance_factor = 0
            B.balance_factor = 1
            C.balance_factor = 0
        elif C.balance_factor == 0:
            A.balance_factor = 0
            B.balance_factor = 0
            C.balance_factor = 0
        else:
            A.balance_factor = -1
            B.balance_factor = 0
            C.balance_factor = 0

    def rotate_rl_when_delete(self, node):
        parent = node.parent
        A = node
        B = A.right
        C = B.left
        CL = C.left
        CR = C.right

        C.parent = parent
        if parent is None:
            self._root = C
        else:
            if node is parent.left:
                parent.left = C
            else:
                parent.right = C
        C.left = A
        C.right = B

        A.parent = C
        A.right = CL
        if CL:
            CL.parent = A

        B.parent = C
        B.left = CR
        if CR:
            CR.parent = B

        if C.balance_factor == 0:
            A.balance_factor = 0
            B.balance_factor = 0
            C.balance_factor = 0
        elif C.balance_factor == 1:
            A.balance_factor = 0
            B.balance_factor = -1
            C.balance_factor = 0
        else:
            A.balance_factor = 1
            B.balance_factor = 0
            C.balance_factor = 0

    def rotate_rr_when_delete(self, node):
        parent = node.parent
        A = node
        B = node.right
        BL = B.left

        B.parent = parent
        if parent is None:
            self._root = B
        else:
            if node is parent.left:
                parent.left = B
            else:
                parent.right = B
        B.left = A

        A.parent = B
        A.right = BL
        if BL:
            BL.parent = A

        if B.balance_factor == 0:
            A.balance_factor = -1
            B.balance_factor = 1
        else:
            A.balance_factor = 0
            B.balance_factor = 0

    @classmethod
    def is_valid_avl_tree(cls, root):
        if root is None:
            return 0
        if root.balance_factor not in [-1, 0, 1]:
            return 1
        if root.balance_factor != (
                cls.get_height(root.left) -
                cls.get_height(root.right)):
            return 2

        if root.left is not None and root.left.keyword > root.keyword:
            return 3
        if root.right is not None and root.right.keyword < root.keyword:
            return 4

        left_status = cls.is_valid_avl_tree(root.left)
        if left_status != 0:
            return left_status
        right_status = cls.is_valid_avl_tree(root.right)
        if right_status != 0:
            return right_status
        return 0


if __name__ == "__main__":
    import random

    array = list(range(100))
    random.shuffle(array)
    print(array)
    tree = AVLTree()
    for keyword in array:
        tree.insert_keyword(keyword)
        status = AVLTree.is_valid_avl_tree(tree.root)
        assert status == 0, "tree is not AVL"

    random.shuffle(array)
    for keyword in array:
        tree.delete_keyword(keyword)
        status = AVLTree.is_valid_avl_tree(tree.root)
        assert status == 0, "tree is not AVL"
