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

    def get_arch(self, tail):
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


def topological_sort(g):
    sequence = []

    stack = []
    for index in range(g.get_vertex_count()):
        node = g.get_vertex(index)
        if node.incoming_degree == 0:
            stack.append(index)

    while stack:
        tail = stack.pop(-1)
        sequence.append(tail)
        for head in g.get_arch(tail):
            g.delete_arch(tail, head)
            if g.get_vertex(head).incoming_degree == 0:
                stack.append(head)

    return sequence


def topological_sort_dfs(g):
    total_sequence = []
    vertex_count = g.get_vertex_count()
    visited = [False for _ in range(vertex_count)]

    def _topological_sort_dfs(start):
        sequence = []
        status = [0 for _ in range(vertex_count)]
        stack = [start]

        while stack:
            top = stack[-1]
            next_vertex = g.get_arch_by_offset(top, status[top])
            if next_vertex is None:
                visited[top] = True
                sequence.insert(0, top)
                stack.pop(-1)
                continue

            status[top] = status[top] + 1
            if not visited[next_vertex]:
                stack.append(next_vertex)

        return sequence

    for index in range(vertex_count):
        if g.get_vertex(index).incoming_degree == 0:
            total_sequence.extend(_topological_sort_dfs(index))

    return total_sequence


def test():
    g = Graph()
    for element in range(13):
        g.add_vertex(element)
    for arch in [(0, 1), (0, 5), (0, 6),
                 (2, 0), (2, 3), (3, 5),
                 (5, 4), (6, 9), (7, 6),
                 (8, 7), (9, 10), (9, 11),
                 (9, 12), (11, 12)]:
        g.add_arch(*arch)

    print(topological_sort_dfs(g))
    print(topological_sort(g))


if __name__ == "__main__":
    test()
