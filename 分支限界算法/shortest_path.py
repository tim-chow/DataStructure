# coding: utf8

# 最小堆
class MinHeap:
    get_parent = lambda self, ind: (ind - 1) / 2
    get_left_child = lambda self, ind: 2 * ind + 1
    get_right_child = lambda self, ind: 2 * ind + 2

    def __init__(self):
        self._queue = []

    def _adjust(self, heap, start=None, end=None):
        if start == None:
            start = 0
        if end == None:
            end = len(heap) - 1

        index = start
        while index >= 0:
            left_child_index = self.get_left_child(index)
            right_child_index = self.get_right_child(index)
            if left_child_index > end:
                break
            if right_child_index > end:
                if heap[index] > heap[left_child_index]:
                    heap[index], heap[left_child_index] = \
                        heap[left_child_index], heap[index]
                break

            if heap[index] <= heap[left_child_index] and \
                heap[index] <= heap[right_child_index]:
                break
            if heap[right_child_index] > heap[left_child_index]:
                heap[index], heap[left_child_index] = \
                    heap[left_child_index], heap[index]
                index = left_child_index
            else:
                heap[index], heap[right_child_index] = \
                    heap[right_child_index], heap[index]
                index = right_child_index

    def put(self, priority, element):
        self._queue.append((priority, element))
        index = len(self._queue) - 1
        parent = self.get_parent(index)

        while parent >= 0:
            self._adjust(self._queue, parent)
            parent = self.get_parent(parent)

    def get(self):
        if not self._queue:
            raise RuntimeError("queue is empty")
        result = self._queue[0]
        last = self._queue.pop(-1)
        if self._queue:
            self._queue[0] = last
            self._adjust(self._queue, 0)
        return result

    def size(self):
        return len(self._queue)

    def empty(self):
        return not len(self._queue)

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

def shorted_path(graph, start):
    queue = MinHeap()
    queue.put(0, start)
    result = {}

    while not queue.empty():
        current_weight, vertex_index = queue.get()
        for ind, weight in enumerate(graph[1][vertex_index]):
            if not weight:
                continue
            weight = current_weight + weight
            if ind not in result or weight < result[ind]: # 剪枝
                result[ind] = weight
                queue.put(weight, ind) # 优先级队列
    return result

if __name__ == "__main__":
    import pprint
    graph = generate_direct_graph_example()
    pprint.pprint(graph)

    result = shorted_path(graph, 0)
    print "\n".join(["从%s到%s的距离是：%-2d" %
            (graph[0][0], graph[0][k], v)
        for k, v in result.items()])

