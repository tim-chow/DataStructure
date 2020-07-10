# coding: utf8


def get_next(pattern):
    next_array = [0] * len(pattern)
    for ind in range(1, len(pattern)):
        j = ind
        while j > 0:
            j = next_array[j - 1]
            if pattern[ind] == pattern[j]:
                next_array[ind] = j + 1
                break
    return next_array


def kmp(main_string, pattern):
    # 计算 next 数组
    next_array = get_next(pattern)

    i = j = 0
    while i < len(main_string):
        if main_string[i] == pattern[j]:
            if j == len(pattern) - 1:
                return i - j
            i = i + 1
            j = j + 1
            continue
        if j == 0:
            i = i + 1
        else:
            j = next_array[j - 1]


if __name__ == "__main__":
    print(kmp("bbaaababaabbaabb", "abaabb"))
