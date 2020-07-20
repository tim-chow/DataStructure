# coding: utf8

import random


class Node(object):
    """
    跳表节点
    """
    def __init__(self, keyword, next_node=None, down_node=None):
        self.keyword = keyword
        self.next_node = next_node
        self.down_node = down_node


class SkipList(object):
    """
    跳表实现
    """
    def __init__(self, probability=0.25, max_levels=10):
        self._probability = probability
        self._max_levels = max_levels
        self._heads = [Node(None)]

    @property
    def heads(self):
        return self._heads

    def insert(self, keyword):
        # 确定在第几层进行插入
        k = 1
        for _ in range(len(self._heads)):
            if random.random() <= self._probability:
                k = k + 1
            else:
                break

        if k > self._max_levels:
            k = self._max_levels

        if k == len(self._heads) + 1:
            new_head = Node(None)
            new_head.down_node = self._heads[-1]
            self._heads.append(new_head)

        node = self._heads[k - 1]
        prev = None

        while node is not None:
            # 找到插入位置
            while node.next_node is not None and node.next_node.keyword < keyword:
                node = node.next_node
            # 插入新节点
            new_node = Node(keyword)
            new_node.next_node = node.next_node
            node.next_node = new_node
            if prev is not None:
                prev.down_node = new_node
            prev = new_node
            # 在下一层上继续插入
            node = node.down_node

    def search(self, keyword):
        node = self._heads[-1]
        while node is not None:
            while node.next_node is not None and node.next_node.keyword < keyword:
                node = node.next_node

            if node.next_node is not None and node.next_node.keyword == keyword:
                node = node.next_node
                while node.down_node is not None:
                    node = node.down_node
                return node
            node = node.down_node
        return None

    def delete(self, keyword):
        node = self._heads[-1]
        while node is not None:
            while node.next_node is not None and node.next_node.keyword < keyword:
                node = node.next_node
            if node.next_node is not None and node.next_node.keyword == keyword:
                node.next_node = node.next_node.next_node
            node = node.down_node
        # 将空层的头节点删掉
        while len(self._heads) > 1:
            if self._heads[-1].next_node is not None:
                break
            self._heads.pop(-1)


def print_skip_list(skip_list):
    """
    以易于阅读的形式打印跳表对象
    """
    for ind, node in enumerate(skip_list.heads[::-1]):
        keywords = []
        while node.next_node is not None:
            keywords.append(node.next_node.keyword)
            node = node.next_node
        print("level %d" % (len(skip_list.heads) - ind))
        print("\t" + " ".join(map(lambda k: str(k), keywords)))


if __name__ == "__main__":
    import unittest

    class SkipListTest(unittest.TestCase):
        def testSkipList(self):
            keywords = list(range(40))
            random.shuffle(keywords)
            skip_list = SkipList()
            for keyword in keywords:
                skip_list.insert(keyword)
            random.shuffle(keywords)
            for keyword in keywords:
                node = skip_list.search(keyword)
                self.assertIsNotNone(node)
                self.assertEqual(node.keyword, keyword)
            random.shuffle(keywords)
            for keyword in keywords:
                skip_list.delete(keyword)
                self.assertIsNone(skip_list.search(keyword))

    unittest.main()
