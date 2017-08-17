#coding: utf8

def partition(array, start, end):
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
    return pos

def quick_sort(array, start=None, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(array) - 1

    if start >= end:
        return

    pos = partition(array, start, end)
    quick_sort(array, start, pos-1)
    quick_sort(array, pos+1, end)

class Frame:
    def __init__(self, return_address, array, start=None, end=None):
        self._return_address = return_address
        self._array = array
        self._start = 0 if start is None else start
        self._end = (len(array) - 1) if end is None else end
        self._pos = None

    def execute(self, return_address, return_value):
        if return_address == 0:
            if self._start >= self._end:
                return
            self._pos = partition(self._array, self._start, self._end)
            return Frame(1, self._array, self._start, self._pos-1)
        elif return_address == 1:
            return Frame(2, self._array, self._pos+1, self._end)
        return

    def get_result(self):
        return

    def get_return_address(self):
        return self._return_address

def generate_array():
    import random
    array = range(50)
    random.shuffle(array)
    return array

def test1():
    array = generate_array()
    print array
    quick_sort(array)
    print array

def test2():
    array = generate_array()
    print array

    address, value = 0, None
    stack = [Frame(0, array)]

    while stack:
        active_frame = stack[-1]
        next_frame = active_frame.execute(address, value)
        if next_frame is None:
            frame = stack.pop(-1)
            address = frame.get_return_address()
            value = frame.get_result()
        else:
            stack.append(next_frame)
            address, value = 0, None
    print array

if __name__ == "__main__":
    test2()

