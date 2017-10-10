#coding: utf8

class DiNetwork:
    def __init__(self):
        self._vertex_array = []
        self._arch_array = []

    def add_arch(self, tail, head, weight):
        self._arch_array[tail][head] = weight
        return self

    def delete_arch(self, tail, head):
        self._arch_array[tail][head] = None
        return self

    def add_vertex(self, element):
        self._vertex_array.append(element)
        for array in self._arch_array:
            array.append(None)
        self._arch_array.append(
            [None for _ in range(len(self._vertex_array))])
        return self

    def set_vertex(self, index, element):
        self._vertex_array[index] = element
        return self

    def delete_vertex(self, index):
        self._vertex_array.remove(index)
        self._arch_array.remove(index)
        for array in self._arch_array:
            array.remove(index)
        return self

    def __str__(self):
        vertexes = "\t".join(map(str, self._vertex_array))
        arches = "\n".join(["\t".join(map(str, array)) for array in self._arch_array])
        return vertexes + "\n" + arches

    def get_next_adjacent(self, index, offset):
        """
        获取某个顶点的下一个邻接点的索引，如果没有了，则返回None
        """
        array = self._arch_array[index]
        for index in xrange(offset, len(array)):
            if array[index] is not None:
                return index
        return None

    def traverse(self):
        """
        用回溯算法实现 有向网 的深度优先遍历
        """
        status = {} # 用status来保存每个顶点的下一个邻接点的索引
        stack = [0]
        index_list = []

        while len(stack):
            top = stack[-1]
            if top not in index_list:
                index_list.append(top)

            offset = status.get(top, 0)
            next = self.get_next_adjacent(top, offset)
            if next:
                status[top] = next + 1
                stack.append(next)
                continue
            stack.pop(-1)
        return index_list

    def get_vertex(self, index):
        return self._vertex_array[index]

if __name__ == "__main__":
    network = DiNetwork()
    for v in range(5):
        network.add_vertex(v * 100)
    network.add_arch(0, 1, 1)
    network.add_arch(1, 4, 14)
    network.add_arch(1, 2, 12)
    network.add_arch(2, 1, 21)
    network.add_arch(3, 0, 30)
    network.add_arch(3, 4, 34)
    network.add_arch(4, 3, 43)
    network.add_arch(0, 3, 3)
    network.add_arch(1, 3, 13)
    network.add_arch(2, 3, 23)
    index_list = network.traverse()
    print [network.get_vertex(index) for index in index_list]

