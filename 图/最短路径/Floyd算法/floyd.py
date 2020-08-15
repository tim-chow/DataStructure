# coding: utf8


class Graph(object):
    """
    图的数组矩阵表示法
    """
    def __init__(self):
        self._vertexes = []
        self._arches = []

    def add_vertex(self, element):
        self._vertexes.append(element)
        for arch in self._arches:
            arch.append(None)
        self._arches.append([None] * len(self._vertexes))

    def get_vertex_count(self):
        return len(self._vertexes)

    def add_arch(self, tail, head, weight):
        self._arches[tail][head] = weight

    def get_weight(self, tail, head):
        return self._arches[tail][head]


def floyd(graph):
    """
    Floyd 算法实现
    """
    import sys

    INFINITY = sys.maxint / 2.0
    vertex_count = graph.get_vertex_count()

    # 初始化辅助数组 d[][]、p[][]
    d = []
    p = []

    # 初始时，任意两个顶点之间的最短路径是 INFINITY
    for i in range(vertex_count):
        d.append([])
        for _ in range(vertex_count):
            d[i].append(INFINITY)

    # 初始时，p[i][j] = j
    for i in range(vertex_count):
        p.append([])
        for j in range(vertex_count):
            p[i].append(j)

    def _floyd(i, j, k):
        if k == -1:
            return graph.get_weight(i, j) or INFINITY
        if i == j:
            d[i][j] = 0
            return 0
        if d[i][j] != INFINITY:
            return d[i][j]

        with_k = _floyd(i, k, k - 1) + _floyd(k, j, k - 1)
        without_k = _floyd(i, j, k - 1)

        if with_k < without_k:
            d[i][j] = with_k
            p[i][j] = k
            return with_k

        d[i][j] = without_k
        return without_k

    for i in range(vertex_count):
        for j in range(vertex_count):
            _floyd(i, j, vertex_count - 1)

    return d, p


def test():
    # http://images.timd.cn/data-structure/floyd-example.png
    g = Graph()
    for ind in range(1, 5):
        g.add_vertex(ind)
    for arch in [(0, 1, 2), (0, 2, 6), (0, 3, 4),
                 (1, 2, 3), (2, 0, 7), (2, 3, 1),
                 (3, 0, 5), (3, 2, 12)]:
        g.add_arch(*arch)
    d, p = floyd(g)
    print(d)
    print(p)


if __name__ == "__main__":
    test()
