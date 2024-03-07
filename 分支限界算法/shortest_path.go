package main

import (
	"container/heap"
	"fmt"
)

// Graph 使用数组矩阵法表示有向图
type Graph struct {
	// 顶点集合
	Vertexes []string
	// 弧的集合
	Arches [][]int
}

// GenerateDirectGraphExample 生成用于测试的有向图
func GenerateDirectGraphExample() *Graph {
	graph := &Graph{}
	graph.Vertexes = []string{"s", "a", "b", "c", "d", "e", "f", "g", "h", "i", "t"}
	graph.Arches = append(graph.Arches, [][]int{
		{0, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 3, 0, 7, 2, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 9, 2, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0},
		{0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2},
		{0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
	}...)
	return graph
}

// Item 表示优先级队列中的元素
type Item struct {
	// 代价
	Weight int
	// 索引
	Index int
}

// PriorityQueue 表示优先级队列
type PriorityQueue []Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool { return pq[i].Weight < pq[j].Weight }

func (pq PriorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }

func (pq *PriorityQueue) Push(x interface{}) {
	*pq = append(*pq, x.(Item))
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	ele := old[len(old)-1]
	*pq = old[:len(old)-1]
	return ele
}

// NewPriorityQueue 构造优先级队列实例
func NewPriorityQueue() PriorityQueue {
	return make(PriorityQueue, 0)
}

// ShortestPath 计算单源最短路径
func ShortestPath(graph *Graph, start int) map[int]int {
	// 顶点的索引 -> 代价
	m := make(map[int]int)
	pq := NewPriorityQueue()
	// 将开始节点加入到优先级队列中
	heap.Push(&pq, Item{Weight: 0, Index: start})
	for len(pq) > 0 {
		// 当前扩展节点
		currentExpandNode := heap.Pop(&pq).(Item)
		// 获取当前扩展节点的所有孩子节点
		for child, weight := range graph.Arches[currentExpandNode.Index] {
			if weight == 0 {
				continue
			}
			newWeight := currentExpandNode.Weight + weight
			// 剪掉无法到达最优解的孩子节点，将其它孩子节点加入到活结点列表，并且使用限界函数进行排序
			if currentWeight, found := m[child]; !found || currentWeight > newWeight {
				m[child] = newWeight
				heap.Push(&pq, Item{Weight: newWeight, Index: child})
			}
		}
	}
	return m
}

func main() {
	graph := GenerateDirectGraphExample()
	startIdx := 0
	for idx, weight := range ShortestPath(graph, startIdx) {
		fmt.Printf("%s -> %s: %d\n", graph.Vertexes[startIdx], graph.Vertexes[idx], weight)
	}
}
