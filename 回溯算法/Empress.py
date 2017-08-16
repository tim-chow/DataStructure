class Node(object):
    def __init__(self, row, column):
        self._row = row
        self._column = column
        self._next_nodes = []
        self._cursor = 0

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def next_nodes(self):
        return self._next_nodes

    @next_nodes.setter
    def next_nodes(self, next_nodes):
        self._next_nodes = next_nodes

    def get_next_node(self):
        if not self._next_nodes or \
            self._cursor >= len(self._next_nodes):
            return 

        node = self._next_nodes[self._cursor]
        self._cursor = self._cursor + 1
        return node

    def __str__(self):
        return "Node{row=%d, column=%d}" % (
            self._row, self._column)
    __repr__ = __str__

    def reset(self):
        self._cursor = 0

def search(root, n):
    stack = [root]

    while stack:
        current_expand_node = stack[-1]
        next_node = current_expand_node.get_next_node()
        if not next_node:
            stack.pop(-1).reset() # reset here!!!
            continue

        flag = True
        for i in range(1, len(stack)):
            if stack[i].row == next_node.row or \
                stack[i].column == next_node.column or \
                abs(stack[i].row - next_node.row) == \
                    abs(stack[i].column - next_node.column):
                    flag = False
                    break
        if not flag:
            continue
        if len(stack) == n:
            print([(node.row, node.column)
                for node in stack[1:]])
            continue
        stack.append(next_node)

def main(n=8):
    root = Node(0, 0)
    all_nodes = []
    for row in range(1, n+1):
        all_nodes.append([Node(row, column) 
            for column in range(1, n+1)])

    root.next_nodes = all_nodes[0]
    for row in range(len(all_nodes)-1):
        for node in all_nodes[row]:
            node.next_nodes = all_nodes[row+1]

    search(root, n)

if __name__ == "__main__":
    main()

