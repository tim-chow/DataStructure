class ShellSort:
    @staticmethod
    def group_sort(array, gap):
        n = len(array)
        for i in range(n - gap):
            j = 1
            while (i + gap * j) < n:
                for p in range(j):
                    if array[i + gap * j] >= array[i + gap * p]:
                        continue
                    temp = array[i + gap * j]
                    for q in range(j, p, -1):
                        array[i + gap * q] = array[i + gap * (q - 1)]
                    array[i + gap * p] = temp
                    break
                j = j + 1

    @classmethod
    def shell_sort(cls, array):
        gap = len(array) / 2
        while gap >= 1:
            cls.group_sort(array, gap)
            gap = gap / 2

if __name__ == "__main__":
    import random
    lst = range(20)
    random.shuffle(lst)
    print lst
    ShellSort.shell_sort(lst)
    print lst

