# coding: utf8


def adjust(array, start, end):
    if start > end:
        raise RuntimeError("unreachable")

    while 2 * start + 1 <= end:
        left = 2 * start + 1

        # 只有左孩子节点
        if 2 * start + 2 > end:
            if array[left] < array[start]:
                array[start], array[left] = \
                    array[left], array[start]
            break

        right = 2 * start + 2
        # 无需调整
        if array[start] <= array[left] and \
                array[start] <= array[right]:
            break

        if array[left] <= array[right]:
            array[start], array[left] = \
                array[left], array[start]
            start = left
            continue

        array[start], array[right] = \
            array[right], array[start]
        start = right


def heap_sort(array):
    for ind in range(len(array) / 2, -1, -1):
        adjust(array, ind, len(array) - 1)

    for end in range(len(array) - 1, 0, -1):
        array[0], array[end] = array[end], array[0]
        adjust(array, 0, end - 1)


def topk(array, k):
    if k >= len(array):
        return

    for ind in range(k / 2, -1, -1):
        adjust(array, ind, k - 1)

    for ind in range(k, len(array)):
        if array[ind] <= array[0]:
            continue

        array[0], array[ind] = array[ind], array[0]
        adjust(array, 0, k - 1)


if __name__ == "__main__":
    import random
    elements = list(range(1, 16) * 2)
    random.shuffle(elements)
    print("elements are: %s" % elements)
    heap_sort(elements)
    print("heap sort: %s" % elements)
    random.shuffle(elements)
    print("elements are: %s" % elements)
    topk(elements, 3)
    print("top 3: %s" % elements)
