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


def dijkstra(graph, source=0):
    """
    Dijkstra 算法实现
    """
    vertex_count = graph.get_vertex_count()

    # A 保存已经计算出最短路径的顶点集，初始时，A 中只包含源点
    A = [source]
    # B 保存尚未计算出最短路径的顶点集，初始时，B 中包含除源点外的其它所有顶点
    B = set([index for index in range(vertex_count) if index != source])

    # D 的每个分量保存一个顶点的最短路径，初始时，源点的最短路径是 0
    D = [None] * vertex_count
    D[source] = 0

    # 初始化 Destimate 数组
    Destimate = [None] * vertex_count
    node = graph.get_vertex(source).next_node
    while node is not None:
        Destimate[node.index] = node.weight
        node = node.next_node
    # 0 表示顶点已经被加入到 A 中
    Destimate[source] = 0

    while B:
        # 找出 estimate 值最小的顶点 m
        lowest_estimate = None
        for index, estimate in enumerate(Destimate):
            if estimate == 0 or estimate is None:
                continue
            if lowest_estimate is None or estimate < lowest_estimate[1]:
                lowest_estimate = (index, estimate)
        m = lowest_estimate[0]

        # 将 m 从 B 中移除
        B.remove(m)
        # 并将其加入到 A 中
        A.append(lowest_estimate[0])
        # D[m] = Destimate[m]
        D[m] = Destimate[m]

        # 更新 Destimte 数组
        Destimate[m] = 0
        node = graph.get_vertex(m).next_node
        while node is not None:
            if Destimate[node.index] == 0:
                node = node.next_node
                continue
            if Destimate[node.index] is None or (D[m] + node.weight) < Destimate[node.index]:
                Destimate[node.index] = D[m] + node.weight
            node = node.next_node

    return D


def test():
    g = Graph()
    for index in range(6):
        g.add_vertex(index)
    for edge in [(0, 2, 10), (0, 4, 30), (0, 5, 100),
                 (1, 2, 5), (2, 3, 50), (3, 5, 10),
                 (4, 3, 20), (4, 5, 60)]:
        g.add_edge(*edge)

    d = dijkstra(g)
    print(d)


if __name__ == "__main__":
    test()
