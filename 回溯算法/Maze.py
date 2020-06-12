class Node(object):
    def __init__(self, row, column, is_wall):
        self._row = row
        self._column = column
        self._is_wall = bool(is_wall)
        self._next_nodes = []
        self._cursor = 0

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def is_wall(self):
        return self._is_wall

    def add_next_node(self, next_node):
        if not isinstance(next_node, Node):
            raise RuntimeError("Node expected")
        self._next_nodes.append(next_node)

    def get_next_node(self):
        if self._cursor >= len(self._next_nodes):
            return
        node = self._next_nodes[self._cursor]
        self._cursor = self._cursor + 1
        return node

    def __eq__(self, o):
        if not isinstance(o, Node):
            return False
        return o.row == self.row and o.column == self.column

    def __str__(self):
        return "%s{row=%d, column=%d, is_wall=%s}" % (
            self.__class__.__name__,
            self.row,
            self.column,
            self._is_wall)
    __repr__ = __str__


def search(start, end):
    stack = [start]

    while stack:
        current_expand_node = stack[-1]
        next_node = current_expand_node.get_next_node()
        if next_node is None:
            stack.pop(-1)
            continue

        if next_node.is_wall or next_node in stack:
            continue

        if next_node == end:
            print(stack + [next_node])
            continue

        stack.append(next_node)


def main():
    # 0 means wall, 1 means road
    maze = [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
    ]

    all_nodes = []
    for row in range(len(maze)):
        nodes = []
        for column in range(len(maze[row])):
            nodes.append(Node(row, column, not maze[row][column]))
        all_nodes.append(nodes)

    for row in range(len(all_nodes)):
        for column in range(len(all_nodes[row])):
            if row > 0:
                all_nodes[row][column].\
                    add_next_node(all_nodes[row-1][column])
            if row < len(all_nodes) - 1:
                all_nodes[row][column].\
                    add_next_node(all_nodes[row+1][column])
            if column > 0:
                all_nodes[row][column].\
                    add_next_node(all_nodes[row][column-1])
            if column < len(all_nodes[row]) - 1:
                all_nodes[row][column].\
                    add_next_node(all_nodes[row][column+1])

    search(all_nodes[1][1], all_nodes[3][1])


if __name__ == "__main__":
    main()
