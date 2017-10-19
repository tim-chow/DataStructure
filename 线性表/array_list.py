#coding: utf8

class ArrayList(object):
    def __init__(self, initialize_size=16, capacity_factor=2):
        self._initialize_size = initialize_size
        self._capacity_factor = capacity_factor

        self._array = [None] * initialize_size
        self._total_size = initialize_size
        self._used_size = 0

    def _ensure_capacity(self, increased_size):
        self._total_size = self._total_size + increased_size
        new_array = [None] * self._total_size
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
        if index >= self._used_size:
            index = self._used_size

        for ind in range(self._used_size, index, -1):
            self._array[ind] = self._array[ind-1]
        self._array[index] = element
        self._used_size = self._used_size + 1

    def delete(self, index):
        if index < 0 or index >= self._used_size:
            raise IndexError("invalid index")

        removed_element = self._array[index]
        # move [index+1 ... used_size-1] ---> [index, used_size-2]
        for i in range(index, self._used_size - 2 + 1):
            self._array[i] = self._array[i+1]

        self._used_size = self._used_size - 1
        return removed_element

    def add(self, element):
        self._will_ensure_capacity()
        self._array[self._used_size] = element
        self._used_size = self._used_size + 1
        return self

    def set(self, index, element):
        self._array[index] = element

    def get(self, index):
        return self._array[index]

    def __str__(self):
        return ", ".join(map(str, self._array[: self._used_size]))

    def size(self):
        return self._used_size

    def find(self, element):
        for index in range(self._used_size):
            if self._array[index] == element:
                return index
        return -1

class Iterator:
    def __init__(self, collection):
        self._collection = collection
        self._cursor = 0

    def __iter__(self):
        return self

    def rewind(self):
        self._cursor = 0

    def next(self):
        size = self._collection.size()
        if self._cursor >= size:
            raise StopIteration("over")

        try:
            return self._collection.get(self._cursor)
        finally:
            self._cursor = self._cursor + 1

if __name__ == "__main__":
    list = ArrayList(4, 2)
    list.insert(0, 100)
    list.insert(0, 50)
    list.insert(-1, 0)
    list.insert(100, 150)
    print list.find(150)

