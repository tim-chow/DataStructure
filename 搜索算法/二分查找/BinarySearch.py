def binary_search_recursive(array, target, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high = len(array) - 1

    if low > high:
        return -1

    mid = (low + high) / 2
    if target == array[mid]:
        return mid
    if target < array[mid]:
        return binary_search_recursive(array, target, low, mid - 1)
    return binary_search_recursive(array, target, mid + 1, high)


def binary_search(array, target):
    low = 0
    high = len(array) - 1

    while low <= high:
        mid = (low + high) / 2
        if target == array[mid]:
            return mid
        elif target < array[mid]:
            high = mid - 1
        else:
            low = mid + 1

    return -1


def test():
    array = list(range(20))
    for ind, element in enumerate(array):
        assert binary_search(array, element) == ind
        assert binary_search_recursive(array, element) == ind
    assert binary_search(array, -1) == -1


if __name__ == "__main__":
    test()
