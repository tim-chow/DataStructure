# coding: utf8


class Node(object):
    """
    静态链表的节点
    """
    def __init__(self, element, cursor=-1):
        # 保存数据元素
        self.element = element
        # 保存直接后继节点在数组中的索引
        self.cursor = cursor


class StaticList(object):
    """
    静态链表
    """
    def __init__(self, max_size):
        # 备用链表的头节点
        self._free_space = Node(None, -1)
        # 静态链表的头节点
        self._head = Node(None, -1)
        # 底层数组
        self._underlying_array = [Node(None, -1) for _ in range(max_size)]

        # 将数组中的全部节点组织进备用链表
        self._free_space.cursor = 0
        for ind in range(0, max_size - 1):
            self._underlying_array[ind].cursor = ind + 1

    def _malloc(self):
        """
        用于从备用链表中申请节点
        """
        cursor = self._free_space.cursor
        if cursor == -1:
            raise RuntimeError("no space left")
        node = self._underlying_array[cursor]
        self._free_space.cursor = node.cursor
        return cursor

    def _free(self, cursor):
        """
        将节点放回备用链表
        """
        node = self._underlying_array[cursor]
        node.cursor = self._free_space.cursor
        self._free_space.cursor = cursor

    def insert(self, index, element):
        node = self._head
        current_index = -1

        while node is not None:
            if current_index == index - 1:
                # 申请新节点
                free_cursor = self._malloc()
                free_node = self._underlying_array[free_cursor]
                free_node.element = element
                free_node.cursor = node.cursor
                node.cursor = free_cursor
                break

            if node.cursor == -1:
                node = None
                continue

            node = self._underlying_array[node.cursor]
            current_index = current_index + 1
        else:
            raise IndexError("invalid index")

    def find(self, element):
        temp = self._head.cursor
        index = 0

        while temp != -1:
            node = self._underlying_array[temp]
            if node.element == element:
                return index
            temp = node.cursor
            index = index + 1
        else:
            raise ValueError("not found")

    def delete(self, element):
        # node 是待删除节点的前一个节点
        node = self._head
        if node.cursor == -1:
            next_node = None
        else:
            next_node = self._underlying_array[node.cursor]

        while next_node is not None:
            if next_node.element == element:
                next_node_cursor = next_node.cursor
                # 释放节点
                self._free(node.cursor)
                # 删除节点
                node.cursor = next_node_cursor
                break
            node = next_node
            if node.cursor == -1:
                next_node = None
            else:
                next_node = self._underlying_array[node.cursor]
        else:
            raise ValueError("not found")


if __name__ == "__main__":
    import unittest

    class TestStaticList(unittest.TestCase):
        def testStaticList(self):
            static_list = StaticList(5)
            static_list.insert(0, 1)
            static_list.insert(0, 0)
            static_list.insert(2, 2)
            self.assertRaises(IndexError, static_list.insert, 4, 4)
            self.assertRaises(ValueError, static_list.delete, 4)

            self.assertEqual(static_list.find(0), 0)
            self.assertEqual(static_list.find(1), 1)
            self.assertEqual(static_list.find(2), 2)
            self.assertRaises(ValueError, static_list.find, -1)

            static_list.delete(1)
            self.assertEqual(static_list.find(2), 1)
            static_list.delete(0)
            self.assertEqual(static_list.find(2), 0)

    unittest.main()
