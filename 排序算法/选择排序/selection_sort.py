class SelectionSort:
    @classmethod
    def selection_sort(cls, array):
        n = len(array)
        for i in range(n/2):
            start = i
            end = n - i - 1
            min, max = cls.select_min_and_max(array, start, end)
            array[start], array[min] = array[min], array[start]
            array[end], array[max] = array[max], array[end]

    @staticmethod
    def select_min_and_max(array, start, end):
        if start > end:
            raise RuntimeError("start > end")
        min = start
        max = start

        for ind in range(start, end+1):
            if array[ind] < array[min]:
                min = ind
            if array[ind] > array[max]:
                max = ind
        return min, max

if __name__ == "__main__":
    import random
    lst = range(20)
    random.shuffle(lst)
    print lst
    SelectionSort.selection_sort(lst)
    print lst

