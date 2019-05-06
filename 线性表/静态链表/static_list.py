# coding: utf8

class Node(object):
    def __init__(self, element=None, cursor=-1):
        self.element = element
        self.cursor = cursor

    def __str__(self):
        return "Node{element=%s, cursor=%d}" % (
            self.element, self.cursor)


class StaticList(object):
    def __init__(self, max_size):
        self.free_space = Node()
        self.head = Node()
        self.max_size = max_size
        self.underlying_array = [Node(None, -1) for _ in range(max_size)]

        self.free_space.cursor = 0
        for ind in range(0, max_size-1):
            self.underlying_array[ind].cursor = ind + 1

    def _malloc(self):
        cursor = self.free_space.cursor
        if cursor == -1:
            raise RuntimeError("no space left on static list")
        node = self.underlying_array[cursor]
        self.free_space.cursor = node.cursor
        return cursor

    def _free(self, cursor):
        node = self.underlying_array[cursor]
        node.cursor = self.free_space.cursor
        self.free_space.cursor = cursor

    def _get(self, index):
        tmp = self.head
        for _ in range(index):
            if tmp.cursor == -1:
                return -1
            tmp = self.underlying_array[tmp.cursor]
        return tmp.cursor

    def insert_after(self, index, element):
        node = self.head
        if index >= 0:
            cursor = self._get(index)
            if cursor == -1:
                raise RuntimeError("invalid index")
            node = self.underlying_array[cursor]
        free_cursor = self._malloc()
        free_node = self.underlying_array[free_cursor]
        free_node.element = element
        free_node.cursor = node.cursor
        node.cursor = free_cursor

    def remove(self, index):
        # 找到待删除节点的前一个节点
        prev_cursor = self._get(index-1)
        if prev_cursor == -1:
            raise RuntimeError("invalid index")
        prev_node = self.underlying_array[prev_cursor]
        if prev_node.cursor == -1:
            raise RuntimeError("invalid index")
        node_cursor = prev_node.cursor
        node = self.underlying_array[node_cursor]

        prev_node.cursor = node.cursor

        # 将待删除节点放回备用节点链表
        self._free(node_cursor)

        return node.element

    def __str__(self):
        result = "underlying array:\n%s" % \
            "\n".join(map(lambda node: "    %s" % node,
                self.underlying_array))
        result = result + "\n" + "Head: %s" % self.head
        result = result + "\n" + "Free Space: %s" % self.free_space
        return result

if __name__ == "__main__":
    static_list = StaticList(5)
    static_list.insert_after(-1, 1)
    static_list.insert_after(0, 2)
    static_list.insert_after(1, 3)
    static_list.insert_after(2, 4)
    static_list.insert_after(3, 5)
    print(static_list)
    print(static_list.remove(2))
    print(static_list)
    static_list.insert_after(3, 6)
    print(static_list)
    print(static_list.remove(4))
    print(static_list)
    print(static_list.remove(3))
    print(static_list)
