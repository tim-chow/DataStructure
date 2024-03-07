// leetcode：https://leetcode.cn/problems/word-search/description/

package main

import (
	"fmt"
)

func inStack(stack [][]int, node []int) bool {
	for _, ele := range stack {
		if ele[0] == node[0] && ele[1] == node[1] {
			return true
		}
	}
	return false
}

func exist(board [][]byte, word string) bool {
	row := len(board)
	col := len(board[0])

	var starts [][]int
	for i := 0; i < row; i++ {
		for j := 0; j < col; j++ {
			if board[i][j] == word[0] {
				starts = append(starts, []int{i, j})
			}
		}
	}

	for _, start := range starts {
		// status[i][j] 保存 board[i][j] 的状态。
		// 1 表示上；2 表示右；3 表示下；4 表示左。初始值为 1
		var status [][]int
		for i := 0; i < row; i++ {
			var oneRow []int
			for j := 0; j < col; j++ {
				oneRow = append(oneRow, 1)
			}
			status = append(status, oneRow)
		}

		stack := [][]int{start}
		for len(stack) > 0 {
			// 当前扩展节点
			currentExpandNode := stack[len(stack)-1]
			if len(stack) == len(word) {
				return true
			}
			x, y := currentExpandNode[0], currentExpandNode[1]
			// 找下一个节点
			var nextNode []int
			if status[x][y] > 4 {
				// 当前扩展节点成为死节点
				// 重置状态
				status[x][y] = 1
				stack = stack[:len(stack)-1]
				continue
			}
			switch status[x][y] {
			case 1:
				status[x][y] += 1
				if x == 0 {
					continue
				}
				nextNode = []int{x - 1, y}
			case 2:
				status[x][y] += 1
				if y == col-1 {
					continue
				}
				nextNode = []int{x, y + 1}
			case 3:
				status[x][y] += 1
				if x == row-1 {
					continue
				}
				nextNode = []int{x + 1, y}
			case 4:
				status[x][y] += 1
				if y == 0 {
					continue
				}
				nextNode = []int{x, y - 1}
			}
			// 剪枝
			x, y = nextNode[0], nextNode[1]
			// 1. 判断是否已经在栈中
			if inStack(stack, nextNode) {
				continue
			}
			// 2. nextNode 对应的字符应该等于 word 的第 len(stack) + 1 个字符
			if board[x][y] != word[len(stack)] {
				continue
			}
			stack = append(stack, nextNode)
		}
	}

	return false
}

func main() {
	tests := []struct {
		board    [][]byte
		word     string
		expected bool
	}{
		{
			board: [][]byte{
				{'A', 'B', 'C', 'E'},
				{'S', 'F', 'C', 'S'},
				{'A', 'D', 'E', 'E'},
			},
			word:     "ABCCED",
			expected: true,
		},
	}
	for _, test := range tests {
		got := exist(test.board, test.word)
		if got != test.expected {
			fmt.Printf("got %v, but %v expected\n", got, test.expected)
			panic("should equal")
		}
	}
}
