from typing import List


class Good:
    def __init__(self, weight: int, value: int) -> None:
        self.weight: int = weight
        self.value: int = value


def dp1(goods: List[Good], max_weight: int) -> int:
    # 处理 corner case
    if not goods:
        return 0
    if max_weight <= 0:
        return 0
    # f[i][j] 表示前 i 个物品放入一个容量为 j 的背包可以获得的最大价值
    f: List[List[int]] = [[0 for _ in range(max_weight + 1)] for _ in range(len(goods))]
    # 设置初始状态：当 i = 1 时
    for j in range(goods[0].weight, max_weight + 1):
        f[0][j] = goods[0].value
    # 状态转移方程
    for i in range(1, len(goods)):
        for j in range(1, max_weight + 1):
            # 放不进去
            if goods[i].weight > j:
                f[i][j] = f[i - 1][j]
                continue
            f[i][j] = max(f[i - 1][j], f[i - 1][j - goods[i].weight] + goods[i].value)
    return f[-1][-1]


def dp2(goods: List[Good], max_weight: int) -> int:
    # 处理 corner case
    if not goods:
        return 0
    if max_weight <= 0:
        return 0
    # 使用滚动数组
    f: List[int] = [0 for _ in range(max_weight + 1)]
    # 初始化
    for j in range(goods[0].weight, max_weight + 1):
        f[j] = goods[0].value
    for i in range(1, len(goods)):
        for j in range(max_weight, 0, -1):
            # 放不进去
            if goods[i].weight > j:
                continue
            f[j] = max(f[j], f[j - goods[i].weight] + goods[i].value)
    return f[-1]


def test() -> None:
    goods: List[Good] = [Good(3, 4), Good(2, 4), Good(5, 8), Good(7, 10), Good(3, 3), Good(8, 11)]
    max_weight: int = 15
    print(dp1(goods, max_weight))
    print(dp2(goods, max_weight))


if __name__ == "__main__":
    test()
