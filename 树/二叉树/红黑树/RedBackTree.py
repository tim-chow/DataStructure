# coding: utf8


class Color(object):
    """
    颜色枚举
    """
    RED   = 'r'
    BLACK = 'b'


class Node(object):
    """
    红黑树的节点
    """
    def __init__(self, keyword, color=Color.RED, parent=None, left=None, right=None):
        self.keyword = keyword
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self):
        return "%s{keyword=%s, color=%s, left=%s, right=%s}" % (
            self.__class__.__name__,
            self.keyword,
            self.color,
            self.left,
            self.right
        )


class RedBlackTree(object):
    """
    红黑树实现
    """
    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    def rotate(self, node):
        while node is not None:
            # 如果 node 是根节点，并且是红色的，那么涂黑即可
            if node is self._root:
                if node.color == Color.RED:
                    node.color = Color.BLACK
                break

            N = node
            P = N.parent
            # 如果父节点是黑色的，那么无需调整
            if P.color == Color.BLACK:
                break

            # 如果父节点是红色的，那么祖父节点一定存在，且是黑色的
            G = P.parent

            left = N is P.left

            if P is G.left:
                parent_left = True
                U = G.right
            else:
                parent_left = False
                U = G.left

            # case 1：如果 U 是红色的，那么将 P、U 染黑，将 G 染红，然后继续向上调整
            if U is not None and U.color == Color.RED:
                P.color = Color.BLACK
                U.color = Color.BLACK
                G.color = Color.RED
                node = G
                continue

            # case 2：如果 U 是黑色的，且 P 是 G 的左孩子，N 是 P 的右孩子，那么
            # 先以 N 为轴将 P 左旋，再以 N 为轴将 G 右旋，然后将 N 染黑，将 G 染红
            """
            G（黑）                      G(黑)                    N（黑）
          /      \                    /       \                /       \
        P（红）   U（黑） --->        N（红）    U(黑) --->     P（红）  G（红）
           \                       /                                    \
         N（红）                P（红）                                  U（黑）
            """
            if parent_left and not left:
                NL = N.left
                NR = N.right
                GP = G.parent

                N.parent = GP
                if GP is None:
                    self._root = N
                elif G is GP.left:
                    GP.left = N
                else:
                    GP.right = N
                N.left = P
                N.right = G
                N.color = Color.BLACK

                P.parent = N
                P.right = NL
                if NL is not None:
                    NL.parent = P

                G.parent = N
                G.left = NR
                if NR is not None:
                    NR.parent = G
                G.color = Color.RED
                break

            # case 3：如果 U 是黑色的，且 P 是 G 的左孩子，N 是 P 的左孩子，那么
            # 以 P 为轴，将 G 右旋，最后将 P 染黑，G 染红
            """
             G (黑)                              P（黑）
           /       \                          /       \
          P（红）    U（黑）     --->         N（红）    G（红）
         /                                              \
        N（红）                                          U（黑）
            """
            if parent_left and left:
                GP = G.parent
                PR = P.right

                P.parent = GP
                if GP is None:
                    self._root = P
                elif G is GP.left:
                    GP.left = P
                else:
                    GP.right = P
                P.right = G
                P.color = Color.BLACK

                G.parent = P
                G.left = PR
                if PR is not None:
                    PR.parent = G
                G.color = Color.RED
                break

            # case 4：如果 U 是黑色的，并且 P 是 G 的右孩子，N 是 P 的右孩子，那么
            # 以 P 为轴将 G 左旋，然后将 P 染黑，G 染红
            if not parent_left and not left:
                GP = G.parent
                PL = P.left

                P.parent = GP
                if GP is None:
                    self._root = P
                elif G is GP.left:
                    GP.left = P
                else:
                    GP.right = P
                P.left = G
                P.color = Color.BLACK

                G.parent = P
                G.right = PL
                if PL is not None:
                    PL.parent = G
                G.color = Color.RED
                break

            # case 5：如果 U 是黑色的，并且 P 是 G 的右孩子，N 是 P 的左孩子，那么
            # 先以 N 为轴将 P 右旋，再以 N 为轴将 G 左旋，然后将 N 染黑，将 G 染红
            if not parent_left and left:
                GP = G.parent
                NL = N.left
                NR = N.right

                N.parent = GP
                if GP is None:
                    self._root = N
                elif G is GP.left:
                    GP.left = N
                else:
                    GP.right = N
                N.left = G
                N.right = P
                N.color = Color.BLACK

                G.parent = N
                G.right = NL
                if NL is not None:
                    NL.parent = G
                G.color = Color.RED

                P.parent = N
                P.left = NR
                if NR is not None:
                    NR.parent = P
                break

    def insert_keyword(self, keyword):
        if self._root is None:
            self._root = Node(keyword, Color.BLACK)
            return

        node = self._root
        while True:
            if keyword < node.keyword:
                if node.left is None:
                    inserted_node = Node(keyword, Color.RED, node)
                    node.left = inserted_node
                    self.rotate(inserted_node)
                    break
                node = node.left
                continue

            if node.right is None:
                inserted_node = Node(keyword, Color.RED, node)
                node.right = inserted_node
                self.rotate(inserted_node)
                break
            node = node.right

    def delete_node(self, node):
        # 二叉搜索树删除节点的本质是：
        # 使用右子树的最左节点（或左子树的最右节点）的关键字替代
        # 待删除的节点的关键字，然后删除右子树的最左节点（或左子树的最右节点）
        deleted_node = node
        if node.right:
            deleted_node = node.right
            while deleted_node.left is not None:
                deleted_node = deleted_node.left
        node.keyword = deleted_node.keyword

        # deleted_node 要么左子树为空，要么右子树为空，要么都为空
        subtree = deleted_node.left or deleted_node.right
        P = deleted_node.parent

        # case 1：如果删除的是根节点，
        if P is None:
            # 并且 subtree 为空，那么将树置空
            if subtree is None:
                self._root = None
            # 否则，将 subtree 染黑并置为根节点
            else:
                subtree.parent = P
                subtree.color = Color.BLACK
                self._root = subtree
            return

        # 将 subtree 接到 P，也就是将 deleted_node 删掉
        if deleted_node is P.left:
            P.left = subtree
        else:
            P.right = subtree
        if subtree is not None:
            subtree.parent = P

        # case 2: 如果 deleted_node 是红色的，那么直接退出即可
        if deleted_node.color == Color.RED:
            return

        # 以下情况中，deleted_node 是黑色的

        # case 3：如果 subtree 非空，且是红色的，那么将 subtree 染黑即可
        if subtree is not None and subtree.color == Color.RED:
            subtree.color = Color.BLACK
            return

        # 以下情况中，subtree 要么是空的，要么是黑色的

        while P is not None:
            """
                   P
                /    \
          subtree   sibling
            """
            # 经过 subtree 的分支的黑节点数量比经过 sibling 的分支的黑节点数量少 1，
            # 所以 sibling 一定非空

            # left 表示 sibling 是否是 P 的左孩子
            left = subtree is not P.left
            if left:
                sibling = P.left
            else:
                sibling = P.right

            # case 4：sibling 是 P 的右孩子，且 sibling 是红色的，
            # 那么 P 一定是黑色的，以 sibling 为轴，将 P 左旋，然后将 sibling 染黑，P 染红。
            # 旋转之后 subtree 的 sibling 变成了 SL，并且是黑色的。
            # 经过 subtree 的分支的黑节点数量仍然比删除节点之前少 1
            if not left and sibling.color == Color.RED:
                """
                 P（黑）                                     sibling（黑）
              /        \                                   /            \
      subtree（黑）   sibling(红)         --->             P（红）       SR（黑）
                     /         \                       /    \
                    SL（黑）    SR(黑)             subtree  SL（黑）
                """
                G = P.parent
                SL = sibling.left

                sibling.parent = G
                if G is None:
                    self._root = sibling
                elif P is G.left:
                    G.left = sibling
                else:
                    G.right = sibling
                sibling.left = P
                sibling.color = Color.BLACK

                P.parent = sibling
                P.right = SL
                if SL is not None:
                    SL.parent = P
                P.color = Color.RED

                sibling = SL
                left = False
            # case 5：sibling 是 P 的左孩子，且 sibling 是红色的，
            # 那么以 sibling 为轴，将 P 右旋，然后将 sibling 染黑，P 染红
            elif left and sibling.color == Color.RED:
                G = P.parent
                SR = sibling.right

                sibling.parent = G
                if G is None:
                    self._root = sibling
                elif P is G.left:
                    G.left = sibling
                else:
                    G.right = sibling
                sibling.right = P
                sibling.color = Color.BLACK

                P.parent = sibling
                P.left = SR
                if SR is not None:
                    SR.parent = P
                P.color = Color.RED

                sibling = SR
                left = True

            # case 4 和 5 主要是将 subtree 的兄弟节点转换成黑色的

            SL = sibling.left
            SR = sibling.right

            # case 6：sibling 是 P 的右孩子，且 SL 为红，
            # 那么先以 SL 为轴，将 sibling 右旋，再以 SL 为轴，将 P 左旋，然后将 SL 染成 P 的颜色，将 P 染黑
            if not left and SL is not None and SL.color == Color.RED:
                G = P.parent
                SLL= SL.left
                SLR = SL.right

                SL.parent = G
                if G is None:
                    self._root = SL
                elif P is G.left:
                    G.left = SL
                else:
                    G.right = SL
                SL.left = P
                SL.right = sibling
                SL.color = P.color

                P.parent = SL
                P.right = SLL
                if SLL is not None:
                    SLL.parent = P
                P.color = Color.BLACK

                sibling.parent = SL
                sibling.left = SLR
                if SLR is not None:
                    SLR.parent = sibling
                break

            # case 7：sibling 是 P 的左孩子，且 SL 为红，
            # 那么以 sibling 为轴将 P 右旋，然后将 sibling 染成 P 的颜色，将 P 和 SL 染黑
            if left and SL is not None and SL.color == Color.RED:
                G = P.parent

                sibling.parent = G
                if G is None:
                    self._root = sibling
                elif P is G.left:
                    G.left = sibling
                else:
                    G.right = sibling
                sibling.right = P
                sibling.color = P.color

                P.parent = sibling
                P.left = SR
                if SR is not None:
                    SR.parent = P
                P.color = Color.BLACK

                SL.color = Color.BLACK
                break

            # case 8：sibling 是 P 的右孩子，且 SR 为红，
            # 那么以 sibling 为轴将 P 左旋，然后将 sibling 染成 P 的颜色，将 P 和 SR 染黑
            if not left and SR is not None and SR.color == Color.RED:
                G = P.parent

                sibling.parent = G
                if G is None:
                    self._root = sibling
                elif P is G.left:
                    G.left = sibling
                else:
                    G.right = sibling
                sibling.left = P
                sibling.color = P.color

                P.parent = sibling
                P.right = SL
                if SL is not None:
                    SL.parent = P
                P.color = Color.BLACK

                SR.color = Color.BLACK
                break

            # case 9：sibling 是 P 的左孩子，且 SR 为红，
            # 那么先以 SR 为轴将 sibling 左旋，再以 SR 为轴将 P 右旋，然后将 SR 染成 P 的颜色，将 P 染黑
            if left and SR is not None and SR.color == Color.RED:
                G = P.parent
                SRL = SR.left
                SRR = SR.right

                SR.parent = G
                if G is None:
                    self._root = SR
                elif P is G.left:
                    G.left = SR
                else:
                    G.right = SR
                SR.left = sibling
                SR.right = P
                SR.color = P.color

                P.parent = SR
                P.left = SRR
                if SRR is not None:
                    SRR.parent = P
                P.color = Color.BLACK

                sibling.parent = SR
                sibling.right = SRL
                if SRL is not None:
                    SRL.parent = sibling
                break

            # 以下情况中，SL 和 SR 要么都是黑色的，要么都是空的

            # case 10：如果 P 是红色的，
            # 那么将 P 染黑，将 sibling 染红即可
            if P.color == Color.RED:
                P.color = Color.BLACK
                sibling.color = Color.RED
                break

            # case 11：如果 P 是黑色的，
            # 那么将 sibling 染红，然后从 P 开始继续向上调整，直到根节点
            sibling.color = Color.RED

            subtree = P
            P = P.parent

    def delete_keyword(self, keyword):
        node = self._root

        while node is not None:
            if keyword == node.keyword:
                self.delete_node(node)
                break
            elif keyword < node.keyword:
                node = node.left
            else:
                node = node.right
        else:
            raise KeyError("not found")


