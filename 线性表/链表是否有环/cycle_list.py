class Node(object):
    def __init__(self, element=None, next=None):
        self.element = element
        self.next = next

    def __str__(self):
        return "Node[element={0.element}]".format(self)

def has_cycle(linked_list):
    fast = slow = linked_list
    while fast != None:
        fast = fast.next
        if fast != None:
            fast = fast.next
            slow = slow.next
            if fast == slow:
                return True
    return False

def cycle_length(linked_list):
    fast = slow = linked_list
    meet_count = 0
    loop_count = 0
    while fast != None:
        fast = fast.next
        if fast != None:
            loop_count = loop_count + 1
            fast = fast.next
            slow = slow.next
            if fast == slow:
                meet_count = meet_count + 1
                if meet_count == 1:
                    loop_count = 0
                else:
                    return loop_count
    return -1

def joint_node(linked_list):
    fast = slow = linked_list
    meet_node = None
    while fast != None:
        fast = fast.next
        if fast != None:
            fast = fast.next
            slow = slow.next
            if fast == slow:
                meet_node = fast
                break
    if meet_node is None:
        raise RuntimeError("no cycle in linked list")

    p = linked_list
    while p != meet_node:
        p = p.next
        meet_node = meet_node.next
    return p

if __name__ == "__main__":
    node1 = Node(1)
    node1.next = node2 = Node(2)
    node2.next = node3 = Node(3)
    node3.next = node4 = Node(4)
    node4.next = node3
    print(has_cycle(node1))
    print(cycle_length(node1))
    print(joint_node(node1))
