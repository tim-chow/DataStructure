# coding: utf8


def bucket_sort(array, m, divide_func, sort_func):
    n = len(array)

    # 创建桶
    buckets = [([None] * n) for _ in range(m)]

    bucket_index_to_cursor = {}
    # 将元素放到相应的桶中
    for element in array:
        bucket_index = divide_func(element)
        if bucket_index not in bucket_index_to_cursor:
            bucket_index_to_cursor[bucket_index] = 0
        else:
            bucket_index_to_cursor[bucket_index] = \
                bucket_index_to_cursor[bucket_index] + 1
        buckets[bucket_index][bucket_index_to_cursor[bucket_index]] = element

    # 对每个桶内的数据元素进行排序
    for bucket_index, last_index in bucket_index_to_cursor.items():
        sort_func(buckets[bucket_index], 0, last_index)

    # 将桶中的元素复制回序列
    cursor = 0
    for bucket_index, last_index in sorted(bucket_index_to_cursor.items(), key=lambda k: k):
        bucket = buckets[bucket_index]
        for index in range(last_index + 1):
            array[cursor] = bucket[index]
            cursor = cursor + 1


if __name__ == "__main__":
    import random


    def divide(element):
        if element < 5:
            return 0
        if element < 10:
            return 1
        if element < 15:
            return 2
        return 3

    # 直接插入排序
    def sort(array, start, end):
        if start >= end:
            return
        for i in range(start + 1, end + 1):
            for j in range(0, i):
                if array[j] <= array[i]:
                    continue
                temp = array[i]
                # 把 array[j...i-1] 移动到 array[j+1...i]
                for ind in range(i, j, -1):
                    array[ind] = array[ind - 1]
                array[j] = temp
                break

    elements = list(range(20)) * 2
    random.shuffle(elements)
    print(elements)

    bucket_sort(elements, 4, divide, sort)
    print(elements)
