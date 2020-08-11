# coding: utf8

"""
有向网实现
"""

from abc import ABCMeta, abstractmethod


class BaseDiGraph(object):
    """
    抽象基类
    """
    __metaclass__ = ABCMeta

    def dfs(self):
        """深度优先遍历"""
        index_list = []
        stack = [0]
        status = [0 for _ in range(self.get_vertex_count())]
        visited = [False for _ in range(self.get_vertex_count())]

        while stack:
            top = stack[-1]
            if not visited[top]:
                visited[top] = True
                index_list.append(top)

            adjacent_index = self.get_adjacent(top, status[top])
            if adjacent_index is None:
                stack.pop(-1)
                continue
            status[top] = status[top] + 1
            stack.append(adjacent_index)
        return index_list

    def bfs(self):
        """
        广度优先遍历
        """
        index_list = []
        queue = [0]
        visited = [False for _ in range(self.get_vertex_count())]

        while queue:
            vertex = queue.pop(0)
            if visited[vertex]:
                continue
            visited[vertex] = True
            index_list.append(vertex)
            queue.extend(list(self.get_adjacents(vertex)))
        return index_list

    @abstractmethod
    def get_adjacent(self, index, offset):
        pass

    @abstractmethod
    def get_adjacents(self, index):
        pass

    @abstractmethod
    def get_vertex_count(self):
        pass


class HeadNode(object):
    """
    头节点
    """
    def __init__(self, element):
        self._element = element
        self._next = None

    def set_element(self, element):
        self._element = element

    def get_element(self):
        return self._element

    def set_next(self, next):
        self._next = next

    def get_next(self):
        return self._next


class AdjacentNode(object):
    """
    表节点
    """
    def __init__(self, index, weight):
        self._index = index
        self._weight = weight
        self._next = None

    def set_index(self, index):
        self._index = index

    def get_index(self):
        return self._index

    def set_weight(self, weight):
        self._weight = weight

    def get_weight(self):
        return self._weight

    def set_next(self, next):
        self._next = next

    def get_next(self):
        return self._next


class DiNetworkAdjacent(BaseDiGraph):
    """
    有向网的邻接表表示
    """
    def __init__(self):
        self._vertex_array = []

    def add_vertex(self, element):
        self._vertex_array.append(HeadNode(element))

    def set_vertex(self, index, element):
        self._vertex_array[index].set_element(element)

    def get_vertex(self, index):
        return self._vertex_array[index]

    def add_arch(self, tail, head, weight):
        node = self._vertex_array[tail]

        while node.get_next() is not None:
            next_node = node.get_next()
            if next_node.get_index() == head:
                next_node.set_weight(weight)
                return
            node = next_node
        node.set_next(AdjacentNode(head, weight))

    def delete_vertex(self, index):
        self._vertex_array.pop(index)
        for head_node in self._vertex_array:
            prev = head_node
            node = head_node.get_next()
            while node is not None:
                if node.get_index() == index:
                    prev.set_next(node.get_next())
                    node = prev.get_next()
                    continue
                elif node.get_index() > index:
                    node.set_index(node.get_index() - 1)
                prev = node
                node = prev.get_next()

    def delete_arch(self, tail, head):
        prev = self._vertex_array[tail]
        node = prev.get_next()
        while node is not None:
            if node.get_index() == head:
                prev.set_next(node.get_next())
                break
            prev = node
            node = prev.get_next()

    def get_adjacent(self, index, offset):
        node = self._vertex_array[index]
        for ind in range(offset + 1):
            node = node.get_next()
            if node is None:
                break
            if ind == offset:
                return node.get_index()
        return None

    def get_adjacents(self, index, return_node=False):
        adjacents = []
        node = self._vertex_array[index].get_next()
        while node is not None:
            adjacents.append(node if return_node else node.get_index())
            node = node.get_next()
        return adjacents

    def get_vertex_count(self):
        return len(self._vertex_array)


class DiNetworkArray(BaseDiGraph):
    """
    有向网的数组矩阵表示
    """
    def __init__(self):
        self._vertex_array = []
        self._arch_array = []

    def add_arch(self, tail, head, weight):
        self._arch_array[tail][head] = weight

    def delete_arch(self, tail, head):
        self._arch_array[tail][head] = None

    def add_vertex(self, element):
        self._vertex_array.append(element)
        for array in self._arch_array:
            array.append(None)
        self._arch_array.append(
            [None for _ in range(len(self._vertex_array))])

    def set_vertex(self, index, element):
        self._vertex_array[index] = element

    def delete_vertex(self, index):
        self._vertex_array.pop(index)
        self._arch_array.pop(index)
        for array in self._arch_array:
            array.pop(index)

    def get_adjacent(self, index, offset):
        real_index = 0
        for adjacent_index, weight in enumerate(self._arch_array[index]):
            if weight is not None:
                if real_index == offset:
                    return adjacent_index
                real_index = real_index + 1
        return None

    def get_adjacents(self, index):
        for adjacent_index, weight in enumerate(self._arch_array[index]):
            if weight is not None:
                yield adjacent_index

    def get_vertex_count(self):
        return len(self._vertex_array)


if __name__ == "__main__":
    network = DiNetworkAdjacent()
    # network = DiNetworkArray()
    for i in range(6):
        network.add_vertex(100 * i)

    network.add_arch(0, 1, 1)
    network.add_arch(0, 3, 3)
    network.add_arch(1, 2, 12)
    network.add_arch(1, 4, 14)
    network.add_arch(2, 1, 21)
    network.add_arch(3, 0, 30)
    network.add_arch(3, 5, 35)
    network.add_arch(4, 3, 43)

    assert network.dfs() == [0, 1, 2, 4, 3, 5]
    assert network.bfs() == [0, 1, 3, 2, 4, 5]
