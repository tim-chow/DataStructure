#coding: utf8

from abc import ABCMeta, abstractmethod

class BaseDiGraph:
    __metaclass__ = ABCMeta

    def dfs(self):
        """使用回溯算法 实现 图的深度优先遍历"""
        index_list = []
        stack = [0]
        # 使用status 记录 每一个顶点的第几个邻接点已经被访问过了
        status = dict.fromkeys(range(self.get_vertex_count()), 0)
        visited = [False for i in range(self.get_vertex_count())]

        while len(stack):
            top = stack[-1]
            if visited[top] == False:
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
        index_list = []
        queue = [0]
        visited = [False for _ in range(self.get_vertex_count())]

        while queue:
            first = queue.pop(0)
            if visited[first]:
                continue
            visited[first] = True
            index_list.append(first)
            queue.extend(self.get_adjacents(first))
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

class HeadNode:
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

class AdjacentNode:
    def __init__(self, index, weight):
        self._index = index
        self._weight = weight
        self._next = None

    def set_index(self, index):
        self._index = index
        return self

    def get_index(self):
        return self._index

    def set_weight(self, weight):
        self._weight = weight
        return self

    def get_weight(self):
        return self._weight        

    def set_next(self, next):
        self._next = next

    def get_next(self):
        return self._next

class DiNetworkAdjacent(BaseDiGraph):
    def __init__(self):
        self._vertex_array = []

    def add_vertex(self, element):
        self._vertex_array.append(HeadNode(element))

    def set_vertext(self, index, element):
        self._vertex_array[index].set_element(element)

    def get_vertext(self, index):
        return self._vertex_array[index]

    def add_arch(self, tail, head, weight):
        head_node = self._vertex_array[tail]
        node = head_node.get_next()

        while node != None:
            if node.get_index() == head:
                node.set_weight(weight)
                return self
            head_node = node
            node = node.get_next()
        head_node.set_next(AdjacentNode(head, weight))
        return self

    def delete_vertex(self, index):
        self._vertex_array.pop(index)
        for head_node in self._vertex_array:
            node = head_node.get_next()
            while node != None:
                if node.get_index() == index:
                    head_node.set_next(node.get_next())
                elif node.get_index() > index:
                    node.set_index(node.get_index() - 1)
                head_node = node
                node = node.get_next()
        return self

    def delete_arch(self, tail, head):
        head_node = self._vertex_array[tail]
        adjacent_node = head_node.get_next()
        while adjacent_node != None:
            if adjacent_node.get_index() == head:
                head_node.set_next(adjacent_node.get_next())
                break
            head_node = adjacent_node
            adjacent_node = adjacent_node.get_next()

    def get_adjacent(self, index, offset):
        node = self._vertex_array[index]
        for ind in range(offset+1):
            node = node.get_next()
            if node == None:
                break
            if ind == offset:
                return node.get_index()
        return None

    def get_adjacents(self, index, return_node=False):
        adjacents = []
        node = self._vertex_array[index].get_next()
        while node != None:
            adjacents.append(node if return_node else node.get_index())
            node = node.get_next()
        return adjacents

    def get_vertex_count(self):
        return len(self._vertex_array)

    def __str__(self):
        result = []
        for ind, head_node in enumerate(self._vertex_array):
            line = ["(%d, %s):" % (ind, head_node.get_element())]
            for adjacent_node in self.get_adjacents(ind, True):
                line.append("({0._index}, {0._weight})".format(adjacent_node))
            result.append("\t".join(line))
        return "\n".join(result)

class DiNetworkArray(BaseDiGraph):
    def __init__(self):
        self._vertex_array = []
        self._arch_array = []

    def add_arch(self, tail, head, weight):
        self._arch_array[tail][head] = weight
        return self

    def delete_arch(self, tail, head):
        self._arch_array[tail][head] = None
        return self

    def add_vertex(self, element):
        self._vertex_array.append(element)
        for array in self._arch_array:
            array.append(None)
        self._arch_array.append(
            [None for _ in range(len(self._vertex_array))])
        return self

    def set_vertex(self, index, element):
        self._vertex_array[index] = element
        return self

    def delete_vertex(self, index):
        self._vertex_array.pop(index)
        self._arch_array.pop(index)
        for array in self._arch_array:
            array.pop(index)
        return self

    def __str__(self):
        vertexes = "\t".join(map(str, self._vertex_array))
        arches = "\n".join(["\t".join(map(str, array)) for array in self._arch_array])
        return vertexes + "\n" + arches

    def get_adjacent(self, index, offset):
        real_index = -1
        for adjacent_index, weight in enumerate(self._arch_array[index]):
            if weight is not None:
                real_index = real_index + 1
                if real_index == offset:
                    return adjacent_index
        return None

    def get_adjacents(self, index):
        for ind, adjacent in enumerate(self._arch_array[index]):
            if adjacent is not None:
                yield ind

    def get_vertex_count(self):
        return len(self._vertex_array)

if __name__ == "__main__":
    network = DiNetworkAdjacent()
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
    print network

    print network.dfs()
    print network.bfs()

