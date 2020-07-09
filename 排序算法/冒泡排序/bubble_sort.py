# coding: utf8


def bubble_sort(array):
    swapped = True
    for end in range(len(array) - 1, 0, -1):
        if not swapped:
            return
        for ind in range(0, end):
            if array[ind] > array[ind + 1]:
                swapped = True
                array[ind], array[ind + 1] = \
                    array[ind + 1], array[ind]


if __name__ == "__main__":
    import random

    elements = list(range(20)) * 2
    random.shuffle(elements)
    print(elements)

    bubble_sort(elements)
    print(elements)
