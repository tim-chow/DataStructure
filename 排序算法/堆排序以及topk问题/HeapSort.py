def adjust(array, start, end=None):
    if end is None:
        end = len(array)

    while 2*start+1 < end:
        if 2*start+2 >= end:
            if array[start] > array[2*start+1]:
                array[start], array[2*start+1] = array[2*start+1], array[start]
            break

        element = array[start]
        left = array[2*start+1]
        right = array[2*start+2]
        if element <= left and element <= right:
            break

        if left < right:
            array[start], array[2*start+1] = array[2*start+1], array[start]
            start = 2*start+1
        else:
            array[start], array[2*start+2] = array[2*start+2], array[start]
            start = 2*start+2

def heapify(array):
    mid = len(array) / 2
    for i in range(mid, -1, -1):
        adjust(array, i, len(array))

def insert(heap, element):
    heap.append(element)
    index = ((len(heap) - 1) - 1) / 2
    while index >= 0:
        adjust(heap, index, len(heap))
        parent = (index - 1) / 2
        if parent < 0 or heap[parent] <= heap[index]:
            break
        index = parent

def heap_sort(array):
    heapify(array)

    end = len(array)
    while end > 1:
        array[0], array[end-1] = array[end-1], array[0]
        end = end - 1
        adjust(array, 0, end)

def topk(array, k):
    for ind in range(k/2, -1, -1):
        adjust(array, ind, k)

    for ind in range(k, len(array)):
        if array[ind] <= array[0]:
            continue
        array[0] = array[ind]
        adjust(array, 0, k)
    return array[:k]

def test():
    import random
    seq = range(1, 15)
    random.shuffle(seq)
    print seq
    print topk(seq, 7)

    seq = range(1, 15)
    random.shuffle(seq)
    print seq
    heap_sort(seq)
    print seq

if __name__ == "__main__":
    test()

