# coding: utf8


def selection_sort(array):
    n = len(array)
    if n <= 1:
        return

    for i in range(1, n / 2 + 1):
        min_index, max_index = \
            select_min_and_max(array, i - 1, n - i)
        array[i - 1], array[min_index] = \
            array[min_index], array[i - 1]
        array[n - i], array[max_index] = \
            array[max_index], array[n - i]


def select_min_and_max(array, start, end):
    assert start < end
    min_index = start
    max_index = start

    for ind in range(start + 1, end + 1):
        if array[ind] <= array[min_index]:
            min_index = ind
        elif array[ind] >= array[max_index]:
            max_index = ind

    return min_index, max_index


if __name__ == "__main__":
    import random

    elements = list(range(20)) * 2
    random.shuffle(elements)
    print(elements)

    selection_sort(elements)
    print(elements)
