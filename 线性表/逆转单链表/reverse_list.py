# coding: utf8


class Node(object):
    def __init__(self, element=None, next_node=None):
        self.element = element
        self.next_node = next_node


def reverse_list(node):
    if node is None:
        return node

    p1 = node
    p2 = p1.next_node
    p1.next_node = None

    while p2 is not None:
        p3 = p2.next_node
        p2.next_node = p1
        p1 = p2
        p2 = p3

    return p1


if __name__ == "__main__":
    import unittest

    class TestReverseList(unittest.TestCase):
        def testReverseList(self):
            nodes = [Node(ind, None) for ind in range(10)]
            for ind in range(9):
                nodes[ind].next_node = nodes[ind + 1]
            node = nodes[0]
            del nodes

            temp = node
            while temp is not None:
                print(temp.element)
                temp = temp.next_node

            print("=" * 10)

            head = reverse_list(node)
            temp = head
            while temp is not None:
                print(temp.element)
                temp = temp.next_node

    unittest.main()
