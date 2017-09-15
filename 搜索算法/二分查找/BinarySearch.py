def binary_search(array, element):
    low, high = 0, len(array) - 1

    while low <= high:
        mid = (low + high) / 2
        if array[mid] == element:
            return mid, mid
        if array[mid] > element:
            if mid == low or \
                    array[mid - 1] < element:
                return mid-1, mid
            high = mid - 1
            continue
        if mid == len(array) - 1 or \
                array[mid+1] > element:
            return mid, mid+1
        low = mid + 1

def binary_search_recusive(array, element, start=None, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(array) - 1

    if start > end:
        return -1

    mid = (start + end) / 2
    if array[mid] == element:
        return mid
    if array[mid] > element:
        return binary_search_recusive(array, element, start, mid-1)
    return binary_search_recusive(array, element, mid+1, end)

if __name__ == "__main__":
    print binary_search([1, 2, 4, 5, 8, 9, 11, 12, 15], 17)
    print binary_search([1, 2, 4, 5, 8, 9, 11, 12, 15], 15)
    print binary_search([1, 2, 4, 5, 8, 9, 11, 12, 15], 12)
    print binary_search([1, 2, 4, 5, 8, 9, 11, 12, 15], 13)
    print binary_search([1, 2, 4, 5, 8, 9, 11, 12, 15], 8)
    print binary_search([1, 2, 4, 5, 8, 9, 11, 12, 15], 1)
    print binary_search([1, 2, 4, 5, 8, 9, 11, 12, 15], 0)

    print binary_search_recusive([1, 2, 4, 5, 8, 9, 11, 12, 15], 1)

