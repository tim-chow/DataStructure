# coding: utf8


def selection_sort(array):
    n = len(array)
    if n <= 1:
        return

    for i in range(1, n / 2 + 1):
        start_index = i - 1
        end_index = n - i
        min_index, max_index = select_min_and_max(
            array, start_index, end_index)

        min_element = array[min_index]
        max_element = array[max_index]
        start_element = array[start_index]
        end_element = array[end_index]

        array[start_index] = min_element
        array[end_index] = max_element
        array[min_index] = start_element
        array[max_index] = end_element


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

    elements = [1, 0, 0, 0, 0, 0]
    print(elements)

    selection_sort(elements)
    print(elements)
