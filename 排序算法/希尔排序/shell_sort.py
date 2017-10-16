class ShellSort:
    @staticmethod
    def tee(size, batch, start=0):
        offset = start
        while offset <= start + size - 1:
            end = offset + batch - 1
            if end > start + size - 1:
                end = start + size - 1
            yield offset, end
            offset = end + 1

    @staticmethod
    def shell_insertion_sort(array, start, end):
        for i in range(start+1, end+1):
            for j in range(start, i):
                if array[i] >= array[j]:
                    continue
                sentinel = array[i]
                # move array[j...i-1] ---> array[j+1...i]
                for k in range(i, j, -1):
                    array[k] = array[k-1]
                array[j] = sentinel

    @classmethod
    def shell_sort(cls, array):
        for batch in [3, 5, len(array)]:
            for start, end in cls.tee(len(array), batch, 0):
                cls.shell_insertion_sort(array, start, end)
            print batch, ":", array

if __name__ == "__main__":
    import random
    lst = range(20)
    random.shuffle(lst)
    print "input: ", lst
    ShellSort.shell_sort(lst)
    print "output: ", lst

