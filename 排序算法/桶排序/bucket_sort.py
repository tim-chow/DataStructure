class BucketSort:
    @classmethod
    def bucket_sort(cls, array, m, devide, sort):
        n = len(array)
        buckets = [[] for _ in range(m)]

        for element in array:
            buckets[devide(element)].append(element)

        for bucket in buckets:
            sort(bucket)

        cursor = 0
        for i in range(m):
            for element in buckets[i]:
                array[cursor] = element
                cursor = cursor + 1

if __name__ == "__main__":
    def bubble_sort(array):
        for i in range(len(array)-1):
            for j in range(i+1, len(array)):
                if array[j] < array[i]:
                    array[i], array[j] = array[j], array[i]

    def devide(element):
        if element < 10:
            return 0
        if element < 15:
            return 1
        if element < 20:
            return 2
        return 3

    import random
    lst = range(25)
    random.shuffle(lst)
    print lst
    BucketSort.bucket_sort(lst, 4, devide, bubble_sort)
    print lst

