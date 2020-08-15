# coding: utf8


class HeadNode(object):
    def __init__(self, element):
        self.element = element
        self.next_node = None


class AdjacentNode(object):
    def __init__(self, index, weight):
        self.index = index
        self.weight = weight
        self.next_node = None


class Graph(object):
    def __init__(self):
        self._vertexes = []

    def add_vertex(self, element):
        self._vertexes.append(HeadNode(element))

    def add_edge(self, tail, head, weight):
        for i, j in [(tail, head), (head, tail)]:
            node = self._vertexes[i]
            while node.next_node is not None:
                if node.next_node.index == j:
                    node.next_node.weight = weight
                    break
                node = node.next_node
            else:
                node.next_node = AdjacentNode(j, weight)

    def get_vertex_count(self):
        return len(self._vertexes)

    def get_vertex(self, index):
        return self._vertexes[index]
