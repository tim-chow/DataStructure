class MinHeap:
    @staticmethod
    def adjust(heap, start=None, end=None):
        get_parent = lambda ind: (ind - 1) / 2
        get_left_child = lambda ind: 2 * ind + 1
        get_right_child = lambda ind: 2 * ind + 2

        if start == None:
            start = 0
        if end == None:
            end = len(heap) - 1

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

class Iterator:
    def __init__(self, array):
        self._array = array
        self._cursor = 0

    def has_next(self):
        return self._cursor < len(self._array)

    def next(self):
        result = self._array[self._cursor]
        self._cursor = self._cursor + 1
        return result

    def peek(self):
        return self._array[self._cursor]

    def __cmp__(self, another):
        self_peek = self.peek()
        another_peek = another.peek()
        if self_peek < another_peek:
            return -1
        if self_peek > another_peek:
            return 1
        return 0

def k_way_merge_sort(arrays):
    result = [None] * sum([len(lst) for lst in arrays])
    index = 0

    k = len(arrays) - 1
    iterators = map(Iterator, arrays)
    MinHeap.heapify(iterators)

    while k >= 0:
        top = iterators[0]
        result[index] = top.next()
        index = index + 1
        if top.has_next():
            MinHeap.adjust(iterators, 0, k)
            continue
        iterators[0] = iterators[k]
        k = k - 1
        MinHeap.adjust(iterators, 0, k)

    return result

if __name__ == "__main__":
    arrays = [
        [1, 5, 9, 13, 15, 17],
        [4, 8, 12, 14, 16, 18],
        [3, 7, 11, 30],
        [2, 6, 10],
    ]
    print k_way_merge_sort(arrays)

