class BubbleSort:
    @staticmethod
    def bubble_sort(array):
        size = len(array)
        for i in range(size-1, 0, -1):
            swapped = False
            for j in range(i):
                if array[j] > array[j+1]:
                    swapped = True
                    array[j], array[j+1] = array[j+1], array[j]
            if not swapped:
                break

if __name__ == "__main__":
    import random
    lst = range(20)
    random.shuffle(lst)
    print lst
    BubbleSort.bubble_sort(lst)
    print lst