def calc_black_count(leaf):
    result = {}
    node = leaf
    count = 0
    while node is not None:
        if node.color == Color.BLACK:
            count = count + 1
        result[node] = count
        node = node.parent
    return result


def is_valid_red_black_tree(root):
    if root is None:
        return True

    if root.color != Color.BLACK:
        return False

    queue = [root]
    black_counts = {}
    while queue:
        node = queue.pop(0)
        if node.left is not None:
            if node.left.keyword > node.keyword:
                return False
            if node.color == Color.RED and node.left.color == Color.RED:
                return False
            queue.append(node.left)

        if node.right is not None:
            if node.right.keyword < node.keyword:
                return False
            if node.color == Color.RED and node.right.color == Color.RED:
                return False
            queue.append(node.right)

        if node.left is None or node.right is None:
            for node, count in calc_black_count(node).items():
                if node not in black_counts:
                    black_counts[node] = count
                elif count != black_counts[node]:
                    return False

    return True


if __name__ == "__main__":
    import random

    keywords = list(range(100))
    random.shuffle(keywords)
    print(keywords)

    tree = RedBlackTree()

    for k in keywords:
        tree.insert_keyword(k)
        assert is_valid_red_black_tree(tree.root), "tree is not RBT"

    random.shuffle(keywords)
    for k in keywords:
        tree.delete_keyword(k)
        assert is_valid_red_black_tree(tree.root), "tree is not RBT"
