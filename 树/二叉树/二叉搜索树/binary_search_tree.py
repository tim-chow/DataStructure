# coding: utf8


class Node(object):
    def __init__(self, keyword=None, left=None, right=None):
        self.keyword = keyword
        self.left = left
        self.right = right

    def __str__(self):
        return "Node{keyword=%s, left=%s, right=%s}" % (
            self.keyword, self.left, self.right)

    __repr__ = __str__


class BinarySearchTree(object):
    def __init__(self):
        self._root_node = None

    def add_keyword(self, keyword):
        if self._root_node == None:
            self._root_node = Node(keyword)
            return

        node = self._root_node
        while node != None:
            if keyword < node.keyword:
                if node.left == None:
                    node.left = Node(keyword)
                    break
                node = node.left
            else:
                if node.right == None:
                    node.right = Node(keyword)
                    break
                node = node.right

    def find_keyword(self, keyword):
        node = self._root_node
        while node != None:
            if keyword < node.keyword:
                node = node.left
            elif keyword > node.keyword:
                node = node.right
            else:
                return node
        return None

    def delete_keyword(self, keyword):
        # 找到待删除节点
        node = self._root_node
        prev_node = None
        is_left = False
        while node != None:
            if keyword == node.keyword:
                break
            prev_node = node
            if keyword < node.keyword:
                is_left = True
                node = node.left
            else:
                is_left = False
                node = node.right
        else:
            return

        # 如果待节点没有左孩子和（或）没有右孩子，
        # + 那么将其非空的子树直接接到其双亲节点
        if not node.left or not node.right:
            subtree = node.left or node.right
            if prev_node == None:
                self._root_node = subtree
                return
            if is_left:
                prev_node.left = subtree
            else:
                prev_node.right = subtree
            return

        # 找到左子树的最右节点，也就是左子树中关键字最大的节点
        # + （该节点的右子树一定为空）
        prev_node = node
        tmp_node = node.left
        is_left = True
        while tmp_node.right != None:
            is_left = False
            prev_node = tmp_node
            tmp_node = tmp_node.right

        # 使用左子树中的最大的关键字替代要删除节点的关键字
        node.keyword = tmp_node.keyword
        if is_left:
            prev_node.left = tmp_node.left
        else:
            prev_node.right = tmp_node.left

    def __str__(self):
        return str(self._root_node)

    __repr__ = __str__


if __name__ == "__main__":
    bst = BinarySearchTree()
    print(bst)
    bst.add_keyword(100)
    bst.add_keyword(50)
    bst.add_keyword(120)
    bst.add_keyword(70)
    print(bst)
    print(bst.find_keyword(90) == None)
    print(bst.find_keyword(70))
    bst.delete_keyword(100)
    print(bst)
    bst.delete_keyword(50)
    print(bst)
    bst.delete_keyword(70)
    print(bst)
    bst.delete_keyword(120)
    print(bst)

