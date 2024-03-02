from typing import List


# 01 背包问题
def zero_one_knapsack(capacity: int, weights: List[int], values: List[int]) -> int:
    # 创建，并且初始化 dp 数组
    dp: List[int] = [0 for _ in range(capacity + 1)]

    # 01 背包问题的状态转移方程（空间优化前）：
    # dp[i][j] = max(dp[i-1][j], dp[i-1][j-weights[i-1]] + values[i-1])  // j >= weights[i-1]

    for i in range(1, len(weights) + 1):
        # 对于 01 背包问题，必须逆向枚举，防止覆盖
        for j in range(capacity, weights[i - 1] - 1, -1):
            # 空间优化后的状态转移方程
            dp[j] = max(dp[j], dp[j - weights[i - 1]] + values[i - 1])
    return dp[capacity]


# 完全背包问题
def unbounded_knapsack(capacity: int, weights: List[int], values: List[int]) -> int:
    # 创建，并且初始化 dp 数组
    dp: List[int] = [0 for _ in range(capacity + 1)]

    # 完全背包问题的状态转移方程（空间优化前）：
    # dp[i][j] = max(dp[i-1][j], dp[i][j-weights[i-1]] + values[i-1])  // j >= weights[i-1]

    for i in range(1, len(weights) + 1):
        # 对于完全背包问题，必须正向枚举
        for j in range(weights[i - 1], capacity + 1):
            # 空间优化后的状态转移方程
            dp[j] = max(dp[j], dp[j - weights[i - 1]] + values[i - 1])
    return dp[-1]


# 多重背包问题
def bounded_knapsack(capacity: int, weights: List[int], values: List[int], nums: List[int]) -> int:
    # 创建，并且初始化 dp 数组
    dp: List[int] = [0 for _ in range(capacity + 1)]

    # 多重背包问题的状态转移方程（空间优化前）：
    # // 0 <= k <= min(j/weights[i-1], nums[i-1])
    # dp[i][j] = max({dp[i-1][j-k*weights[i-1]] + k*values[i-1]} for every k)

    for i in range(1, len(weights) + 1):
        # 对于多重背包问题，必须逆向枚举，防止覆盖
        for j in range(capacity, weights[i - 1] - 1, -1):
            for k in range(0, min(j // weights[i - 1], nums[i - 1]) + 1):
                # 空间优化后的状态转移方程
                dp[j] = max(dp[j], dp[j - k * weights[i - 1]] + k * values[i - 1])

    return dp[capacity]


def test() -> None:
    capacity: int = 15
    weights: List[int] = [3, 2, 5, 7, 3, 8]
    values: List[int] = [4, 4, 8, 10, 3, 11]
    # 输出：23
    print(zero_one_knapsack(capacity, weights, values))
    # 输出：28
    print(unbounded_knapsack(capacity, weights, values))
    nums: List[int] = [1, 100, 1000, 1, 1, 1]
    # 输出：28
    print(bounded_knapsack(capacity, weights, values, nums))


if __name__ == "__main__":
    test()

