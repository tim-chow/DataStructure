#coding: utf8

def quick_sort(array, start=None, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(array) - 1

    if start >= end:
        return

    pivot = array[start]
    pos = start
    for ind in range(start+1, end+1):
        if array[ind] >= pivot:
            continue
        array[pos] = array[ind]
        #把array(pos+1...ind-1) 右移一位到 array(pos+2...ind)
        for ind1 in range(ind, pos+2-1, -1):
            array[ind1] = array[ind1-1]
        pos = pos + 1
        array[pos] = pivot

    quick_sort(array, start, pos-1)
    quick_sort(array, pos+1, end)

if __name__ == "__main__":
    import random
    array = range(50)
    random.shuffle(array)
    print array
    quick_sort(array)
    print array
