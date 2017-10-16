class MergeSort:
    @staticmethod
    def merge(array, start, mid, end):
        if not (start <= mid <= end):
            return
        i, j = start, mid + 1
        temp_list = [None] * (end - start + 1)
        cursor = 0

        while i <= mid and j <= end:
            if array[i] <= array[j]:
                temp_list[cursor] = array[i]
                i = i + 1
            else:
                temp_list[cursor] = array[j]
                j = j + 1
            cursor = cursor + 1

        while i <= mid:
            temp_list[cursor] = array[i]
            i = i + 1
            cursor = cursor + 1

        while j <= end:
            temp_list[cursor] = array[j]
            j = j + 1
            cursor = cursor + 1

        for ind, element in enumerate(temp_list):
            array[start + ind] = element

    @classmethod
    def merge_sort_recursive(cls, array, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = len(array) - 1
        if start >= end:
            return

        mid = (end + start) / 2
        cls.merge_sort_recursive(array, start, mid)
        cls.merge_sort_recursive(array, mid+1, end)
        cls.merge(array, start, mid, end)

    @classmethod
    def merge_sort(cls, array):
        step = 1
        while step <= len(array):
            step = step * 2
            for start in range(0, len(array), step):
                end = start + step - 1
                mid = (start + end) / 2
                if end >= len(array):
                    end = len(array) - 1
                    mid = min(start + step / 2 - 1, end)
                cls.merge(array, start, mid, end)

if __name__ == "__main__":
    import random
    lst = range(30)
    random.shuffle(lst)
    print lst
    MergeSort.merge_sort(lst)
    print lst

