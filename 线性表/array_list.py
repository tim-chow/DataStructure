# coding: utf8


class ArrayList(object):
    """
    顺序表实现
    """
    def __init__(self, initialize_size=16, capacity_factor=2):
        """
        :param initialize_size: 初始容量
        :param capacity_factor: 扩容因子
        """
        self._initialize_size = initialize_size
        self._capacity_factor = capacity_factor
        self._array = [None] * initialize_size
        self._total_size = initialize_size
        self._used_size = 0

    def _ensure_capacity(self, increased_size):
        self._total_size = self._total_size + increased_size
        new_array = [None] * self._total_size

        # 将旧数组中的元素拷贝到新数组
        for ind in range(self._used_size):
            new_array[ind] = self._array[ind]

        self._array = new_array

    def _will_ensure_capacity(self):
        if self._used_size < self._total_size:
            return
        self._ensure_capacity(
            self._initialize_size * self._capacity_factor)

    def insert(self, index, element):
        self._will_ensure_capacity()

        if index < 0:
            index = 0
        if index > self._used_size:
            index = self._used_size

        # 将 array[index...used_size-1] 移动到 array[index+1...used_size]
        for ind in range(self._used_size, index, -1):
            self._array[ind] = self._array[ind - 1]

        self._array[index] = element
        self._used_size = self._used_size + 1

    def delete(self, index):
        if index < 0 or index >= self._used_size:
            raise IndexError("invalid index")

        removed_element = self._array[index]
        # 将 array[index+1...used_size-1] 移动到 array[index, used_size-2]
        for ind in range(index, self._used_size - 2 + 1):
            self._array[ind] = self._array[ind + 1]

        self._used_size = self._used_size - 1
        return removed_element

    def set(self, index, element):
        self._array[index] = element

    def get(self, index):
        return self._array[index]

    def size(self):
        return self._used_size

    def find(self, element):
        for index in range(self._used_size):
            if self._array[index] == element:
                return index
        return -1


class Iterator(object):
    def __init__(self, collection):
        self._collection = collection
        self._cursor = 0

    def __iter__(self):
        return self

    def rewind(self):
        self._cursor = 0

    def next(self):
        if self._cursor >= self._collection.size():
            raise StopIteration("over")

        try:
            return self._collection.get(self._cursor)
        finally:
            self._cursor = self._cursor + 1


if __name__ == "__main__":
    array_list = ArrayList(4, 2)
    array_list.insert(0, 100)
    array_list.insert(0, 50)
    array_list.insert(-1, 0)
    array_list.insert(100, 150)
    print(array_list.find(150))
