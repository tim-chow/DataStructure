# coding: utf8


class Node(object):
    def __init__(self, key, prev_node=None, next_node=None):
        self.key = key
        self.prev_node = prev_node
        self.next_node = next_node


def partition(linked_list):
    if linked_list.next_node is None:
        return None, linked_list, None

    left = None
    temp = linked_list.next_node
    while temp is not None:
        if temp.key >= linked_list.key:
            temp = temp.next_node
            continue

        # 把 temp 移到 left
        prev_node = temp.prev_node
        next_node = temp.next_node
        prev_node.next_node = next_node
        if next_node is not None:
            next_node.prev_node = prev_node

        if left is None:
            left = temp
            left.prev_node = None
            left.next_node = None
        else:
            left_next = left.next_node
            if left_next is not None:
                left_next.prev_node = temp
            left.next_node = temp
            temp.prev_node = left
            temp.next_node = left_next

        temp = next_node

    right = linked_list.next_node
    if right is not None:
        right.prev_node = None

    linked_list.next_node = None

    return left, linked_list, right


def print_linked_list(linked_list):
    if linked_list is None:
        return
    temp = linked_list
    keys = []
    while temp is not None:
        keys.append(temp.key)
        temp = temp.next_node
    print(" ".join(map(str, keys)))


def quick_sort(linked_list):
    if linked_list is None or linked_list.next_node is None:
        return linked_list

    left, linked_list, right = partition(linked_list)

    if left is not None:
        left = quick_sort(left)
    if right is not None:
        right = quick_sort(right)

    head = linked_list
    if left is not None:
        head = left
        while left.next_node is not None:
            left = left.next_node
        left.next_node = linked_list
    linked_list.prev_node = left
    linked_list.next_node = right
    if right is not None:
        right.prev_node = linked_list

    return head


def check_sorted_linked_list(linked_list):
    p1 = linked_list
    while p1 is not None and p1.next_node is not None:
        p2 = p1.next_node
        if p1.key > p2.key:
            return False
        p1 = p2
    return True


def test():
    import random

    # 元素数量
    N = 100

    elements = range(N)
    # 将元素打乱
    random.shuffle(elements)

    # 生成链表
    nodes = []
    for element in elements:
        nodes.append(Node(element))
    for ind in range(N - 1):
        nodes[ind].next_node = nodes[ind + 1]
        nodes[ind + 1].prev_node = nodes[ind]
    linked_list = nodes[0]
    del nodes

    head = quick_sort(linked_list)
    assert check_sorted_linked_list(head)


if __name__ == "__main__":
    for i in range(20):
        test()
