// leetcode：https://leetcode.cn/problems/regular-expression-matching/description/

package main

import (
	"fmt"
)

func isMatch(s string, p string) bool {
	// dp[i][j] 表示 s 的前 i（从 1 开始）个字符与 p 的前 j（从 1 开始）个字符是否匹配
	// dp[0][0] = true 表示空串与空串匹配
	dp := make([][]bool, len(s)+1)
	for i := 0; i < len(dp); i++ {
		dp[i] = make([]bool, len(p)+1)
	}
	// 初始化 dp 数组
	dp[0][0] = true
	for j := 2; j <= len(p); j++ {
		if p[j-1] == '*' {
			dp[0][j] = dp[0][j-2]
		}
	}

	// 状态转移方程
	for i := 1; i <= len(s); i++ {
		for j := 1; j <= len(p); j++ {
			if p[j-1] == '*' {
				// 如果 j 为 *
				if j >= 2 && dp[i][j-2] {
					// 如果 s[1...i] 与 p[1...j-2] 匹配，那么 dp[i][j] = true。
					// 此时，* 表示重复 p 的第 j-1 个字符 0 次
					dp[i][j] = true
				} else {
					// 如果 s[1...i-1] 与 p[1...j] 匹配，并且 s 的第 i 个字符与 p 的第 j-1 个字符匹配，那么 dp[i][j] = true。
					// 此时，* 的复制能力增加 1
					if dp[i-1][j] && j >= 2 && (p[j-2] == '.' || s[i-1] == p[j-2]) {
						dp[i][j] = true
					}
				}
			} else {
				// 如果 j 不为 *
				if dp[i-1][j-1] && (p[j-1] == '.' || s[i-1] == p[j-1]) {
					// 那么当 s[1...i-1] 和 p[1...j-1] 匹配，并且 s 的第 i 个字符与 p 的第 j 个字符匹配时，dp[i][j] = true
					dp[i][j] = true
				}
			}
		}
	}

	return dp[len(s)][len(p)]
}

func main() {
	tests := []struct {
		s        string
		p        string
		expected bool
	}{
		{"aa", "a", false},
		{"aa", "a*", true},
		{"ab", ".*", true},
	}

	for _, test := range tests {
		result := isMatch(test.s, test.p)
		if result != test.expected {
			panic(fmt.Sprintf("s: %s, p: %s got %v, but %v expected",
				test.s, test.p, result, test.expected))
		}
	}
}

