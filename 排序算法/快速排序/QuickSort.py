# coding: utf8


def quick_sort(array, start=None, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(array) - 1

    if start >= end:
        return

    # 选择基准元素
    base = array[start]
    pos = start

    for i in range(start+1, end+1):
        if array[i] >= base:
            continue

        array[pos] = array[i]
        # 将 array[pos+1...i-1] 移动到 array[pos+2...i]
        for j in range(i, pos+1, -1):
            array[j] = array[j-1]
        pos = pos + 1
        array[pos] = base

    # 使用快排分别对左右两部分进行排序
    quick_sort(array, start, pos-1)
    quick_sort(array, pos+1, end)


if __name__ == "__main__":
    import random

    elements = list(range(20))
    random.shuffle(elements)
    print(elements)

    quick_sort(elements)
    print(elements)
