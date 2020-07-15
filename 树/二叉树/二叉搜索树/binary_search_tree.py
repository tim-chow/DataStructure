# coding: utf8


class Node(object):
    """
    二叉搜索树的节点
    """
    def __init__(self, keyword, left=None, right=None):
        self.keyword = keyword
        self.left = left
        self.right = right


class BinarySearchTree(object):
    """
    二叉搜索树实现
    """
    def __init__(self):
        self._root = None

    def insert(self, keyword):
        # 如果树为空，则创建新节点，并使之成为根节点
        if self._root is None:
            self._root = Node(keyword)
            return

        node = self._root
        while True:
            # 如果待插入关键字小于 node 的关键字
            if keyword < node.keyword:
                # 如果 node 的左子树为空，则创建新节点，并使之成为 node 的左孩子节点
                if node.left is None:
                    node.left = Node(keyword)
                    break
                # 否则，使用相同的方式在左子树上进行插入
                node = node.left
            # 如果待插入关键字不小于 node 的关键字
            else:
                # 如果 node 的右子树为空，则创建新节点，并使之成为 node 的右孩子节点
                if node.right is None:
                    node.right = Node(keyword)
                    break
                # 否则，使用相同的方式在右子树上进行插入
                node = node.right

    def search(self, keyword):
        node = self._root
        while node is not None:
            # 如果 node 的关键字等于待查询关键字，则搜索成功
            if keyword == node.keyword:
                return node
            # 如果待搜索关键字小于 node 的关键字，则使用相同的方式在左子树上进行查询
            if keyword < node.keyword:
                node = node.left
                continue
            # 否则，使用相同的方式在右子树上进行查询
            node = node.right
        return None

    def delete(self, keyword):
        node = self._root
        left = None
        parent = node
        while node is not None:
            if keyword == node.keyword:
                # 如果待删除节点是叶子节点
                if node.left is None and node.right is None:
                    # 如果待删除节点是根节点，那么将树置空
                    if node is self._root:
                        self._root = None
                    # 否则，将待删除节点的父节点的相应孩子节点置空
                    elif left:
                        parent.left = None
                    else:
                        parent.right = None
                # 如果待删除节点的左子树和右子树都不为空
                elif node.left is not None and node.right is not None:
                    # 找到左子树的最右节点（或者找到右子树的最左节点）
                    temp = node.left
                    parent = node
                    left = True
                    while temp.right is not None:
                        parent = temp
                        left = False
                        temp = temp.right
                    # 将待删除节点的关键字置为 temp 的关键字，然后将 temp 删掉
                    node.keyword = temp.keyword
                    # 因为 temp 的右子树肯定为空，所以将其左子树接到其父节点
                    if left:
                        parent.left = temp.left
                    else:
                        parent.right = temp.left
                # 如果待删除节点的左子树为空
                elif node.left is None:
                    # 如果待删除节点是根节点，则将根节点置为其右孩子节点
                    if node is self._root:
                        self._root = node.right
                    # 否则，将待删除节点的右孩子节点接到其父节点上
                    elif left:
                        parent.left = node.right
                    else:
                        parent.right = node.right
                # 如果待删除节点的右子树为空
                else:
                    # 如果待删除节点是根节点，则将根节点职位其左孩子节点
                    if node is self._root:
                        self._root = node.left
                    # 否则，将待删除节点的左孩子节点接到其父节点上
                    elif left:
                        parent.left = node.left
                    else:
                        parent.right = node.left
                return
            elif keyword < node.keyword:
                # 使用相同的方式，去左子树上进行删除
                parent = node
                left = True
                node = node.left
            else:
                # 使用相同的方式，去右子树上进行删除
                parent = node
                left = False
                node = node.right

        raise KeyError("not found")

    @property
    def root(self):
        return self._root


if __name__ == "__main__":
    import random
    elements = list(range(20))
    random.shuffle(elements)
    print("元素列表：")
    print(elements)

    print("插入元素")
    binary_search_tree = BinarySearchTree()
    for ind in elements:
        binary_search_tree.insert(ind)

    def inorder_traverse(root):
        if root is None:
            return []

        nodes = []
        nodes.extend(inorder_traverse(root.left))
        nodes.append(root.keyword)
        nodes.extend(inorder_traverse(root.right))

        return nodes

    print("中序遍历：")
    print(inorder_traverse(binary_search_tree.root))

    for ind in elements:
        assert binary_search_tree.search(ind) is not None

    print("删除元素")
    for ind in elements:
        binary_search_tree.delete(ind)

    assert binary_search_tree.root is None
