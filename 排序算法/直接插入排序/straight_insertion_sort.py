#coding: utf8

class StraightInsertionSort:
    @staticmethod
    def straight_insertion_sort(array):
        for i in range(1, len(array)):
            for j in range(i):
                if array[i] >= array[j]:
                    continue
                # move array[j...i-1] ---> array[j+1...i]
                sentinal = array[i]
                for k in range(i, j, -1):
                    array[k] = array[k-1]
                array[j] = sentinal
                break

if __name__ == "__main__":
    import random
    lst = range(20)
    random.shuffle(lst)
    print lst
    StraightInsertionSort.straight_insertion_sort(lst)
    print lst

