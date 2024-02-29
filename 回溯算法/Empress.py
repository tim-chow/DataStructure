from typing import List


def _is_safe(status: List[int], next_: int) -> bool:
    for row in range(next_):
        # 在同一列或同一斜线上不安全
        if status[row] == status[next_] or abs(row - next_) == abs(status[row] - status[next_]):
            return False
    return True


def empress(n: int) -> int:
    result: int = 0
    # 第 i 行的皇后所在的列，元素的取值范围是 0 到 n-1
    status: List[int] = [0] * n
    # 当前正在处理的行，取值范围是 0 到 n-1
    current: int = 0
    while current >= 0:
        # 当前节点是最终状态
        if current == n - 1:
            result += 1
            status[current] += 1
            if current > 0:
                current -= 1
            elif status[current] >= n:
                break
            continue
        next_: int = current + 1
        # 无法继续前进
        if status[next_] >= n:
            status[next_] = 0
            status[current] += 1
            if current > 0:
                current -= 1
            elif status[current] >= n:
                break
            continue
        # 无法到达最终状态
        if not _is_safe(status, next_):
            status[next_] += 1
            continue
        # 只有满足条件才会入栈
        current = next_

    return result


def main() -> None:
    for n in range(1, 11):
        print(n, ":", empress(n))

    # Output:
    # 1 : 1
    # 2 : 0
    # 3 : 0
    # 4 : 2
    # 5 : 10
    # 6 : 4
    # 7 : 40
    # 8 : 92
    # 9 : 352
    # 10 : 724


if __name__ == "__main__":
    main()

