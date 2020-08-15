# coding: utf8

from graph import Graph


def prim(graph, start=0):
    """
    Prim 算法实现
    """
    # 初始化顶点集和边集
    u = [start]
    e = []

    # 初始化 closedge 数组
    closedge = [None] * graph.get_vertex_count()
    node = graph.get_vertex(start).next_node
    while node is not None:
        closedge[node.index] = (start, node.weight)
        node = node.next_node
    # (-1, -1) 表示已经在顶点集中
    closedge[start] = (-1, -1)

    while len(u) != graph.get_vertex_count():
        # 选择代价最小的边
        lowest_cost = None
        for index, edge in enumerate(closedge):
            if edge == (-1, -1) or edge is None:
                continue
            if lowest_cost is None or edge[1] < lowest_cost[2]:
                lowest_cost = (edge[0], index, edge[1])

        # 将顶点加入到 u
        u.append(lowest_cost[1])
        # 将边加入到 e
        e.append(lowest_cost)

        # 更新 closedge 数组
        closedge[lowest_cost[1]] = (-1, -1)
        node = graph.get_vertex(lowest_cost[1]).next_node
        while node is not None:
            if closedge[node.index] == (-1, -1):
                pass
            elif closedge[node.index] is None or closedge[node.index][1] > node.weight:
                closedge[node.index] = (lowest_cost[1], node.weight)
            node = node.next_node

    return u, e


def test():
    g = Graph()
    for ch in ["A", "B", "C", "D", "E", "F", "G"]:
        g.add_vertex(ch)
    for edge in [(0, 1, 7), (0, 3, 5), (1, 2, 8),
                 (1, 3, 9), (1, 4, 7), (2, 4, 5),
                 (3, 4, 15), (3, 5, 6), (4, 5, 8),
                 (4, 6, 9), (5, 6, 11)]:
        g.add_edge(*edge)

    u, e = prim(g)
    print(u)
    print(e)


if __name__ == "__main__":
    test()
