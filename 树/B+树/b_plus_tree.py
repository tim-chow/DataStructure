# coding: utf8

import math


def find_insertion_position(array, target):
    """
    利用二分查找寻找插入位置
    """
    low = 0
    high = len(array) - 1

    while low <= high:
        mid = (low + high) / 2
        if array[mid] == target:
            return mid - 1, mid
        if array[mid] > target:
            if mid == 0:
                return -1, 0
            if target > array[mid - 1]:
                return mid - 1, mid
            high = mid - 1
        else:
            if mid == len(array) - 1:
                return mid, mid + 1
            if target < array[mid + 1]:
                return mid, mid + 1
            low = mid + 1

    raise RuntimeError("unreachable")


class BaseNode(object):
    def __init__(self, keywords, parent):
        self.keywords = keywords
        self.parent = parent


class IndexNode(BaseNode):
    """
    索引节点
    """
    def __init__(self, keywords, children=None, parent=None):
        BaseNode.__init__(self, keywords, parent)
        self.children = children or []


class DataNode(BaseNode):
    """
    数据节点
    """
    def __init__(self, keywords, parent=None, next_node=None):
        BaseNode.__init__(self, keywords, parent)
        self.next_node = next_node


class BPlusTree(object):
    """
    B+ 树实现
    """
    def __init__(self, m):
        self.min_keywords = int(math.ceil(m / 2.0))
        self.max_keywords = m
        self._root = None
        self._data = None

    def insert(self, keyword):
        """
        插入关键字
        """
        # 如果树为空，那么创建根节点，初始时根节点只有一个关键字，且根节点是数据节点
        if self._root is None:
            self._root = self._data = DataNode([keyword])
            return

        node = self._root
        while True:
            pos = find_insertion_position(node.keywords, keyword)
            if isinstance(node, DataNode):
                node.keywords.insert(pos[1], keyword)

                # 回溯
                temp = node
                index = pos[1]
                while temp is not None and index == 0:
                    parent = temp.parent
                    if parent is None:
                        break
                    for index, child in enumerate(parent.children):
                        if child is temp:
                            break
                    parent.keywords[index] = keyword
                    temp = parent
                break

            if pos[0] == -1:
                child_index = 0
            elif pos[0] == len(node.keywords) - 1:
                child_index = len(node.children) - 1
            elif node.keywords[pos[1]] == keyword:
                child_index = pos[1]
            else:
                child_index = pos[0]
            node = node.children[child_index]

        while len(node.keywords) > self.max_keywords:
            mid = len(node.keywords) / 2
            if isinstance(node, DataNode):
                new_node = DataNode(node.keywords[mid:], node.parent, node.next_node)
                node.next_node = new_node
            else:
                new_node = IndexNode(node.keywords[mid:], node.children[mid:], node.parent)
                for child in new_node.children:
                    child.parent = new_node
                node.children = node.children[:mid]
            node.keywords = node.keywords[:mid]

            if node is self._root:
                self._root = IndexNode([node.keywords[0], new_node.keywords[0]], [node, new_node])
                node.parent = new_node.parent = self._root
                return

            parent = node.parent
            index = None
            for index, child in enumerate(parent.children):
                if child is node:
                    break
            parent.keywords.insert(index + 1, new_node.keywords[0])
            parent.children.insert(index + 1, new_node)

            node = parent

    def search(self, keyword):
        """
        搜索关键字
        """
        # 如果树为空，则搜索失败
        if self._root is None:
            raise KeyError()

        node = self._root
        while node is not None:
            pos = find_insertion_position(node.keywords, keyword)
            if isinstance(node, DataNode):
                if pos[0] == -1:
                    if node.keywords[0] == keyword:
                        return node, 0
                    raise KeyError()
                elif pos[1] == len(node.keywords):
                    if node.keywords[pos[0]] == keyword:
                        return node, pos[0]
                    raise KeyError()
                elif node.keywords[pos[1]] == keyword:
                    return node, pos[1]
                elif node.keywords[pos[0]] == keyword:
                    return node, pos[0]
                raise KeyError()

            if pos[0] == -1:
                if node.keywords[0] == keyword:
                    child_index = 0
                else:
                    raise KeyError()
            elif pos[1] == len(node.keywords):
                child_index = pos[0]
            elif node.keywords[pos[1]] == keyword:
                child_index = pos[1]
            else:
                child_index = pos[0]

            node = node.children[child_index]

    def delete(self, keyword):
        """
        删除关键字
        """
        node, index = self.search(keyword)
        assert isinstance(node, DataNode), "node must be DataNode"
        node.keywords.pop(index)

        if node is self._root:
            if len(node.keywords) == 0:
                self._root = None
                self._data = None
            return

        temp = node
        while index == 0:
            parent = temp.parent
            if parent is None:
                break
            for index, child in enumerate(parent.children):
                if child is temp:
                    break
            parent.keywords[index] = node.keywords[0]
            temp = parent

        while len(node.keywords) < self.min_keywords:
            parent = node.parent
            for index, child in enumerate(parent.children):
                if child is node:
                    break
            if index == 0:
                left_sibling = None
                right_sibling = None
                if len(parent.children) > 1:
                    right_sibling = parent.children[index + 1]
            elif index == len(parent.children) - 1:
                left_sibling = parent.children[index - 1]
                right_sibling = None
            else:
                left_sibling = parent.children[index - 1]
                right_sibling = parent.children[index + 1]

            # 尝试从左兄弟借一个关键字
            if left_sibling is not None and len(left_sibling.keywords) > self.min_keywords:
                borrowed_keyword = left_sibling.keywords.pop(-1)
                parent.keywords[index] = borrowed_keyword
                node.keywords.insert(0, borrowed_keyword)
                if isinstance(left_sibling, IndexNode):
                    borrowed_subtree = left_sibling.children.pop(-1)
                    node.children.insert(0, borrowed_subtree)
                    borrowed_subtree.parent = node
                break

            # 尝试从右兄弟借一个关键字
            if right_sibling is not None and len(right_sibling.keywords) > self.min_keywords:
                borrowed_keyword = right_sibling.keywords.pop(0)
                parent.keywords[index + 1] = right_sibling.keywords[0]
                node.keywords.append(borrowed_keyword)
                if isinstance(right_sibling, IndexNode):
                    borrowed_subtree = right_sibling.children.pop(0)
                    node.children.append(borrowed_subtree)
                    borrowed_subtree.parent = node
                break

            # 如果左兄弟非空，则与左兄弟合并
            if left_sibling is not None:
                parent.keywords.pop(index)
                parent.children.pop(index)
                for keyword in node.keywords:
                    left_sibling.keywords.append(keyword)
                if isinstance(node, IndexNode):
                    for child in node.children:
                        child.parent = left_sibling
                        left_sibling.children.append(child)
                else:
                    left_sibling.next_node = node.next_node
            # 如果右兄弟非空，则与右兄弟合并
            elif right_sibling is not None:
                parent.keywords.pop(index+1)
                parent.children.pop(index+1)
                for keyword in right_sibling.keywords:
                    node.keywords.append(keyword)
                if isinstance(node, IndexNode):
                    for child in right_sibling.children:
                        child.parent = node
                        node.children.append(child)
                else:
                    node.next_node = right_sibling.next_node
            # 如果节点既没有左兄弟，也没有右兄弟，说明其父节点只有一个关键字，其父节点只能是根节点
            else:
                assert parent is self._root, "parent must be root"
                self._root = node
                break

            if parent is self._root:
                break

            node = parent

    @property
    def root(self):
        return self._root

    @property
    def data(self):
        return self._data

    @staticmethod
    def is_valid_b_plus_tree(tree):
        if tree.root is None:
            if tree.data is not None:
                return False
            return True

        queue = [tree.root, None]
        current_data_node = tree.data
        while queue:
            node_type = None
            while True:
                node = queue.pop(0)
                if node is None:
                    break
                # 校验 node 的关键字数量
                if len(node.keywords) > tree.max_keywords:
                    return False
                if node is tree.root:
                    if len(node.keywords) < 1:
                        return False
                else:
                    if len(node.keywords) < tree.min_keywords:
                        return False
                # 校验 node 的关键字是否有序
                for ind in range(len(node.keywords) - 1):
                    if node.keywords[ind] > node.keywords[ind + 1]:
                        return False
                if isinstance(node, IndexNode):
                    if node_type is None:
                        node_type = IndexNode
                    else:
                        if not isinstance(node, node_type):
                            return False
                    # 校验孩子节点
                    if len(node.children) != len(node.keywords):
                        return False
                    for ind, child in enumerate(node.children):
                        if child.parent is not node:
                            return False
                        if len(child.keywords) == 0 or node.keywords[ind] != child.keywords[0]:
                            return False
                        queue.append(child)
                else:
                    if node_type is None:
                        node_type = DataNode
                    else:
                        if not isinstance(node, node_type):
                            return False
                    if node is not current_data_node:
                        return False
                    current_data_node = current_data_node.next_node
            if queue:
                queue.append(None)

        return True


def test():
    import random

    keywords = list(range(1000))
    tree = BPlusTree(random.randint(3, 20))
    for keyword in keywords:
        tree.insert(keyword)
        assert BPlusTree.is_valid_b_plus_tree(tree), "invalid b+ tree"

    random.shuffle(keywords)
    for keyword in keywords:
        node, index = tree.search(keyword)
        assert node.keywords[index] == keyword, "there are some bugs in search"

    random.shuffle(keywords)
    for keyword in keywords:
        tree.delete(keyword)
        try:
            tree.search(keyword)
            raise RuntimeError("there are some bugs in delete")
        except KeyError:
            pass
        assert BPlusTree.is_valid_b_plus_tree(tree), "invalid b+ tree"


if __name__ == "__main__":
    test()
