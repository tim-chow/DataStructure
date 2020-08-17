# coding: utf8


class Node(object):
    def __init__(self, element):
        self.element = element
        self.incoming_degree = 0


class Graph(object):
    """
    数组矩阵表示法
    """
    def __init__(self):
        self._vertexes = []
        self._arches = []

    def add_vertex(self, element):
        self._vertexes.append(Node(element))
        for arch in self._arches:
            arch.append(None)
        self._arches.append([None] * len(self._vertexes))
        return len(self._vertexes) - 1

    def add_arch(self, tail, head, weight=1):
        old_weight = self._arches[tail][head]
        if old_weight is None:
            self._vertexes[head].incoming_degree = \
                self._vertexes[head].incoming_degree + 1
        self._arches[tail][head] = weight

    def delete_arch(self, tail, head):
        old_weight = self._arches[tail][head]
        if old_weight is None:
            return
        self._vertexes[head].incoming_degree = \
            self._vertexes[head].incoming_degree - 1
        self._arches[tail][head] = None

    def get_vertex_count(self):
        return len(self._vertexes)

    def get_vertex(self, index):
        return self._vertexes[index]

    def get_arches(self, tail):
        for head, weight in enumerate(self._arches[tail]):
            if weight is None:
                continue
            yield head

    def get_arch_by_offset(self, head, offset):
        real_index = 0
        for index, weight in enumerate(self._arches[head]):
            if weight is None:
                continue
            if real_index == offset:
                return index
            real_index = real_index + 1
        return None

    def get_weight(self, tail, head):
        return self._arches[tail][head]


def topological_order(g):
    """
    利用拓扑排序计算每个顶点的最早发生时间和最晚发生时间
    """
    # 初始化 stack、ve、vl, incoming_degrees
    stack = []
    ve = []
    vl = []
    incoming_degrees = []
    for index in range(g.get_vertex_count()):
        ve.append(None)
        vl.append(None)
        incoming_degree = g.get_vertex(index).incoming_degree
        incoming_degrees.append(incoming_degree)

        if incoming_degree == 0:
            ve[index] = 0
            stack.append(index)

    sequence = []
    while stack:
        top = stack.pop(-1)
        sequence.append(top)
        for head in g.get_arches(top):
            new = ve[top] + g.get_weight(top, head)
            if ve[head] is None or new > ve[head]:
                ve[head] = new
            incoming_degrees[head] = incoming_degrees[head] - 1
            if incoming_degrees[head] == 0:
                stack.append(head)

    vl[-1] = ve[-1]

    for tail in range(len(sequence) -1, -1, -1):
        for head in g.get_arches(tail):
            new = vl[head] - g.get_weight(tail, head)
            if vl[tail] is None or new < vl[tail]:
                vl[tail] = new

    return ve, vl


def critical_path(g):
    ve, vl = topological_order(g)
    critical_activities = []
    for tail in range(g.get_vertex_count()):
        for head in g.get_arches(tail):
            if ve[tail] == vl[head] - g.get_weight(tail, head):
                critical_activities.append((tail, head))

    paths = []
    d = {}
    for a in critical_activities:
        d.setdefault(a[0], []).append(a[1])
    status = {}
    stack = [0]
    while stack:
        top = stack[-1]
        if top not in d:
            paths.append(stack[:])
            stack.pop(-1)
            continue
        if top in status and status[top] >= len(d[top]):
            stack.pop(-1)
            status[top] = 0
            continue
        stack.append(d[top][status.get(top, 0)])
        status[top] = status.get(top, 0) + 1
    return paths


def test():
    g = Graph()
    for index in range(7):
        g.add_vertex(index)
    for arch in [(0, 1, 3), (0, 2, 2), (0, 3, 6),
                 (1, 3, 2), (1, 4, 4), (2, 3, 1),
                 (2, 5, 3), (3, 4, 1), (4, 6, 3),
                 (5, 6, 4)]:
        g.add_arch(*arch)
    print(critical_path(g))


if __name__ == "__main__":
    test()
