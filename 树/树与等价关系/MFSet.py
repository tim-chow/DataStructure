class Node:
    def __init__(self, element, parent=-1):
        self._element = element
        self._parent = parent

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def get_element(self):
        return self._element

    def find_root(self, nodes):
        index = nodes.index(self)
        node = self
        while node.get_parent() >= 0:
            index = node.get_parent()
            node = nodes[index]
        return node, index

    def merge(self, another, nodes):
        another_root, another_index = another.find_root(nodes)
        root, index = self.find_root(nodes)
        if another_root == root:
            return

        another_nodes_count = -1 * another_root.get_parent()
        nodes_count = -1 * root.get_parent()

        if another_nodes_count > nodes_count:
            root.set_parent(another_index)
            another_root.set_parent(-1*(another_nodes_count + nodes_count))
        else:
            another_root.set_parent(index)
            root.set_parent(-1*(another_nodes_count + nodes_count))

    def __str__(self):
        return "Node[element={0._element}, parent={0._parent}]".format(self)
    __repr__ = __str__

def main():
    R = [(0, 2), (2, 4), (4, 6), (6, 8)]
    S = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    nodes = [Node(element, -1) for element in S]

    for x, y in R:
        nodes[x].merge(nodes[y], nodes)

    print nodes

if __name__ == "__main__":
    main()

