#coding: utf8

class Node:
    def __init__(self, element=None, parent=None,
            left=None, right=None, balance_factor=0):
        self._element = element
        self._parent = parent
        self._left = left
        self._right = right
        self._bf = balance_factor

    def set_element(self, element):
        self._element = element
        return self

    def get_element(self):
        return self._element

    def set_parent(self, parent):
        self._parent = parent
        return self

    def get_parent(self):
        return self._parent

    def set_left(self, left):
        self._left = left
        return self

    def get_left(self):
        return self._left

    def set_right(self, right):
        self._right = right
        return self

    def get_right(self):
        return self._right

    def set_bf(self, balance_factor):
        self._bf = balance_factor
        return self

    def get_bf(self):
        return self._bf

    def __str__(self):
        return "Node[element={0._element}, bf={0._bf}, " \
            "left={0._left}, right={0._right}]".format(self)

    def find_unbalance_node(self, node):
        subnode = None
        parent = node.get_parent()
        while parent:
            if node == parent.get_left():
                if parent.get_bf() == -1:
                    parent.set_bf(0)
                    break
                if parent.get_bf() == 1:
                    return subnode, node, parent
                parent.set_bf(1)
            else:
                if parent.get_bf() == 1:
                    parent.set_bf(0)
                    break
                if parent.get_bf() == -1:
                    return subnode, node, parent
                parent.set_bf(-1)
            subnode = node
            node = parent
            parent = parent.get_parent()
        return None, None, None

    def rotate(self, inserted_node):
        # 寻找失衡点
        subnode, node, parent = self.find_unbalance_node(inserted_node)
        if not subnode:
            return

        if subnode == node.get_left() and node == parent.get_left():
            self.rotate_ll(subnode, node, parent)
        elif subnode == node.get_right() and node == parent.get_left():
            self.rotate_lr(subnode, node, parent)
        elif subnode == node.get_right() and node == parent.get_right():
            self.rotate_rr(subnode, node, parent)
        else:
            self.rotate_rl(subnode, node, parent)

    def rotate_ll(self, subnode, node, parent):
        temp = parent.get_element()
        parent.set_element(node.get_element())
        node.set_element(temp)

        parent.set_bf(0)
        parent.set_left(subnode.set_parent(parent))

        node.set_bf(0)
        node.set_left(node.get_right())
        node.set_right(parent.get_right())
        if (parent.get_right()):
            parent.get_right().set_parent(node)
        
        parent.set_right(node)

    def rotate_lr(self, subnode, node, parent):
        temp = parent.get_element()
        parent.set_element(subnode.get_element())
        subnode.set_element(temp)

        parent.set_bf(0)
        
        node.set_right(subnode.get_left())
        if subnode.get_left():
            subnode.get_left().set_parent(node)

        subnode.set_left(subnode.get_right())
        subnode.set_right(parent.get_right())
        if parent.get_right():
            parent.get_right().set_parent(subnode)
        if subnode.get_bf() == -1:
            subnode.set_bf(0)
            node.set_bf(1)
        elif subnode.get_bf() == 0:
            subnode.set_bf(0)
            node.set_bf(0)
        else:
            subnode.set_bf(-1)
            node.set_bf(0)

        parent.set_right(subnode.set_parent(parent))

    def rotate_rl(self, subnode, node, parent):
        temp = parent.get_element()
        parent.set_element(subnode.get_element())
        subnode.set_element(temp)

        parent.set_bf(0)
        pl = parent.get_left()
        sl = subnode.get_left()
        sr = subnode.get_right()
        node.set_left(sr)
        if sr:
            sr.set_parent(node)

        subnode.set_right(sl)
        subnode.set_left(pl)
        if pl:
            pl.set_parent(subnode)

        if subnode.get_bf() == 1:
            subnode.set_bf(0)
            node.set_bf(-1)
        elif subnode.get_bf() == 0:
            subnode.set_bf(0)
            node.set_bf(0)
        else:
            subnode.set_bf(1)
            node.set_bf(0)

        parent.set_left(subnode.set_parent(parent))

    def rotate_rr(self, subnode, node, parent):
        temp = parent.get_element()
        parent.set_element(node.get_element())
        node.set_element(temp)
    
        parent.set_bf(0)
        pl = parent.get_left()
        parent.set_right(subnode.set_parent(parent))

        node.set_bf(0)
        node.set_right(node.get_left())
        node.set_left(pl)
        if pl:
            pl.set_parent(node)

        parent.set_left(node)

    def insert_element(self, element):
        if self.get_element() == None:
            self.set_element(element)
            return

        node = self
        while True:
            if node.get_element() < element:
                if node.get_right() == None:
                    inserted_node = Node(element).set_parent(node)
                    node.set_right(inserted_node)
                    self.rotate(inserted_node)
                    break
                node = node.get_right()
            else:
                if node.get_left() == None:
                    inserted_node = Node(element).set_parent(node)
                    node.set_left(inserted_node)
                    self.rotate(inserted_node)
                    break
                node = node.get_left()

    @classmethod
    def get_height(cls, root):
        if not root:
            return 0

        left_height = cls.get_height(root.get_left())
        right_height = cls.get_height(root.get_right())
        if left_height > right_height:
            return left_height + 1
        return right_height + 1

    @classmethod
    def is_valid_avl(cls, root):
        if not root or not root.get_element():
            return True

        left_child = root.get_left()
        right_child = root.get_right()

        if left_child and left_child.get_element() > root.get_element():
            return False
        if right_child and right_child.get_element() < root.get_element():
            return False

        left_height = cls.get_height(left_child)
        right_height = cls.get_height(right_child)
        if abs(left_height - right_height) > 1:
            return False

        #no qa
        if root.get_bf() != left_height - right_height:
            return False
        if not cls.is_valid_avl(left_child):
            return False
        if not cls.is_valid_avl(right_child):
            return False
        return True

    def search_element(self, element):
        if not self.get_element():
            return None
        node = self
        while node:
            if node.get_element() == element:
                return node
            if node.get_element() > element:
                node = node.get_left()
            else:
                node = node.get_right()
        return None

    def find_unbalance_node_2(self, subtree, position, parent):
        while parent:
            if position == 0:
                if parent.get_bf() == 0:
                    parent.set_bf(-1)
                    break
                if parent.get_bf() == -1:
                    return subtree, position, parent
            else:
                if parent.get_bf() == 0:
                    parent.set_bf(1)
                    break
                if parent.get_bf() == 1:
                    return subtree, position, parent
            parent.set_bf(0)
            subtree = parent
            parent = parent.get_parent()
            if parent:
                position = 0 if parent.get_left() == subtree else 1
        return None, None, None

    def delete_element(self, element):
        if element is None:
            return False
        node = self.search_element(element)
        if not node:
            return False

        # 整棵树只有一个节点
        if not node.get_left() and \
                not node.get_right() and \
                not node.get_parent():
            node.set_element(None)
            return True

        real_deleted_node = node
        # 左子树的最右节点
        if node.get_left():
            real_deleted_node = node.get_left()
            while real_deleted_node.get_right():
                real_deleted_node = real_deleted_node.get_right()
        # 或者右子树的最左节点
        elif node.get_right():
            real_deleted_node = node.get_right()
            while real_deleted_node.get_left():
                real_deleted_node = real_deleted_node.get_left()
        # 交换关键字
        node.set_element(real_deleted_node.get_element())

        parent = real_deleted_node.get_parent()
        if real_deleted_node.get_left():
            subtree = real_deleted_node.get_left()
        else:
            subtree = real_deleted_node.get_right()
        if real_deleted_node == parent.get_left():
            position = 0
            parent.set_left(subtree)
        else:
            position = 1
            parent.set_right(subtree)

        while parent:
            subtree, position, unbalance_node = \
                self.find_unbalance_node_2(subtree, position, parent)
            if not unbalance_node:
                return True

            ul = unbalance_node.get_left()
            ur = unbalance_node.get_right()
            if unbalance_node.get_bf() == -1:
                if ur.get_bf() == 0 or ur.get_bf() == -1:
                    subtree, position, parent = self.rotate_rr_2(
                        subtree, unbalance_node)
                    continue
                subtree, position, parent = self.rotate_rl_2(
                        subtree, unbalance_node)
                continue
            if ul.get_bf() == 0 or ul.get_bf() == 1:
                subtree, position, parent = self.rotate_ll_2(
                    subtree, unbalance_node)
                continue
            subtree, position, parent = self.rotate_lr_2(
                    subtree, unbalance_node)
        return True

    def rotate_lr_2(self, subtree, unbalance_node):
        a = unbalance_node
        b = a.get_left()
        c = b.get_right()
        cl = c.get_left()
        cr = c.get_right()

        temp = a.get_element()
        a.set_element(c.get_element())
        c.set_element(temp)

        b.set_right(cl)
        if cl:
            cl.set_parent(b)

        c.set_left(cr)
        c.set_right(subtree)
        if subtree:
            subtree.set_parent(c)
        a.set_right(c.set_parent(a))

        if c.get_bf() == 0:
            a.set_bf(0)
            b.set_bf(0)
            c.set_bf(0)
        elif c.get_bf() == 1:
            a.set_bf(0)
            b.set_bf(0)
            c.set_bf(-1)
        else:
            a.set_bf(0)
            b.set_bf(1)
            c.set_bf(0)
        p = a.get_parent()
        return a, 0 if p and p.get_left() == a else 0, p

    def rotate_ll_2(self, subtree, unbalance_node):
        a = unbalance_node
        b = a.get_left()
        bl = b.get_left()
        br = b.get_right()

        temp = a.get_element()
        a.set_element(b.get_element())
        b.set_element(temp)

        a.set_left(bl.set_parent(a))

        b.set_left(br)
        b.set_right(subtree)
        if subtree:
            subtree.set_parent(b)
        a.set_right(b)

        if b.get_bf() == 0:
            a.set_bf(-1)
            b.set_bf(1)
            return None, None, None
        a.set_bf(0)
        b.set_bf(0)
        p = a.get_parent()
        return a, 0 if p and p.get_left() == a else 0, p

    def rotate_rl_2(self, subtree, unbalance_node):
        a = unbalance_node
        b = a.get_right()
        c = b.get_left()

        temp = a.get_element()
        a.set_element(c.get_element())
        c.set_element(temp)

        cl = c.get_left()
        cr = c.get_right()

        b.set_left(cr)
        if cr:
            cr.set_parent(b)

        c.set_right(cl)
        c.set_left(subtree)
        if subtree:
            subtree.set_parent(c)

        a.set_left(c.set_parent(a))

        if c.get_bf() == 0:
            a.set_bf(0)
            b.set_bf(0)
            c.set_bf(0)
        elif c.get_bf() == 1:
            a.set_bf(0)
            b.set_bf(-1)
            c.set_bf(0)
        else:
            a.set_bf(0)
            b.set_bf(0)
            c.set_bf(1)
        p = a.get_parent()
        return a, 0 if p and p.get_left() == a else 0, p

    def rotate_rr_2(self, subtree, unbalance_node):
        a = unbalance_node
        b = a.get_right()

        temp = a.get_element()
        a.set_element(b.get_element())
        b.set_element(temp)

        bl = b.get_left()
        br = b.get_right()
        a.set_right(br.set_parent(a))
        b.set_right(bl)
        b.set_left(subtree)
        if subtree:
            subtree.set_parent(b)
        a.set_left(b)

        if b.get_bf() == 0:
            a.set_bf(1)
            b.set_bf(-1)
            return None, None, None
        a.set_bf(0)
        b.set_bf(0)
        p = a.get_parent()
        return a, 0 if p and p.get_left() == a else 0, p

if __name__ == "__main__":
    root = Node()
    for i in [100, 80, 110, 70]: 
        root.insert_element(i)
    print "\033[31mroot is:\033[0m"
    print root
    root.delete_element(110)
    print root
    print Node.is_valid_avl(root)
    print

