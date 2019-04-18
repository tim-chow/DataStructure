# coding: utf8

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

    def __str__(self):
        return "ListNode{val=%s, next=%s}" % (self.val, self.next)

    def __repr__(self):
        return self.__str__() + "@" + hex(id(self))


class Solution(object):
    def sortList(self, head):
        if head == None or head.next == None:
            return head

        mid = head
        tail = head
        while tail.next != None:
            tail = tail.next
            if tail.next != None:
                tail = tail.next
                mid = mid.next

        right = mid.next
        mid.next = None

        head1 = self.sortList(head)
        head2 = self.sortList(right)
        return self._merge(head1, head2).next

    def _merge(self, l1, l2):
        head = ListNode(None)
        tail = head
        x = l1
        y = l2

        while x != None and y != None:
            if x.val < y.val:
                tail.next = x
                tail = x
                x = x.next
            else:
                tail.next = y
                tail = y
                y = y.next

        if x != None:
            tail.next = x
        if y != None:
            tail.next = y

        return head


if __name__ == "__main__":
    tmp = None
    head = None
    for element in [4, 2, 1, 3]:
        node = ListNode(element)
        if head == None:
            head = node
            tmp = head
        else:
            tmp.next = node
            tmp = node

    head = Solution().sortList(head)
    tmp = head
    while tmp != None:
        print(tmp)
        tmp = tmp.next
