def dp(string):
    p = []
    for ind in range(len(string)):
        p.append([])
        for _ in range(len(string)):
            p[ind].append(None)

    def _dp(i, j):
        if p[i][j] is not None:
            return p[i][j]
        if i > j:
            p[i][j] = False
            return False
        if i == j:
            p[i][j] = True
            return True
        if string[i] != string[j]:
            p[i][j] = False
            return False
        if j == i + 1:
            p[i][j] = True
            return True
        p[i][j] = _dp(i + 1, j - 1)
        return p[i][j]

    for i in range(len(string)):
        for j in range(len(string) - 1, i - 1, -1):
            _dp(i, j)

    longest = None
    for i in range(len(p)):
        for j in range(len(p[i]) - 1, i - 1, -1):
            if p[i][j] is not None and p[i][j]:
                if longest is None or (j - i) > longest[1] - longest[0]:
                    longest = i, j

    return longest


if __name__ == "__main__":
    print(dp("abba2c1abba1d1"))
