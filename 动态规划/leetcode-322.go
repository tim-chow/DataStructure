// leetcode：https://leetcode.cn/problems/coin-change/description/

package main

import (
	"fmt"
	"math"
)

func coinChange(coins []int, amount int) int {
	// 将原问题转换成恰好装满的完全背包问题。状态转移方程是：
	// // dp[i][j] 表示将前 i 种（i 从 1 开始）硬币兑换成金额 j 时，所需的最小硬币数量
	// // j >= coins[i-1]
	// dp[i][j] = min(dp[i-1][j], dp[i-1][j-coins[i-1]] + 1)
	// 空间优化后的状态转移方程是：
	// dp[j] = min(dp[j], dp[j-coins[i-1]] + 1)
	N := len(coins)
	W := amount
	dp := make([]int, W+1)
	// 将前 0 种硬币兑换成金额 0 时，需要的最小硬币数量是 0；
	// 其它情况均没有合法解，因此设为 MaxInt
	dp[0] = 0
	for i := 1; i <= W; i++ {
		dp[i] = math.MaxInt
	}

	for i := 1; i <= N; i++ {
		for j := coins[i-1]; j <= W; j++ {
			// 防止溢出
			if dp[j]-1 > dp[j-coins[i-1]] {
				dp[j] = dp[j-coins[i-1]] + 1
			}
		}
	}

	if dp[W] == math.MaxInt {
		return -1
	} else {
		return dp[W]
	}
}

func main() {
	tests := []struct {
		coins    []int
		amount   int
		expected int
	}{
		{[]int{1, 2, 5}, 11, 3},
		{[]int{2}, 3, -1},
		{[]int{1}, 0, 0},
	}

	for _, test := range tests {
		result := coinChange(test.coins, test.amount)
		if result != test.expected {
			panic(fmt.Sprintf("coins: %v, amout: %d got %v, but %v expected",
				test.coins, test.amount, result, test.expected))
		}
	}
}

