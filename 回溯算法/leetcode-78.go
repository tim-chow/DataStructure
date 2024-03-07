// leetcode：https://leetcode.cn/problems/subsets/description/

package main

import (
	"fmt"
	"reflect"
)

func subsets(nums []int) [][]int {
	var result [][]int

	n := len(nums)
	// status 用于保存状态。status[i] 表示 nums 中第 i 个元素（从 0 开始）的起点
	status := make([]int, n+1)
	for i := 0; i < n; i++ {
		status[i] = i + 1
	}
	// n 的起点是 0
	status[n] = 0

	stack := []int{n}
	for len(stack) > 0 {
		// 当前扩展起点
		currentExpandNode := stack[len(stack)-1]
		// 如果无法继续前进
		if status[currentExpandNode] > n-1 {
			// 那么当前扩展节点成为死节点
			// 输出答案
			oneAns := make([]int, 0)
			for i := 1; i < len(stack); i++ {
				oneAns = append(oneAns, nums[stack[i]])
			}
			result = append(result, oneAns)
			// 将其从栈中弹出
			stack = stack[:len(stack)-1]
			// 重置状态
			if currentExpandNode == n {
				status[currentExpandNode] = 0
			} else {
				status[currentExpandNode] = currentExpandNode + 1
			}
			continue
		}
		nextNode := status[currentExpandNode]
		status[currentExpandNode] += 1
		stack = append(stack, nextNode)
	}

	return result
}

func equalOutOfOrder(x, y [][]int) bool {
	for _, xe := range x {
		isIn := false
		for _, ye := range y {
			if reflect.DeepEqual(xe, ye) {
				isIn = true
				break
			}
		}
		if !isIn {
			return false
		}
	}
	return true
}

func main() {
	tests := []struct {
		nums     []int
		expected [][]int
	}{
		{
			nums: []int{1, 2, 3},
			expected: [][]int{
				{1, 2, 3},
				{1, 2},
				{1, 3},
				{1},
				{2, 3},
				{2},
				{3},
				{},
			},
		},
		{
			nums:     []int{0},
			expected: [][]int{{0}, {}},
		},
	}

	for _, test := range tests {
		got := subsets(test.nums)
		if !equalOutOfOrder(got, test.expected) {
			fmt.Printf("got %v, but %v expected\n", got, test.expected)
			panic("should equal out of order")
		}
	}
}
