package main

import "fmt"

func inStack(stack [][]int, nextNode []int) bool {
	for _, node := range stack {
		if node[0] == nextNode[0] && node[1] == nextNode[1] {
			return true
		}
	}
	return false
}

func copyPath(stack [][]int, end []int) [][]int {
	var path [][]int
	for _, node := range stack {
		path = append(path, node)
	}
	path = append(path, end)
	return path
}

// Search 搜索指定的迷宫中的全部路径
func Search(maze [][]int, start, end []int) [][][]int {
	var result [][][]int

	// 1 代表上面的格子待搜索；
	// 2 代表右面的格子待搜索
	// 3 代表下面的格子待搜索
	// 4 代表左面的格子待搜索
	// 5 代表上下左右都已搜索
	// 初始值为 1
	var status [][]int
	for i := 0; i < len(maze); i++ {
		status = append(status, nil)
		for j := 0; j < len(maze[i]); j++ {
			status[i] = append(status[i], 1)
		}
	}

	// 栈中保存格子的坐标
	var stack [][]int
	// 将起点压入栈顶
	stack = append(stack, start)
	for len(stack) > 0 {
		currentExpandNode := stack[len(stack)-1]
		x, y := currentExpandNode[0], currentExpandNode[1]
		var nextNode []int
		switch status[x][y] {
		case 1:
			status[x][y] = 2
			if x == 0 {
				continue
			}
			nextNode = []int{x - 1, y}
		case 2:
			status[x][y] = 3
			if y == len(maze[x])-1 {
				continue
			}
			nextNode = []int{x, y + 1}
		case 3:
			status[x][y] = 4
			if x == len(maze)-1 {
				continue
			}
			nextNode = []int{x + 1, y}
		case 4:
			status[x][y] = 5
			if y == 0 {
				continue
			}
			nextNode = []int{x, y - 1}
		default:
			// 无法继续向纵深方向前进
			// 恢复状态
			status[x][y] = 1
			// 将死节点从栈中弹出
			stack = stack[:len(stack)-1]
			continue
		}

		x, y = nextNode[0], nextNode[1]
		// 新节点是墙
		if maze[x][y] == 0 {
			continue
		}
		// 已经在栈中
		if inStack(stack, nextNode) {
			continue
		}
		// 到达终点
		if x == end[0] && y == end[1] {
			result = append(result, copyPath(stack, end))
			continue
		}
		// 使之成为活结点
		stack = append(stack, nextNode)
	}

	return result
}

func main() {
	// 0 代表墙；1 代表路
	maze := [][]int{
		{0, 0, 0, 0, 0},
		{1, 1, 1, 1, 0},
		{1, 0, 0, 1, 0},
		{1, 1, 0, 1, 0},
		{0, 1, 1, 1, 0},
	}
	for _, path := range Search(maze, []int{1, 0}, []int{3, 0}) {
		fmt.Println(path)
	}
}

