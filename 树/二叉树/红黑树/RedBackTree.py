#coding: utf8

from abc import ABCMeta, abstractmethod

class BaseNode(object):
    __metaclass__ = ABCMeta

    def is_valid_bst(self):
        if not self.get_element():
            return True

        queue = [self]
        while queue:
            node = queue.pop(0)
            if node.get_left() and \
                node.get_left().get_element() > node.get_element():
                return False
            if node.get_right() and \
                node.get_right().get_element() < node.get_element():
                return False
        return True

    @abstractmethod
    def get_element(self):
        pass

    @abstractmethod
    def get_left(self):
        pass

    @abstractmethod
    def get_right(self):
        pass

    def search_element(self, element):
        if not self.get_element():
            raise KeyError("there is no element: %s" % str(element))

        node = self
        while node:
            if node.get_element() == element:
                return node
            if element > node.get_element():
                node = node.get_right()
                continue
            node = node.get_left()
        raise KeyError("there is no element: %s" % str(element))

class Node(BaseNode):
    def __init__(self, element=None, color=1):
        self._element = element
        # color = 0 代表节点是黑节点，1代表节点是红节点
        self._color = color

        self._parent = None
        self._left = None
        self._right = None

    def get_element(self):
        return self._element

    def set_element(self, element):
        self._element = element
        return self

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        return self

    def get_parent(self):
        return self._parent

    def get_left(self):
        return self._left

    def get_right(self):
        return self._right

    def set_parent(self, parent):
        self._parent = parent
        return self

    def set_left(self, left):
        self._left = left
        return self

    def set_right(self, right):
        self._right = right
        return self

    def case00(self, node, parent, grand_parent, uncle):
        temp = grand_parent.get_element()
        grand_parent.set_element(parent.get_element())
        parent.set_element(temp)

        grand_parent.set_left(node.set_parent(grand_parent))
        parent.set_left(parent.get_right())
        parent.set_right(uncle)
        if uncle:
            uncle.set_parent(parent)
        grand_parent.set_right(parent)

    def case01(self, node, parent, grand_parent, uncle):
        temp = grand_parent.get_element()
        grand_parent.set_element(node.get_element())
        node.set_element(temp)

        nl = node.get_left()
        parent.set_right(nl)
        if nl:
            nl.set_parent(parent)

        node.set_left(node.get_right())
        node.set_right(uncle)
        if uncle:
            uncle.set_parent(node)

        grand_parent.set_right(node.set_parent(grand_parent))

    def case10(self, node, parent, grand_parent, uncle):
        temp = grand_parent.get_element()
        grand_parent.set_element(node.get_element())
        node.set_element(temp)

        nr = node.get_right()
        parent.set_left(nr)
        if nr:
            nr.set_parent(parent)

        node.set_right(node.get_left())
        node.set_left(uncle)
        if uncle:
            uncle.set_parent(node)

        grand_parent.set_left(node.set_parent(grand_parent))

    def case11(self, node, parent, grand_parent, uncle):
        temp = grand_parent.get_element()
        grand_parent.set_element(parent.get_element())
        parent.set_element(temp)

        grand_parent.set_right(node.set_parent(grand_parent))

        parent.set_right(parent.get_left())
        parent.set_left(uncle)
        if uncle:
            uncle.set_parent(parent)

        grand_parent.set_left(parent)

    def rotate(self, node):
        parent = node.get_parent()
        # case 1: 父节点是黑色的，无需调整
        if parent.get_color() == 0:
            return

        grand_parent = parent.get_parent()
        # 以下情况中，父节点是红色的
        # + 祖父节点一定是黑色的

        # parent_position = 0 代表父节点是祖父节点的左孩子
        # parent_position = 1 代表父节点是祖父节点的右孩子
        # position = 0 代表节点是父节点的左孩子
        # position = 1 代表节点是父节点的右孩子
        parent_position = 0
        uncle = grand_parent.get_right()
        if uncle == parent:
            uncle = grand_parent.get_left()
            parent_position = 1
        position = 0
        if node == parent.get_right():
            position = 1

        # case 2: 叔叔是黑色的
        if not uncle or uncle.get_color() == 0:
            # case 2-1: 父亲是祖父的左孩子，插入节点也是父亲的左孩子
            # + 此时，需要以父亲为轴，将祖父右旋，并重新染色
            if parent_position == 0 and position == 0:
                self.case00(node, parent, grand_parent, uncle)
            # case 2-2: 父亲是祖父的左孩子，插入节点是父亲的右孩子
            # + 此时，先以node为轴，将parent左旋；
            # + + 再以node为轴，将grand_parent右旋；并重新染色
            elif parent_position == 0 and position == 1:
                self.case01(node, parent, grand_parent, uncle)
            # case 2-3: 父亲是祖父的右孩子，插入节点是父亲的左孩子
            # + 此时，先以node为轴，将parent右旋；
            # + + 再以node为轴，将grand_parent左旋；并重新染色
            elif parent_position == 1 and position == 0:
                self.case10(node, parent, grand_parent, uncle)
            # case 2-4: 父亲是祖父的右孩子，插入节点也是父亲的右孩子
            # + 此时，以parent为轴，将grand_parent左旋；并重新染色
            elif parent_position == 1 and position == 1:
                self.case11(node, parent, grand_parent, uncle)
            return

        # case 3: 叔叔是红色的
        # + 此时，将parent和uncle涂黑，然后将grand_parent涂红，
        # + + 然后向上回溯，一直到根节点
        parent.set_color(0)
        uncle.set_color(0)
        if grand_parent.get_parent() is None:
            return
        grand_parent.set_color(1)
        self.rotate(grand_parent)

    def insert_element(self, element):
        if self.get_element() is None:
            self.set_element(element)
            return

        node = self
        while True:
            if element >= node.get_element():
                if node.get_right() == None:
                    inserted_node = Node(element, 1).set_parent(node)
                    node.set_right(inserted_node)
                    self.rotate(inserted_node)
                    break
                node = node.get_right()
                continue

            if node.get_left() == None:
                inserted_node = Node(element, 1).set_parent(node)
                node.set_left(inserted_node)
                self.rotate(inserted_node)
                break
            node = node.get_left()

    def __str__(self):
        return "Node[element={0._element}, color={0._color}," \
            " left={0._left}, right={0._right}]".format(self)

    def inorder_traverse(self):
        if self.get_left():
            self.get_left().inorder_traverse()
        print self.get_element(), self.get_color() and "红色" or "黑色"
        if self.get_right():
            self.get_right().inorder_traverse()

    def delete_node(self, node):
        # 二叉查找树删除节点的本质是：
        # + 使用右子树的最左节点（左子树的最右节点）的关键字覆盖
        # + + 要被删除的节点的关键字，
        # + + 然后删除右子树的最左节点（左子树的最右节点）

        deleted_node = node
        right_child = node.get_right()
        if right_child:
            deleted_node = right_child
            while deleted_node.get_left():
                deleted_node = deleted_node.get_left()
        node.set_element(deleted_node.get_element())

        # deleted_node 要么左子树为空，要么右子树为空，要么都为空

        # case 1: deleted_node是红色的
        # + 此时，只要使用非空节点替代deleted_node即可
        if self.delete_case_1(deleted_node):
            return

        # 以下情况中，待删除节点都是黑色的

        # case 2: 不为空的子树的根节点是红色的
        # + 此时，只要使用非空子树的根替代deleted_node即可（颜色不用替换）
        if self.delete_case_2(deleted_node):
            return

        # 以下情况中，待删除节点的左右子树都是空的

        # 待删除节点是根节点
        # 此时，将根节点的元素置空
        if not deleted_node.get_parent():
            deleted_node.set_element(None)
            return

        # 将subtree接到parent上，表明 待删除节点 已经被从树中删除。
        # + 同时，sibling节点一定不是空的，
        # + 并且subtree所在的子树的黑节点数量 比 sibling子树的数量少1
        # + subtree是黑色的
