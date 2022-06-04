package main

import "fmt"

type Node struct {
	row       int
	column    int
	isWall    bool
	neighbors []*Node
	cursor    int
}

func (n *Node) IsWall() bool {
	return n.isWall
}

func (n *Node) Row() int {
	return n.row
}

func (n *Node) Column() int {
	return n.column
}

func (n *Node) AddNeighbor(neighbor *Node) {
	if neighbor != nil {
		n.neighbors = append(n.neighbors, neighbor)
	}
}

func (n *Node) GetNextNode() *Node {
	if n.cursor >= len(n.neighbors) {
		return nil
	}
	defer func() {
		n.cursor += 1
	}()
	return n.neighbors[n.cursor]
}

func (n *Node) Is(node *Node) bool {
	if node == nil {
		return false
	}
	return n.row == node.row && n.column == node.column
}

func NewNode(row, column int, isWall bool) *Node {
	return &Node{
		row:    row,
		column: column,
		isWall: isWall,
	}
}

func Search(start, end *Node) [][][]int {
	if start == nil || end == nil {
		panic("invalid start or end point")
	}
	stack := make([]*Node, 0)
	stack = append(stack, start)
	result := make([][][]int, 0)
	for len(stack) > 0 {
		currentExpandNode := stack[len(stack)-1]
		nextNode := currentExpandNode.GetNextNode()
		if nextNode == nil {
			stack = stack[:len(stack)-1]
			continue
		}
		if nextNode.IsWall() {
			continue
		}
		inStack := false
		for _, node := range stack {
			if node.Is(nextNode) {
				inStack = true
				break
			}
		}
		if inStack {
			continue
		}
		if nextNode.Is(end) {
			path := make([][]int, 0)
			for _, node := range stack {
				path = append(path, []int{node.Row(), node.Column()})
			}
			path = append(path, []int{end.Row(), end.Column()})
			result = append(result, path)
			continue
		}
		stack = append(stack, nextNode)
	}
	return result
}

func main() {
	// 0 means wall, 1 means road
	maze := [][]int{
		{0, 0, 0, 0, 0},
		{1, 1, 1, 1, 0},
		{1, 0, 0, 1, 0},
		{1, 1, 0, 1, 0},
		{0, 1, 1, 1, 0},
	}
	allNodes := make([][]*Node, 0)
	for rowIdx, row := range maze {
		nodes := make([]*Node, 0)
		for columnIdx, column := range row {
			nodes = append(nodes, NewNode(rowIdx, columnIdx, column == 0))
		}
		allNodes = append(allNodes, nodes)
	}
	for rowIdx, row := range allNodes {
		for columnIdx, column := range row {
			// 上
			if rowIdx > 0 {
				column.AddNeighbor(allNodes[rowIdx-1][columnIdx])
			}
			// 下
			if rowIdx < len(allNodes)-1 {
				column.AddNeighbor(allNodes[rowIdx+1][columnIdx])
			}
			// 左
			if columnIdx > 0 {
				column.AddNeighbor(allNodes[rowIdx][columnIdx-1])
			}
			// 右
			if columnIdx < len(allNodes[rowIdx])-1 {
				column.AddNeighbor(allNodes[rowIdx][columnIdx+1])
			}
		}
	}
	for _, path := range Search(allNodes[1][1], allNodes[3][1]) {
		fmt.Println(path)
	}
}
