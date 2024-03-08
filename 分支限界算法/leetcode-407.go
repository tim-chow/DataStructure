// leetcode：https://leetcode.cn/problems/trapping-rain-water-ii/description/

package main

import (
	"container/heap"
	"fmt"
)

// 问题分析：
//
// 1. 路径是一个节点序列，路径中的两个相邻的节点必须相邻接。
// 比如 [(0, 0), (0, 1), (1, 1), (1, 2)] 是路径；而 [(0, 0), (1, 1)] 不是，因为它的前两个节点不邻接
// 2. 在本题的上下文中，路径的起点必须是边缘。由此可以进一步得到，[(1, 1), (1, 2), (2, 2), (2, 3)] 不是路径，因为其起点不是边缘
// 3. 将路径上最高的节点的高度称为路径的高度。
// 假如 [(x1, x2), ...(xi, yi)] 的路径高度是 heightI，
// 那么 [(x1, x2), ...(xi, yi), (xi, yi+1)] 的路径高度是 max(heightI, Height[(xi, yi+1)])
// 4. 对于任何一个节点而言，到达它的路径有很多，但是必然存在一个或多个路径高度最低的路径，记其为 minPath。
// 该节点能否接雨水，以及接多少取决于自身的高度（记为 h）与 minPath 的高度（记为 minPathHeight）。
// 如果 h >= minPathHeight，那么无法接雨水，因为雨水将沿着 minPath 从边缘流出；
// 否则可以接雨水，由于所有其它路径的高度都大于或等于 minPath 的高度，根据木桶原理，该节点能接的雨水为 minPathHeight - h。
// 由此，也可以得到，边缘无法接雨水
// 5. 根据 4，如果可以保证第一次搜索到节点 i 时，走的是 minPath。那么在第一次搜索到 i 时，就可以计算出 i 接的雨水。
// 那么如何做到呢？
// **从边缘开始，每次都从路径高度最低的节点以广度优先的方式进行搜索。**
// **同时需要保证，每个节点只被访问一次**

// 结论：
//
// 使用分支限界算法

// Item 表示优先级队列中的元素
type Item struct {
	X int
	Y int
	// 点 (x, y) 的路径高度。Height 越小，优先级越高
	Height int
}

// PriorityQueue 是基于 MinHeap 的优先级队列
type PriorityQueue []Item

func (pq PriorityQueue) Len() int           { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].Height < pq[j].Height }
func (pq PriorityQueue) Swap(i, j int)      { pq[i], pq[j] = pq[j], pq[i] }

func (pq *PriorityQueue) Push(x interface{}) {
	*pq = append(*pq, x.(Item))
}
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := old[len(old)-1]
	*pq = old[:len(old)-1]
	return n
}

// NewPriorityQueue 构造 PriorityQueue 实例
func NewPriorityQueue() PriorityQueue {
	return make(PriorityQueue, 0)
}

func trapRainWater(heightMap [][]int) int {
	var ans = 0
	m := len(heightMap)
	n := len(heightMap[0])

	queue := NewPriorityQueue()
	// 记录每个节点是否已经访问过
	visited := make([][]bool, m)
	// 将所有边缘加入队列，并且设置为已访问
	for x := 0; x < m; x++ {
		oneRow := make([]bool, n)
		for y := 0; y < n; y++ {
			if x == 0 || x == m-1 || y == 0 || y == n-1 {
				heap.Push(&queue, Item{
					X:      x,
					Y:      y,
					Height: heightMap[x][y],
				})
				oneRow[y] = true
			} else {
				oneRow[y] = false
			}
		}
		visited[x] = oneRow
	}

	for len(queue) > 0 {
		currentExpandNode := heap.Pop(&queue).(Item)
		x, y, height := currentExpandNode.X, currentExpandNode.Y, currentExpandNode.Height
		// 向上下左右四个方向广度优先遍历
		for _, nextNode := range [][]int{{x - 1, y}, {x, y + 1}, {x + 1, y}, {x, y - 1}} {
			tx, ty := nextNode[0], nextNode[1]
			// 如果该点存在，并且未被访问过
			if tx >= 0 && tx < m && ty >= 0 && ty < n && !visited[tx][ty] {
				// 高度较低，可以接雨水
				if heightMap[tx][ty] < height {
					ans += height - heightMap[tx][ty]
					heap.Push(&queue, Item{X: tx, Y: ty, Height: height})
				} else {
					heap.Push(&queue, Item{X: tx, Y: ty, Height: heightMap[tx][ty]})
				}
				// 设置为已访问
				visited[tx][ty] = true
			}
		}
	}

	return ans
}

func main() {
	tests := []struct {
		heightMap [][]int
		expected  int
	}{
		{
			heightMap: [][]int{{1, 4, 3, 1, 3, 2}, {3, 2, 1, 3, 2, 4}, {2, 3, 3, 2, 3, 1}},
			expected:  4,
		},
		{
			heightMap: [][]int{{3, 3, 3, 3, 3}, {3, 2, 2, 2, 3}, {3, 2, 1, 2, 3}, {3, 2, 2, 2, 3}, {3, 3, 3, 3, 3}},
			expected:  10,
		},
	}
	for _, test := range tests {
		got := trapRainWater(test.heightMap)
		if got != test.expected {
			message := fmt.Sprintf("got %d, but %d expected", got, test.expected)
			fmt.Println(message)
			panic(message)
		}
	}
}