####################
# 比如，一种形式是：
#       p
#      / \
#     /   \
# subtree sibling
####################
        subtree = None
        parent = deleted_node.get_parent()
        if deleted_node == parent.get_left():
            sibling = parent.get_right()
            parent.set_left(subtree)
        else:
            sibling = parent.get_left()
            parent.set_right(subtree)

        # 还剩下两种大情况：
        # + 1，sibling是红的（此种情况会转换成第二种情况）
        # + 2，sibling是黑的
        # !!!delete_black_sibling的终极目的是将subtree的黑节点数量增加1!!!
        self.delete_black_sibling(subtree, sibling, parent)

    def delete_case_3(self, subtree, sibling, parent):
        if sibling.get_color() == 0:
            return False

        # 此时分两种情况：
        # + 1，subtree是左孩子，sibling是右孩子
        # + 2，subtree是右孩子，sibling是左孩子
        temp = parent.get_element()
        parent.set_element(sibling.get_element())
        sibling.set_element(temp)
        sl = sibling.get_left()
        sr = sibling.get_right()

        # 第一种情况，以sibling为轴将parent左旋，然后重新染色
        # + 此时，subtree的兄弟节点已经从sibling变成了sl，并且从红色变成了黑色
        if subtree == parent.get_left():
            parent.set_right(sr.set_parent(parent))
            sibling.set_right(sl)
            sibling.set_left(subtree)
            if subtree:
                subtree.set_parent(sibling)
            parent.set_left(sibling)
            return subtree, sl, sibling

        # 第二种情况，以sibling为轴将parent右旋，然后重新染色
        # + 此时，subtree的兄弟节点已经从sibling变成了sr，并且从红色变成了黑色
        parent.set_left(sl.set_parent(parent))
        sibling.set_left(sr)
        sibling.set_right(subtree)
        if subtree:
            subtree.set_parent(sibling)
        parent.set_right(sibling)
        return subtree, sr, sibling

    def delete_black_sibling(self, subtree, sibling, parent):
        # 用sl表示sbling的左孩子；sr表示sibling的右孩子
        # 如果sibling是红色的，那么sl，sr都非空，且是黑色的
        # + 此时，通过旋转和染色，将这种情况转换成sibling是黑色的情况
        result = self.delete_case_3(subtree, sibling, parent)
        if result:
            subtree, sibling, parent = result

        # 以下的情况中，sibling都是黑色的

        # SL为红色，SR，parent任意
        if self.delete_case_4(subtree, sibling, parent):
            return
        # SR为红色，SL，parent任意
        if self.delete_case_5(subtree, sibling, parent):
            return
        # SL SR均为黑色，且P为红色
        if self.delete_case_6(subtree, sibling, parent):
            return
        # SL SR均为黑色，且P为黑色
        # 此时，无法直接从sibling"借"节点了，所以，索性将sibling染红，
        # + 这样以parent为根的整棵子树的黑节点数都减少1了，
        # + 然后把parent当作subtree角色，进行回溯，一直到根节点
        sibling.set_color(1)
        if not parent.get_parent():
            return

        subtree = parent
        parent = parent.get_parent()
        sibling = parent.get_left()
        if sibling == subtree:
            sibling = parent.get_right()

        self.delete_black_sibling(subtree, sibling, parent)

    def delete_case_6(self, subtree, sibling, parent):
        sl = sibling.get_left()
        sr = sibling.get_right()
        if sl and sl.get_color() == 1:
            return False
        if sr and sr.get_color() == 1:
            return False
        if parent.get_color() == 0:
            return False

        # 此时，只需要将parent染成黑色，sibling染成红色即可
        parent.set_color(0)
        sibling.set_color(1)
        return True

    def delete_case_5(self, subtree, sibling, parent):
        sr = sibling.get_right()
        if not sr or sr.get_color() == 0:
            return False
        srl = sr.get_left()
        srr = sr.get_right()

        # 此时，分两种情况：
        # + 1，subtree是左子树
        # + 2，subtree是右子树
        if subtree == sibling.get_left():
            # 第一种情况
            # + 以sibling为轴将P左转，并重新染色
            temp = parent.get_element()
            parent.set_element(sibling.get_element())
            sibling.set_element(temp)

            sr.set_color(0)
            parent.set_right(sr.set_parent(parent))

            sibling.set_right(sibling.get_left())
            sibling.set_left(subtree)
            if subtree:
                subtree.set_parent(sibling)
            parent.set_left(sibling)
            return True

        # 第二种情况
        # + 先以SR为轴，将sibling左旋
        # + + 再以SR为轴，将parent右旋；然后重新染色
        temp = parent.get_element()
        parent.set_element(sr.get_element())
        sr.set_element(temp)

        sibling.set_right(srl)
        if srl:
            srl.set_parent(sibling)

        sr.set_color(0)
        sr.set_left(srr)
        sr.set_right(subtree)
        if subtree:
            subtree.set_parent(sr)

        parent.set_right(sr.set_parent(parent))
        return True

    def delete_case_4(self, subtree, sibling, parent):
        sl = sibling.get_left()
        if not sl or sl.get_color() == 0:
            return False

        sll = sl.get_left()
        slr = sl.get_right()

        # 此时，分两种情况：
        # + 1，subtree是左子树
        # + 2，subtree是右子树
        if subtree == parent.get_left():
            # 第一种情况，
            # + 先以sl为轴，将sibling右旋，
            # + + 再以sl为轴，将parent左旋；并重新染色
            temp = parent.get_element()
            parent.set_element(sl.get_element())
            sl.set_element(temp)

            sibling.set_left(slr)
            if slr:
                slr.set_parent(sibling)

            sl.set_color(0)
            sl.set_left(subtree)
            if subtree:
                subtree.set_parent(sl)
            sl.set_right(sll)
            
            parent.set_left(sl.set_parent(parent))
        else:
            # 第二种情况：
            # + 以sibling为轴将parent右旋，并重新染色
            temp = parent.get_element()
            parent.set_element(sibling.get_element())
            sibling.set_element(temp)

            sl.set_color(0)
            parent.set_left(sl.set_parent(parent))

            sibling.set_left(sibling.get_right())
            sibling.set_right(subtree)
            if subtree:
                subtree.set_parent(sibling)

            parent.set_right(sibling)
        return True

    def delete_case_2(self, deleted_node):
        left_child = deleted_node.get_left()
        right_child = deleted_node.get_right()

        subtree = None
        if left_child is None:
            if right_child and right_child.get_color() == 1:
                subtree = right_child
        elif right_child is None:
            if left_child and left_child.get_color() == 1:
                subtree = left_child
        if not subtree:
            return False

        deleted_node.set_element(subtree.get_element())
        deleted_node.set_left(subtree.get_left())
        deleted_node.set_right(subtree.get_right())
        return True

    def delete_case_1(self, deleted_node):
        if deleted_node.get_color() == 0:
            return False

        subtree = deleted_node.get_left()
        if not subtree:
            subtree = deleted_node.get_right()

        if deleted_node.get_parent().get_left() == deleted_node:
            deleted_node.get_parent().set_left(subtree)
        else:
            deleted_node.get_parent().set_right(subtree)
        return True

    def delete_element(self, element):
        node = self

        while node:
            if node.get_element() == element:
                return self.delete_node(node)
            elif node.get_element() < element:
                node = node.get_right()
            else:
                node = node.get_left()
        raise KeyError("there is no element in this tree")

if __name__ == "__main__":
    root = Node(None, 0)
    
    for i in [12, 1, 9, 2, 0, 11, 7, 19, 4, 15, 18, 5, 14, 13, 10, 16, 6, 3, 8, 17]:
        root.insert_element(i)
    for i in [12, 1, 9, 2, 0, 11, 7, 19, 4, 15, 18, 5, 14, 13]:
        root.delete_element(i)
    print root
    print "=========="
    print root.get_left()
    print "=========="
    print root.get_right()

