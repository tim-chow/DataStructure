class Node(object):
    def __init__(self, element=None, next=None):
        self.element = element
        self.next = next

    def __str__(self):
        return "Node{element=%s, next=%s}" % (
            self.element, self.next)


def reverse_list(first_node):
    prev_node = None
    tmp_node = first_node
    while tmp_node != None:
        p = tmp_node.next
        tmp_node.next = prev_node
        prev_node = tmp_node
        tmp_node = p
    return prev_node


if __name__ == "__main__":
    node1 = Node(1)
    node1.next = node2 = Node(2)
    node2.next = node3 = Node(3)
    print(node1)
    node = reverse_list(node1)
    print(node)
