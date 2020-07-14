# coding: utf8


class Node(object):
    def __init__(self, element=None, next_node=None):
        self.element = element
        self.next_node = next_node


def get_middle_node(linked_list):
    if linked_list is None:
        return None

    # 快指针每次前进 2 步，慢指针每次前进 1 步，当快指针到头时，慢指针到达中间节点
    slow = fast = linked_list
    while fast is not None:
        fast = fast.next_node
        if fast is not None:
            fast = fast.next_node
            slow = slow.next_node

    return slow


def get_last_node(linked_list, k):
    slow = fast = linked_list

    # 快指针先前进 k - 1 步
    for _ in range(k):
        if fast is None:
            return linked_list
        fast = fast.next_node

    # 然后慢指针开始出发
    while fast is not None:
        slow = slow.next_node
        fast = fast.next_node

    return slow


if __name__ == "__main__":
    import unittest

    class SlowFastPointerTest(unittest.TestCase):
        def setUp(self):
            nodes = [Node(ind) for ind in range(100)]
            for ind in range(99):
                nodes[ind].next_node = nodes[ind + 1]
            self.node = nodes[0]
            self.middle_node = nodes[50]
            self.last_1st_node = nodes[99]
            self.last_3rd_node = nodes[97]
            self.last_100th_node = nodes[0]
            del nodes

        def testGetMiddleNode(self):
            self.assertIs(get_middle_node(self.node), self.middle_node)

        def testGetLastNode(self):
            self.assertIs(get_last_node(self.node, 1), self.last_1st_node)
            self.assertIs(get_last_node(self.node, 3), self.last_3rd_node)
            self.assertIs(get_last_node(self.node, 100), self.last_100th_node)
    unittest.main()
