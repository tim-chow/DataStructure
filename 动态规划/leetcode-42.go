// leetcode：https://leetcode.cn/problems/trapping-rain-water/description/

package main

import "fmt"

func trap(height []int) int {
	// 每个柱子能接的雨水与它左面的柱子中最高的（left）、它右面的柱子中最高的（right），以及其自身高度有关：
	// 如果它的高度与 left 和 right 中的任意一个相等或者更高，那么无法接到雨水；
	// 否则，接到的雨水等于 left 和 right 中的较小者与柱子本身的高度之差。
	// 从左向右遍历，获取每根柱子的左面的最高的柱子。
	// 第一根柱子的左面的最高的柱子初始化为 0，第 i 根柱子的左面的最高的柱子是第 i-1 根柱子的左面的最高的柱子和第 i-1 根柱子中的较大者
	left := make([]int, len(height))
	for i := 1; i < len(height); i++ {
		if left[i-1] > height[i-1] {
			left[i] = left[i-1]
		} else {
			left[i] = height[i-1]
		}
	}
	// 从右向左遍历，获取每根柱子的右面的最高的柱子。
	// 最右面的柱子的右面的最高的柱子初始化为 0，第 i 根柱子的右面的最高的柱子是第 i+1 根柱子的右面的最高的柱子和第 i+1 根柱子中的较大者
	right := make([]int, len(height))
	for i := len(height) - 2; i >= 0; i-- {
		if right[i+1] > height[i+1] {
			right[i] = right[i+1]
		} else {
			right[i] = height[i+1]
		}
	}
	sum := 0
	for i := 0; i < len(height); i++ {
		if height[i] >= left[i] || height[i] >= right[i] {
			continue
		}
		if left[i] > right[i] {
			sum += right[i] - height[i]
		} else {
			sum += left[i] - height[i]
		}
	}
	return sum
}

func main() {
	tests := []struct {
		height   []int
		expected int
	}{
		{[]int{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1}, 6},
		{[]int{4, 2, 0, 3, 2, 5}, 9},
	}

	for _, test := range tests {
		result := trap(test.height)
		if test.expected != result {
			panic(fmt.Sprintf("height: %v got %d, but %d expected", test.height, result, test.expected))
		}
	}
}
