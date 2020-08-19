# coding: utf8


class MinHeap(object):
    @staticmethod
    def adjust(heap, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = len(heap) - 1

        get_left_child = lambda ind: 2 * ind + 1
        get_right_child = lambda ind: 2 * ind + 2

        index = start
        while index >= 0:
            left_child_index = get_left_child(index)
            right_child_index = get_right_child(index)
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

    @classmethod
    def heapify(cls, heap):
        for ind in range(len(heap)/2, -1, -1):
            cls.adjust(heap, ind)


class Node(object):
    def __init__(self, cursor, array):
        self.cursor = cursor
        self.array = array

    def __cmp__(self, other):
        diff = self.array[self.cursor] - other.array[other.cursor]
        if diff > 0:
            return 1
        elif diff == 0:
            return 0
        else:
            return -1

    def get_next_node(self):
        if self.cursor >= len(self.array) - 1:
            return None
        return Node(self.cursor + 1, self.array)

    def get_element(self):
        return self.array[self.cursor]


def k_way_merge_sort(arrays):
    result = [None] * sum([len(array) for array in arrays])
    # 取每个数组的第一个元素，建立一个最小堆
    heap = [Node(0, array) for array in arrays]
    MinHeap.heapify(heap)

    index = 0
    k = len(arrays) - 1

    while True:
        # 弹出堆顶元素
        node = heap[0]
        result[index] = node.get_element()
        index = index + 1

        # 如果堆顶元素所在的数组仍有剩余元素，那么从其中取下一个元素，然后放到堆顶
        next_node = node.get_next_node()
        if next_node is not None:
            heap[0] = next_node
            # 调整堆
            MinHeap.adjust(heap, 0, k)
            continue

        # 如果堆空，则退出
        if k == 0:
            break

        # 否则将堆的最后一个元素弹出，然后放到堆顶
        heap[0] = heap[k]
        # 调整堆
        k = k - 1
        MinHeap.adjust(heap, 0, k)

    return result


def test():
    arrays = []
    for ind in range(1, 10):
        array = range(100 * ind, 100 * ind + 100)
        arrays.append(array)
    result = k_way_merge_sort(arrays)
    for ind in range(0, len(result) - 1):
        assert result[ind] <= result[ind + 1]


if __name__ == "__main__":
    test()
