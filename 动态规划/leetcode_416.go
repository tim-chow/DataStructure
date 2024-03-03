// leetcode：https://leetcode.cn/problems/partition-equal-subset-sum/description/

package main

import (
	"fmt"
)

func canPartition(nums []int) bool {
	sum := 0
	for _, num := range nums {
		sum += num
	}
	if sum%2 == 1 {
		return false
	}
	W := sum / 2
	N := len(nums)

	// 转换成恰好装满的 01 背包问题。状态转移方程是：
	// dp[i][j] = dp[i-1][j] || dp[i-1][j-nums[i-1]]
	dp := make([]bool, W+1)
	dp[0] = true
	for i := 1; i <= N; i++ {
		for j := W; j >= nums[i-1]; j-- {
			dp[j] = dp[j] || dp[j-nums[i-1]]
		}
	}

	return dp[W]
}

func main() {
	tests := []struct {
		nums     []int
		expected bool
	}{
		{[]int{1, 5, 11, 5}, true},
		{[]int{1, 2, 3, 5}, false},
	}

	for _, test := range tests {
		result := canPartition(test.nums)
		if result != test.expected {
			panic(fmt.Sprintf("nums: %s got %v, but %v expected", test.nums, result, test.expected))
		}
	}
}

