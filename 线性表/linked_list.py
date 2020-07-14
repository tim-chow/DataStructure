# coding: utf8


class LinkedList(object):
    """
    单链表实现
    """
    class Node(object):
        def __init__(self, element, next_node=None):
            self._element = element
            self._next_node = next_node

        @property
        def element(self):
            return self._element

        @element.setter
        def element(self, element):
            self._element = element

        @property
        def next_node(self):
            return self._next_node

        @next_node.setter
        def next_node(self, next_node):
            self._next_node = next_node

    def __init__(self):
        # 头结点
        self._head = self.Node(None, None)
        # 元素数量
        self._size = 0

    def insert(self, index, element):
        # 先找到待插入节点的前一个节点，然后在其后插入新节点
        node = self._head
        cursor = -1
        while node is not None:
            if cursor == index - 1:
                # 插入新节点
                new_node = self.Node(element)
                new_node.next_node = node.next_node
                node.next_node = new_node
                break
            node = node.next_node
            cursor = cursor + 1
        else:
            raise IndexError("invalid index")

    def delete(self, element):
        # 先找到待删除节点的前一个节点，然后删除节点
        node = self._head
        while node.next_node is not None:
            if node.next_node.element == element:
                node.next_node = node.next_node.next_node
                break
            node = node.next_node
        else:
            raise ValueError("not found")

    def find(self, element):
        cursor = 0
        node = self._head.next_node

        while node is not None:
            if node.element == element:
                return cursor
            node = node.next_node
            cursor = cursor + 1
        else:
            raise ValueError("not found")


if __name__ == "__main__":
    import unittest

    class LinkedListTest(unittest.TestCase):
        def testLinkedList(self):
            linked_list = LinkedList()
            linked_list.insert(0, 0)
            self.assertEqual(linked_list.find(0), 0)
            linked_list.insert(0, 1)
            self.assertEqual(linked_list.find(1), 0)
            self.assertEqual(linked_list.find(0), 1)
            linked_list.insert(2, 2)
            self.assertEqual(linked_list.find(2), 2)
            linked_list.delete(1)
            self.assertEqual(linked_list.find(2), 1)
            self.assertRaises(ValueError, linked_list.delete, 3)
            self.assertRaises(ValueError, linked_list.find, 3)
