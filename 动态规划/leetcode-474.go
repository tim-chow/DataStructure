// leetcode：https://leetcode.cn/problems/ones-and-zeroes/description/

package main

import (
	"fmt"
)

func findMaxForm(strs []string, m int, n int) int {
	// 二维 01 背包
	N := len(strs)
	dp := make([][]int, m+1)
	for i := 0; i < len(dp); i++ {
		dp[i] = make([]int, n+1)
	}

	for i := 1; i <= N; i++ {
		w0 := 0
		w1 := 0
		for _, chr := range strs[i-1] {
			if chr == '0' {
				w0 += 1
			} else {
				w1 += 1
			}
		}
		for j := m; j >= w0; j-- {
			for k := n; k >= w1; k-- {
				chooseI := dp[j-w0][k-w1] + 1
				if chooseI > dp[j][k] {
					dp[j][k] = chooseI
				}
			}
		}
	}
	return dp[m][n]
}

func main() {
	tests := []struct {
		strs     []string
		m        int
		n        int
		expected int
	}{
		{[]string{"10", "0001", "111001", "1", "0"}, 5, 3, 4},
		{[]string{"10", "0", "1"}, 1, 1, 2},
	}

	for _, test := range tests {
		result := findMaxForm(test.strs, test.m, test.n)
		if result != test.expected {
			panic(fmt.Sprintf("strs: %v, m: %d, n: %d got %v, but %v expected",
				test.strs, test.m, test.n, result, test.expected))
		}
	}
}

