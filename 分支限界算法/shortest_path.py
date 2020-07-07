# coding: utf8


# 最小堆
class MinHeap(object):
    get_parent = lambda self, ind: (ind - 1) / 2
    get_left_child = lambda self, ind: 2 * ind + 1
    get_right_child = lambda self, ind: 2 * ind + 2

    def __init__(self):
        self._array = []

    def _adjust(self, array, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = len(array) - 1

        while self.get_left_child(start) <= end:
            left_child_index = self.get_left_child(start)
            right_child_index = self.get_right_child(start)

            if right_child_index > end:
                if array[start] > array[left_child_index]:
                    array[start], array[left_child_index] = \
                        array[left_child_index], array[start]
                break

            if array[start] <= array[left_child_index] and \
                    array[start] <= array[right_child_index]:
                break

            if array[right_child_index] > array[left_child_index]:
                array[start], array[left_child_index] = \
                    array[left_child_index], array[start]
                start = left_child_index
            else:
                array[start], array[right_child_index] = \
                    array[right_child_index], array[start]
                start = right_child_index

    def put(self, priority, element):
        self._array.append((priority, element))
        index = len(self._array) - 1
        parent = self.get_parent(index)

        while parent >= 0:
            self._adjust(self._array, parent)
            parent = self.get_parent(parent)

    def get(self):
        if not self._array:
            raise RuntimeError("queue is empty")
        result = self._array[0]
        last = self._array.pop(-1)
        if self._array:
            self._array[0] = last
            self._adjust(self._array, 0)
        return result

    def empty(self):
        return not len(self._array)


# 图的数组/矩阵表示法
def generate_direct_graph_example():
    vertexes = ['s', 'a', 'b', 'c', 'd', 'e',
        'f', 'g', 'h', 'i', 't']
    arches = [
        [0, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 7, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    return vertexes, arches


def shortest_path(graph, start):
    queue = MinHeap()
    queue.put(0, start)
    result = {}

    while not queue.empty():
        current_weight, vertex_index = queue.get()
        for ind, weight in enumerate(graph[1][vertex_index]):
            if not weight:
                continue
            total_weight = current_weight + weight
            if ind not in result or total_weight < result[ind]:
                result[ind] = total_weight
                queue.put(total_weight, ind)
    return result


if __name__ == "__main__":
    import pprint

    graph = generate_direct_graph_example()
    pprint.pprint(graph)

    result = shortest_path(graph, 0)
    print(
        "\n".join(["从%s到%s的距离是：%-3d" %
            (graph[0][0], graph[0][k], v)
            for k, v in result.items()])
    )
