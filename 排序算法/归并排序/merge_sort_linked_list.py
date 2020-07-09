# coding: utf8


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

    def __str__(self):
        return "%s{val=%s, next=%s}" % (
            self.__class__.__name__,
            self.val,
            self.next.val if self.next is not None else self.next
        )

    def __repr__(self):
        return self.__str__() + "@" + hex(id(self))


class Solution(object):
    def sort(self, h):
        # 如果 h 中没有元素 或 只有一个元素，则其直接有序，立刻返回
        if h is None or h.next is None:
            return h

        # 通过快慢指针，找到链表的中间节点
        tail = h
        mid = h
        while tail.next is not None:
            # tail 先前进一步
            tail = tail.next

            # 如果未到尾部，tail 再前进一步，mid 前进一步
            if tail.next is not None:
                tail = tail.next
                mid = mid.next

            # 每次循环 tail 前进两步，mid 前进一步，所以当 tail 到达尾部时，
            # mid 到达链表的中间位置

        # 将列表从中间分成两个：head、right
        right = mid.next
        mid.next = None

        # 使用归并排序分别对着两个列表进行排序
        l1 = self.sort(h)
        l2 = self.sort(right)

        # 归并两个有序链表
        return self.merge(l1, l2)

    @staticmethod
    def merge(l1, l2):
        """将两个有序链表归并成一个有序列表"""
        if l1 is l2:
            return l1

        # h 是头节点
        h = ListNode(None)

        tail = h
        x = l1
        y = l2

        while x is not None and y is not None:
            if x.val <= y.val:
                tail.next = x
                tail = x
                x = x.next
            else:
                tail.next = y
                tail = y
                y = y.next

        if x is not None:
            tail.next = x
        elif y is not None:
            tail.next = y

        return h.next


if __name__ == "__main__":
    import random

    elements = list(range(-10, 11))
    random.shuffle(elements)
    print(elements)

    # 生成一个无序链表
    temp1 = None
    head = None
    for element in elements:
        node = ListNode(element)
        if head is None:
            head = node
            temp1 = node
        else:
            temp1.next = node
            temp1 = node

    new_head = Solution().sort(head)
    temp2 = new_head
    while temp2 is not None:
        print(temp2.val)
        temp2 = temp2.next
