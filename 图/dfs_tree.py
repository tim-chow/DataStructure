#coding: utf8

# 孩子兄弟表示法
class Node:
    def __init__(self, data):
        self._data = data
        self._first_child = None
        self._next_sibling = None

    def add_child(self, child):
        if self._first_child is None:
            self._first_child = child
            return
        node = self._first_child
        while node._next_sibling is not None:
            node = node._next_sibling
        node._next_sibling = child

    def get_first_child(self):
        return self._first_child

    def get_next_sibling(self):
        return self._next_sibling

    def get_data(self):
        return self._data

def get_adjacent(adjacent_list, index):
    count = 0
    for adjacent_index, weight in enumerate(adjacent_list):
        if weight is None:
            continue
        if count == index:
            return adjacent_index
        count = count + 1
    return None

def dfs_tree_recursive(start_index, start_node, 
        visited, vertexes, edges):
    visited[start_index] = True
  
    adjacent_list = edges[start_index]
    index = 0
    adjacent_index = get_adjacent(adjacent_list, index)
    while adjacent_index is not None:
        if visited[adjacent_index] == False:
            node = Node(adjacent_index)
            start_node.add_child(node)
            dfs_tree_recursive(adjacent_index,
                node, visited, vertexes, edges)
        index = index + 1
        adjacent_index = get_adjacent(adjacent_list, index)

def dfs_tree(vertexes, edges):
    root = None
    stack = [0]
    vertex_count = len(vertexes)

    # 记录每个顶点的第几个邻接点还没被访问
    status = [0 for i in range(vertex_count)]
    visited = [False for i in range(vertex_count)]
    nodes = [None for i in range(vertex_count)]
    parent = [None for i in range(vertex_count)]

    while len(stack):
        top = stack[-1]
        if False == visited[top]:
            visited[top] = True
            node = Node(top)
            nodes[top] = node
            if parent[top] is None:
                root = node
            else:
                nodes[parent[top]].add_child(node)

        adjacent_index = get_adjacent(edges[top], status[top])
        if adjacent_index is None:
            stack.pop(-1)
            continue
        status[top] = status[top] + 1
        parent[adjacent_index] = top
        stack.append(adjacent_index)
    return root

if __name__ == "__main__":
    vertexes = range(4) 
    edges = [[None] * 4, [None] * 4, [None] * 4, [None] * 4]
    edges[0][1] = 1
    edges[0][3] = 3
    edges[3][2] = 3
    import pprint
    pprint.pprint(edges)

    root = Node(0)
    visited = [False for _ in range(len(vertexes))]
    dfs_tree_recursive(0, root, visited, vertexes, edges)

    print root.get_data()
    first_child = root.get_first_child()
    print first_child.get_data()
    second_child = first_child.get_next_sibling()
    print second_child.get_data()
    first_grandson = second_child.get_first_child()
    print first_grandson.get_data()

