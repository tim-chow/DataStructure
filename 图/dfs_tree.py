# coding: utf8

"""
DFS 生成树
"""


class TreeNode(object):
    """
    树的孩子兄弟表示法
    """
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
    real_index = 0
    for adjacent_index, weight in enumerate(adjacent_list):
        if weight is None:
            continue
        if real_index == index:
            return adjacent_index
        real_index = real_index + 1
    return None


def dfs_tree_recursive(vertexes, edges):
    visited = [False for _ in range(len(vertexes))]
    root = TreeNode(vertexes[0])
    visited[0] = True

    def _dfs_tree_recursive(start_index, start_node):
        adjacent_list = edges[start_index]
        index = 0
        adjacent_index = get_adjacent(adjacent_list, index)
        while adjacent_index is not None:
            if not visited[adjacent_index]:
                visited[adjacent_index] = True
                node = TreeNode(vertexes[adjacent_index])
                start_node.add_child(node)
                _dfs_tree_recursive(adjacent_index, node)
            index = index + 1
            adjacent_index = get_adjacent(adjacent_list, index)

    _dfs_tree_recursive(0, root)
    return root


def dfs_tree(vertexes, edges):
    root = None
    stack = [0]
    vertex_count = len(vertexes)
    status = [0 for _ in range(vertex_count)]
    visited = [False for _ in range(vertex_count)]
    nodes = [None for _ in range(vertex_count)]
    parent = [None for _ in range(vertex_count)]

    while stack:
        top = stack[-1]
        if not visited[top]:
            visited[top] = True
            node = TreeNode(vertexes[top])
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
        # 剪枝
        if visited[adjacent_index]:
            continue
        stack.append(adjacent_index)
    return root


def test():
    vertexes = range(5)
    edges = []
    for ind in range(len(vertexes)):
        edges.append([])
        for _ in range(len(vertexes)):
            edges[ind].append(None)
    edges[0][1] = 1
    edges[1][0] = 1
    edges[0][3] = 3
    edges[3][0] = 3
    edges[2][3] = 23
    edges[3][2] = 23
    edges[2][4] = 24
    edges[4][2] = 24
    edges[1][2] = 12
    edges[2][1] = 12

    """
    
    0 --- 1 ----┐ 
    |           |
    └---- 3 --- 2 --- 4
    """

    root = dfs_tree_recursive(vertexes, edges)

    # root = dfs_tree(vertexes, edges)

    assert root.get_data() == 0
    first = root.get_first_child()
    assert first.get_data() == 1
    second = first.get_first_child()
    assert second.get_data() == 2
    third = second.get_first_child()
    assert third.get_data() == 3
    forth = third.get_next_sibling()
    assert forth.get_data() == 4


if __name__ == "__main__":
    test()
