# coding: utf8

class Node(object):
    def __init__(self, keyword, parent=None, balance_factor=0):
        self.keyword = keyword
        self.parent = parent
        self.left = None
        self.right = None
        self.balance_factor = balance_factor

    def __str__(self):
        return "Node{keyword=%s, parent=%s, left=%s, right=%s, bf=%d}" % (
            self.keyword, self.parent and self.parent.keyword,
                self.left, self.right, self.balance_factor)

    __repr__ = __str__


class AVLTree(object):
    def __init__(self):
        self._root_node = None

    @property
    def root_node(self):
        return self._root_node

    def insert_keyword(self, keyword):
        if self._root_node == None:
            self._root_node = Node(keyword)
            return

        node = self._root_node
        while node != None:
            if keyword < node.keyword:
                if node.left == None:
                    node.left = Node(keyword, node)
                    self.rotate(node.left)
                    break
                node = node.left
            else:
                if node.right == None:
                    node.right = Node(keyword, node)
                    self.rotate(node.right)
                    break
                node = node.right

    def find_unbalance_node(self, node):
        if node.parent:
            # 用于标记插入发生在左子树还是右子树
            is_left = node is node.parent.left
        node = node.parent

        while node != None:
            if is_left:
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
            if node.parent:
                is_left = node is node.parent.left
            node = node.parent

    def rotate_ll(self, node):
        parent = node.parent
        A = node
        B = node.left
        BR = B.right

        B.parent = parent
        if parent == None:
            self._root_node = B
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
        if parent == None:
            self._root_node = C
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
        if parent == None:
            self._root_node = B
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
        if parent == None:
            self._root_node = C
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
        left_child = unbalance_node.left
        right_child = unbalance_node.right
        if unbalance_node.balance_factor > 0:
            if left_child.balance_factor > 0:
                self.rotate_ll(unbalance_node)
            else:
                self.rotate_lr(unbalance_node)
        else:
            if right_child.balance_factor < 0:
                self.rotate_rr(unbalance_node)
            else:
                self.rotate_rl(unbalance_node)

    def bfs(self):
        if not self._root_node:
            return []

        queue = [self._root_node]
        cursor = 0
        while cursor < len(queue):
            node = queue[cursor]
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
            cursor = cursor + 1
        return queue

    @classmethod
    def get_height(cls, node):
        if node == None:
            return 0
        if node.left == None and node.right == None:
            return 1
        return max(cls.get_height(node.left), cls.get_height(node.right)) + 1

    def delete_keyword(self, keyword):
        if not self._root_node:
            return

        node = self._root_node
        while node != None:
            if node.keyword == keyword:
                break
            if node.keyword > keyword:
                node = node.left
            else:
                node = node.right
        else:
            return

        if node is self._root_node and (node.left == None or node.right == None):
            self._root_node = node.left or node.right
            return

        real_deleted_node = node
        if node.left != None:
            real_deleted_node = node.left
            while real_deleted_node.right != None:
                real_deleted_node = real_deleted_node.right
        node.keyword = real_deleted_node.keyword
        self.rotate2(real_deleted_node)

    def rotate2(self, real_deleted_node):
        parent = real_deleted_node.parent
        subtree = real_deleted_node.left or real_deleted_node.right
        if real_deleted_node is parent.left:
            parent.left = subtree
            is_left = True
        else:
            parent.right = subtree
            is_left = False
        if subtree != None:
            subtree.parent = parent
        node = parent
        while node != None:
            tmp = node.parent
            tmp_is_left = False
            if tmp:
                tmp_is_left = node is tmp.left
            if is_left:
                if node.balance_factor == 1:
                    node.balance_factor = 0
                elif node.balance_factor == 0:
                    node.balance_factor = -1
                    break
                else:
                    node.balance_factor = -2
                    if node.right.balance_factor > 0:
                        self.rotate_rl2(node)
                    elif node.right.balance_factor == 0:
                        self.rotate_rr2(node)
                        break
                    else:
                        self.rotate_rr2(node)
            else:
                if node.balance_factor == 1:
                    node.balance_factor = 2
                    if node.left.balance_factor < 0:
                        self.rotate_lr2(node)
                    elif node.left.balance_factor == 0:
                        self.rotate_ll2(node)
                        break
                    else:
                        self.rotate_ll2(node)
                elif node.balance_factor == 0:
                    node.balance_factor = 1
                    break
                else:
                    node.balance_factor = 0
            node = tmp
            is_left = tmp_is_left

    def rotate_ll2(self, node):
        parent = node.parent
        A = node
        B = A.left
        BR = B.right

        B.parent = parent
        if parent == None:
            self._root_node = B
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

    def rotate_lr2(self, node):
        parent = node.parent
        A = node
        B = A.left
        C = B.right
        CL = C.left
        CR = C.right

        C.parent = parent
        if parent == None:
            self._root_node = C
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

    def rotate_rl2(self, node):
        parent = node.parent
        A = node
        B = A.right
        C = B.left
        CL = C.left
        CR = C.right

        C.parent = parent
        if parent == None:
            self._root_node = C
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

    def rotate_rr2(self, node):
        parent = node.parent
        A = node
        B = node.right
        BL = B.left

        B.parent = parent
        if parent == None:
            self._root_node = B
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
    def is_valid_avl_tree(cls, root_node):
        if not root_node:
            return 0
        if root_node.balance_factor not in [-1, 0, 1]:
            return 1
        if root_node.balance_factor != (
            cls.get_height(root_node.left) -
                cls.get_height(root_node.right)):
            return 2
        if root_node.left and root_node.left.keyword >= root_node.keyword:
            return 3
        if root_node.right and root_node.right.keyword < root_node.keyword:
            return 4

        left_status = cls.is_valid_avl_tree(root_node.left)
        if left_status != 0:
            return left_status
        right_status = cls.is_valid_avl_tree(root_node.right)
        if right_status != 0:
            return right_status
        return 0

if __name__ == "__main__":
    import random
    min_keyword = 1
    max_keyword = random.choice(range(50, 100))
    array = range(min_keyword, max_keyword)
    random.shuffle(array)
    print(array)
    tree = AVLTree()
    for keyword in array:
        tree.insert_keyword(keyword)

    print(tree.root_node)
    status = AVLTree.is_valid_avl_tree(tree.root_node)
    print(status == 0)

    random.shuffle(array)
    for keyword in array:
        print("delete keyword: %s" % keyword)
        tree.delete_keyword(keyword)
        status = AVLTree.is_valid_avl_tree(tree.root_node)
        print(status == 0)
        if status != 0:
            print(tree.root_node)
    print(tree.root_node)

