package main

import "fmt"

// ZeroOneKnapsack 是 01 背包问题的实现
func ZeroOneKnapsack(capacity int, weights []int, values []int) int {
	// 创建，同时初始化 dp 数组
	dp := make([]int, capacity+1)
	for i := 0; i < len(dp); i++ {
		dp[i] = 0
	}

	// 01 背包问题的状态转移方程（空间优化前）：
	// dp[i][j] = max(dp[i-1][j], dp[i-1][j-weights[i-1]] + values[i-1])  // j >= weights[i-1]

	for i := 1; i <= len(weights); i++ {
		// 对于 01 背包问题，必须逆向枚举，防止覆盖
		for j := capacity; j >= weights[i-1]; j-- {
			// 空间优化后的状态转移方程
			chooseI := dp[j-weights[i-1]] + values[i-1]
			if chooseI > dp[j] {
				dp[j] = chooseI
			}
		}
	}

	return dp[capacity]
}

func UnboundedKnapsack(capacity int, weights []int, values []int) int {
	// 创建，同时初始化 dp 数组
	dp := make([]int, capacity+1)
	for i := 0; i < len(dp); i++ {
		dp[i] = 0
	}

	// 完全背包问题的状态转移方程（空间优化前）：
	// dp[i][j] = max(dp[i-1][j], dp[i][j-weights[i-1]] + values[i-1])  // j >= weights[i-1]

	for i := 1; i <= len(weights); i++ {
		// 对于完全背包问题，必须正向枚举
		for j := weights[i-1]; j <= capacity; j++ {
			// 空间优化后的状态转移方程
			chooseI := dp[j-weights[i-1]] + values[i-1]
			if chooseI > dp[j] {
				dp[j] = chooseI
			}
		}
	}

	return dp[capacity]
}

func BoundedKnapsack(capacity int, weights []int, values []int, nums []int) int {
	// 创建，同时初始化 dp 数组
	dp := make([]int, capacity+1)
	for i := 0; i < len(dp); i++ {
		dp[i] = 0
	}

	// 多重背包问题的状态转移方程（空间优化前）：
	// 0 <= k <= min(nums[i-1], j / weights[i-1])
	// dp[i][j] = max({dp[i-1][j-k*values[i-1]] + k*values[i-1]} for every k)

	for i := 1; i <= len(weights); i++ {
		// 对于完全背包问题，必须逆向枚举，防止覆盖
		for j := capacity; j >= weights[i-1]; j-- {
			kMax := j / weights[i-1]
			if nums[i-1] < kMax {
				kMax = nums[i-1]
			}
			for k := 0; k <= kMax; k++ {
				// 空间优化后的状态转移方程
				value := dp[j-k*weights[i-1]] + k*values[i-1]
				if value > dp[j] {
					dp[j] = value
				}
			}
		}
	}

	return dp[capacity]
}

func main() {
	capacity := 15
	weights := []int{3, 2, 5, 7, 3, 8}
	values := []int{4, 4, 8, 10, 3, 11}
	// 输出：23
	fmt.Println(ZeroOneKnapsack(capacity, weights, values))
	// 输出：28
	fmt.Println(UnboundedKnapsack(capacity, weights, values))
	nums := []int{1, 100, 1000, 1, 1, 1}
	// 输出：28
	fmt.Println(BoundedKnapsack(capacity, weights, values, nums))
}

