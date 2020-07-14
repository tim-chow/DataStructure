# coding: utf8


class Node(object):
    def __init__(self, element=None, next_node=None):
        self.element = element
        self.next_node = next_node


def has_cycle(node):
    """判断单链表是否有环"""
    if node is None:
        return False

    slow = fast = node
    while fast is not None:
        # 快指针先前进一步
        fast = fast.next_node
        if fast is not None:
            # 快指针再前进一步
            fast = fast.next_node
            # 慢指针前进一步
            slow = slow.next_node

            # 快慢指针相遇表示有环
            if slow is fast:
                return True
    return False


def get_cycle_length(node):
    """获取环的长度"""
    if node is None:
        return 0

    slow = fast = node
    meet_count = 0
    loop_count = 0
    while fast is not None:
        fast = fast.next_node
        if fast is not None:
            fast = fast.next_node
            slow = slow.next_node
            loop_count = loop_count + 1
            if slow is fast:
                meet_count = meet_count + 1
                if meet_count == 1:
                    # 快慢指针第一次相遇
                    loop_count = 0
                elif meet_count == 2:
                    # 快慢指针再次相遇时，慢指针走的步数就是环长
                    return loop_count
    return 0


def get_joint_node(node):
    if node is None:
        return None

    slow = fast = node
    while fast is not None:
        fast = fast.next_node
        if fast is not None:
            fast = fast.next_node
            slow = slow.next_node
            if slow is fast:
                p1 = slow
                p2 = node
                while p1 is not p2:
                    p1 = p1.next_node
                    p2 = p2.next_node
                return p1

    return None


if __name__ == "__main__":
    import unittest

    class CycleListTest(unittest.TestCase):
        def setUp(self):
            # 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 2
            nodes = [Node(ind) for ind in range(6)]
            for ind in range(5):
                nodes[ind].next_node = nodes[ind + 1]
            nodes[5].next_node = nodes[2]
            self.node = nodes[0]
            # 连接点
            self.joint_node = nodes[2]

        def testCycleList(self):
            self.assertTrue(has_cycle(self.node))
            self.assertEqual(get_cycle_length(self.node), 4)
            self.assertIs(get_joint_node(self.node), self.joint_node)

    unittest.main()
