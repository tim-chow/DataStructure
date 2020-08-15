# coding: utf8

from graph import Graph


def kruskal(graph):
    """
    Kruskal 算法实现
    """
    # 获取原图的边集
    edges = []
    duplicate_set = set()
    for index in range(graph.get_vertex_count()):
        node = graph.get_vertex(index).next_node
        while node is not None:
            # 排重
            if (index, node.index) in duplicate_set or \
                    (node.index, index) in duplicate_set:
                node = node.next_node
                continue
            edges.append((index, node.index, node.weight))
            duplicate_set.add((index, node.index))
            node = node.next_node
    # 对原图的边集进行排序
    edges = sorted(edges, key=lambda t: t[2])

    # 初始化结果边集
    T = []

    # 初始化并查集
    union_find = [i for i in range(graph.get_vertex_count())]

    def find_root(index):
        temp = index
        while union_find[temp] != temp:
            temp = union_find[temp]
        return temp

    while edges:
        # 从原图的剩余边中选择代价最小的边
        edge = edges.pop(0)
        # 判断其与 T 中的边是否构成环
        # 如果是，则丢弃该边
        root_0 = find_root(edge[0])
        root_1 = find_root(edge[1])
        if root_0 == root_1:
            continue
        # 否则，将其加入到 T
        T.append(edge)
        # 将 root_1 接到 root_0
        union_find[root_1] = root_0

    return T


def test():
    g = Graph()
    for ch in ["A", "B", "C", "D", "E", "F", "G"]:
        g.add_vertex(ch)
    for edge in [(0, 1, 7), (0, 3, 5), (1, 2, 8),
                 (1, 3, 9), (1, 4, 7), (2, 4, 5),
                 (3, 4, 15), (3, 5, 6), (4, 5, 8),
                 (4, 6, 9), (5, 6, 11)]:
        g.add_edge(*edge)

    print(kruskal(g))


if __name__ == "__main__":
    test()
