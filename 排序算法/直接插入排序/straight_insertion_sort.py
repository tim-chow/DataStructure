# coding: utf8


def straight_insertion_sort(array):
    if len(array) <= 1:
        return

    for i in range(1, len(array)):
        for j in range(0, i):
            if array[j] <= array[i]:
                continue
            temp = array[i]
            # 把 array[j...i-1] 移动到 array[j+1...i]
            for ind in range(i, j, -1):
                array[ind] = array[ind - 1]
            array[j] = temp
            break


if __name__ == "__main__":
    import random

    elements = list(range(20)) * 2
    random.shuffle(elements)
    print(elements)

    straight_insertion_sort(elements)
    print(elements)
