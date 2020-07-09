# coding: utf8


def shell_sort(array):
    gap = len(array) / 2
    while gap >= 1:
        group_sort(array, gap)
        gap = gap / 2


def group_sort(array, gap):
    n = len(array)
    for i in range(gap):
        # 对分组进行直接插入排序
        j = 1
        while i + j * gap < n:
            for k in range(0, j):
                temp = array[i + j * gap]
                if array[i + k * gap] <= temp:
                    continue
                for m in range(j, k, -1):
                    array[i + m * gap] = array[i + (m - 1) * gap]
                array[i + k * gap] = temp
                break
            j = j + 1


if __name__ == "__main__":
    import random

    elements = list(range(20)) * 2
    random.shuffle(elements)
    print(elements)

    shell_sort(elements)
    print(elements)
