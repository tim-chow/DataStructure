# coding: utf8

# 头节点
class HeadNode(object):
    def __init__(self, data):
        # 数据域
        self._data = data
        # 指针域：指向第一个表节点
        self._first_adjacent_node = None

    def add_adjacent(self, adjacent_node):
        node = self._first_adjacent_node
        if node is None:
            self._first_adjacent_node = adjacent_node
            return

        while node.next != None:
            node = node.next
        node.next = adjacent_node

    @property
    def next(self):
        return self._first_adjacent_node

    @next.setter
    def next(self, next):
        self._first_adjacent_node = next

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return "HeadNode[data=%s]" % self._data
    __str__ = __repr__

# 表节点
class AdjacentNode(object):
    def __init__(self, index, info):
        # 索引域：邻接点在顶点集中的索引
        self._index = index
        # 信息域：存储权重等信息
        self._info = info
        # 指针域：指向下一个邻接点
        self._next = None

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    @property
    def index(self):
        return self._index

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, info):
        self._info = info

    def __str__(self):
        return "Adjacent[index={0.index}, info={0.info}]".format(self)
    __repr__ = __str__

class Graph(object):
    def __init__(self):
        self._vertexes =[]

    def add_edge(self, start, end, info):
        for i, j in [(start, end), (end, start)]:
            vertex = self._vertexes[i]
            node = vertex
            while node.next != None:
                if node.next.index == j:
                    node.next.info = info
                    break
                node = node.next
            else:
                node.next = AdjacentNode(j, info)

    @property
    def vertexes(self):
        return self._vertexes

    def add_vertex(self, data):
        self._vertexes.append(HeadNode(data))

def prim(g, start=0):
    v = g.vertexes
    u = [start]
    e = []

    # 初始化closedge数组，
    # + closedge数组的每一个分量表示：
    # + + 从u中的所有顶点到该顶点（在v-u中）的边中最短的那条
    # + + 每个分量是一个元组：(u中的顶点索引，权重)
    # + + None表示没有符合条件的边，也就是无法从u中的顶点达到该顶点
    # + + 0表示该顶点已经在u中
    closedge = [None] * len(v)
    closedge[start] = 0
    node = v[start].next
    while node is not None:
        closedge[node.index] = (start, node.info)
        node = node.next

    while len(u) != len(v):
        # 从closedge中选择代价最小的边
        lowest_cost = None
        for index, edge in enumerate(closedge):
            if edge == 0 or edge is None:
                continue
            if lowest_cost is None or edge[1] < lowest_cost[2]:
                lowest_cost = (edge[0], index, edge[1])

        u.append(lowest_cost[1])
        e.append(lowest_cost)

        # 修改closedge数组
        closedge[lowest_cost[1]] = 0
        node = v[lowest_cost[1]].next
        while node is not None:
            if closedge[node.index] == 0:
                node = node.next
                continue
            if closedge[node.index] is None or \
                    node.info < closedge[node.index][1]:
                closedge[node.index] = (lowest_cost[1], node.info)
            node = node.next
    return e

def kruskal(g):
    # 创建一个新图
    # graph_new = Graph()
    # 图中包含原图中所有的顶点，但是不包含任何边
    # for vertex in g.vertexes:
    #     graph_new.add_vertex(vertex.data)

    # 将所有的边按权值进行排序
    edges = {}
    for start, vertex in enumerate(g.vertexes):
        node = vertex.next
        while node is not None:
            end = node.index
            if start < end:
                edges[(start, end)] = node.info
            else:
                edges[(end, start)] = node.info
            node = node.next
    edges = [(k[0], k[1], v) for k, v in edges.items()]
    edges = sorted(edges, key=lambda x: x[2])

    # 对排序后的边依次执行下面的操作： 
    # + 如果这条边会导致某个连通分量产生回路，那么则丢弃
    # + 否则加入到graph_new中
    # 重复执行上面的步骤，一直到graph_new连通

    # 使用并查集做连通性检查
    union_find = [i for i in range(len(g.vertexes))]
    for start, end, info in edges:
        root_start = union_find[start]
        root_end = union_find[end]
        # 丢弃导致回路的边
        if root_start == root_end:
            continue
        print "%s ---> %s: %d" % (g.vertexes[start].data, 
                g.vertexes[end].data, info)
        # 合并两个联通分量
        # + 同时，检查整个图的连通性
        flag = True
        for i in range(len(union_find)):
            if union_find[i] == root_end:
                union_find[i] = root_start
            if union_find[i] != root_start:
                flag = False
        if flag:
            print "最小生成树生成完成"
            break

if __name__ == "__main__":
    g = Graph()
    for ch in ["A", "B", "C", "D", "E", "F", "G"]:
        g.add_vertex(ch)
    for edge in [(0, 1, 7), (0, 3, 5),
        (1, 2, 8), (1, 3, 9), (1, 4, 7),
        (2, 4, 5), (3, 4, 15), (3, 5, 6),
        (4, 5, 8), (4, 6, 9), (5, 6, 11)]:
        g.add_edge(*edge)
    vertexes = g.vertexes
    
    edges = prim(g, 0)
    for start, end, info in edges:
        start = vertexes[start].data
        end = vertexes[end].data
        print "%s ---> %s: %d" % (start, end, info)
    print "=" * 10
    kruskal(g)

