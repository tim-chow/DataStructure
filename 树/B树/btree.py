# coding: utf8

import math


def find_insertion_position(array, target):
    """
    寻找插入位置
    """
    low = 0
    high = len(array) - 1

    if target <= array[0]:
        return -1, 0
    if target >= array[high]:
        return high, high + 1

    while low <= high:
        mid = (low + high) / 2
        if target == array[mid]:
            return mid - 1, mid
        elif target < array[mid]:
            if target >= array[mid - 1]:
                return mid - 1, mid
            high = mid - 1
        else:
            if target <= array[mid + 1]:
                return mid, mid + 1
            low = mid + 1

    raise RuntimeError("unreachable")


class Node(object):
    """
    B 树的节点
    """
    def __init__(self, keywords, children=None):
        self.keywords = keywords
        # children 为 None 表示节点是根节点
        self.children = children
        self.parent = None


class BTree(object):
    """
    B 树实现
    """
    def __init__(self, m):
        # B 树的阶数
        self.m = m
        # 树根
        self._root = None

    def insert(self, keyword):
        """
        插入关键字
        """
        # 如果树为空，那么创建根节点，初始时根节点只包含一个关键字
        if self._root is None:
            self._root = Node([keyword])
            return

        # 在叶子节点上插入关键字
        node = self._root
        while True:
            pos = find_insertion_position(node.keywords, keyword)
            if node.children is not None:
                node = node.children[pos[1]]
            else:
                node.keywords.insert(pos[1], keyword)
                break

        # 如果节点的关键字个数超过 max keywords，则分裂
        while len(node.keywords) > self.max_keywords:
            mid = self.m / 2
            mid_keyword = node.keywords[mid]

            # 在 mid 处，将节点一分为二
            new_node = Node(node.keywords[mid + 1:])
            if node.children is not None:
                new_node.children = node.children[mid + 1:]
                # 重置孩子节点的双亲节点
                for child in new_node.children:
                    child.parent = new_node
            node.keywords = node.keywords[:mid]
            if node.children is not None:
                node.children = node.children[:mid + 1]

            # 如果分裂的是根节点，那么将树增高一层
            if node is self._root:
                self._root = Node([mid_keyword], [node, new_node])
                node.parent = self._root
                new_node.parent = self._root
                break

            parent = node.parent
            index = None
            # TODO: 当前的实现的时间复杂度是 O(m)
            for index, child in enumerate(parent.children):
                if node is child:
                    break
            # 在父节点上插入关键字和新子树
            parent.keywords.insert(index, mid_keyword)
            parent.children.insert(index + 1, new_node)

            # 设置新节点的父节点
            new_node.parent = parent

            # 从父节点开始，向上回溯
            node = parent

    def search(self, keyword):
        """
        搜索关键字
        """
        if self._root is None:
            raise KeyError(keyword)

        node = self._root
        while True:
            pos = find_insertion_position(node.keywords, keyword)
            if pos[0] == -1:
                if keyword == node.keywords[0]:
                    return node, 0
            elif pos[1] == len(node.keywords):
                if keyword == node.keywords[-1]:
                    return node, pos[1] - 1
            elif node.keywords[pos[0]] == keyword:
                return node, pos[0]
            elif node.keywords[pos[1]] == keyword:
                return node, pos[1]
            if node.children is None:
                raise KeyError(keyword)
            node = node.children[pos[1]]

    @property
    def max_keywords(self):
        return self.m - 1

    @property
    def min_keywords(self):
        return int(math.ceil(self.m / 2.0) - 1)

    def delete(self, keyword):
        """
        删除元素
        """
        # 找到待删除元素
        deleted_node, deleted_index = self.search(keyword)

        # 使用 deleted_node.children[deleted_index + 1] 的最左关键字代替待被删除的关键字或
        # 使用 deleted_node.children[deleted_index] 的最右关键字代替待被删除的关键字
        node = deleted_node
        index = deleted_index
        if deleted_node.children is not None:
            node = deleted_node.children[deleted_index + 1]
            index = 0
            while node.children is not None:
                node = node.children[0]
        deleted_node.keywords[deleted_index] = node.keywords[index]

        # node 一定是叶子节点，将关键字从叶子节点移除
        node.keywords.pop(index)

        # 如果 node 是根节点，
        if node is self._root:
            # 并且 node 中本来只有一个元素，那么将树置空
            if len(node.keywords) == 0:
                self._root = None
            # 否则，直接退出，因为根节点没最少关键字个数的限制
            return

        # 如果节点的关键字个数不满于要求，那么需要进行调整
        while len(node.keywords) < self.min_keywords:
            # 找到父节点、左兄弟、右兄弟
            parent = node.parent
            for index, child in enumerate(parent.children):
                if node is child:
                    break
            if index == 0:
                left_sibling = None
                right_sibling = parent.children[index + 1]
            elif index == len(parent.children) - 1:
                left_sibling = parent.children[index - 1]
                right_sibling = None
            else:
                left_sibling = parent.children[index - 1]
                right_sibling = parent.children[index + 1]

            # 尝试从左兄弟借一个节点
            if left_sibling is not None and len(left_sibling.keywords) > self.min_keywords:
                borrowed_keyword = left_sibling.keywords.pop(-1)
                # 需要通过父节点进行中转
                node.keywords.insert(0, parent.keywords[index - 1])
                parent.keywords[index - 1] = borrowed_keyword

                if left_sibling.children is not None:
                    borrowed_subtree = left_sibling.children.pop(-1)
                    node.children.insert(0, borrowed_subtree)
                    borrowed_subtree.parent = node
                break

            # 尝试从右兄弟借一个节点
            if right_sibling is not None and len(right_sibling.keywords) > self.min_keywords:
                borrowed_keyword = right_sibling.keywords.pop(0)
                # 需要通过父节点进行中转
                node.keywords.append(parent.keywords[index])
                parent.keywords[index] = borrowed_keyword

                if right_sibling.children is not None:
                    borrowed_subtree = right_sibling.children.pop(0)
                    node.children.append(borrowed_subtree)
                    borrowed_subtree.parent = node
                break

            # 如果有左兄弟，则与父节点、左兄弟进行三方合并
            if left_sibling is not None:
                left_sibling.keywords.append(parent.keywords[index - 1])
                left_sibling.keywords.extend(node.keywords)
                parent.keywords.pop(index - 1)
                parent.children.pop(index)
                if node.children is not None:
                    for child in node.children:
                        child.parent = left_sibling
                        left_sibling.children.append(child)
                maybe_new_root = left_sibling
            # 如果有右兄弟，那么与父节点、右兄弟进行三方合并
            elif right_sibling is not None:
                node.keywords.append(parent.keywords[index])
                node.keywords.extend(right_sibling.keywords)
                parent.keywords.pop(index)
                parent.children.pop(index + 1)
                if right_sibling.children is not None:
                    for child in right_sibling.children:
                        child.parent = node
                        node.children.append(child)
                maybe_new_root = node
            else:
                raise RuntimeError("unreachable")

            # 如果 parent 是父节点，
            if parent is self._root:
                # 并且合并后，没有关键字了，那么树的高度将降低 1
                if len(parent.keywords) == 0:
                    self._root = maybe_new_root
                # 否则，直接退出即可，因为根节点没有最少关键字个数的限制
                break

            # 否则从 parent 开始继续向上调整
            node = parent


def test():
    import random

    tree = BTree(5)
    keywords = list(range(100000))
    random.shuffle(keywords)

    # 插入元素
    for keyword in keywords:
        tree.insert(keyword)

    # 搜索元素
    random.shuffle(keywords)
    for keyword in keywords:
        node, index = tree.search(keyword)
        assert node.keywords[index] == keyword

    random.shuffle(keywords)
    for keyword in keywords:
        tree.delete(keyword)
        try:
            tree.search(keyword)
            raise RuntimeError("delete %s failed" % keyword)
        except KeyError:
            pass


if __name__ == "__main__":
    test()
