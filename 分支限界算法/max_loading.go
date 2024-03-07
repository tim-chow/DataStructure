package main

import "fmt"

func MaxLoading(weights []int, c1, c2 int) bool {
	if len(weights) == 0 {
		return true
	}
	// remaining[i] 表示装完第 i 个元素之后，仍然剩余的重量
	remaining := make([]int, len(weights))
	sum := weights[len(weights)-1]
	for i := len(weights) - 2; i >= 0; i-- {
		remaining[i] = weights[i+1] + remaining[i+1]
		sum += weights[i]
	}

	// 0 表示重量为 0，-1 表示 Dummy 节点，是每一层的分隔符
	queue := []int{0, -1}
	for ind := 0; ind < len(weights); ind++ {
		node := queue[0]
		queue = queue[1:]
		for node != -1 {
			// 列出所有孩子节点

			// 情况 1：能装下
			if node+weights[ind] <= c1 {
				queue = append(queue, node+weights[ind])
			}
			// 情况 2：可以不装
			if node+weights[ind]+remaining[ind] > c1 {
				queue = append(queue, node)
			}
			node = queue[0]
			queue = queue[1:]
		}
		// 在每一层的末尾防止 Dummy 节点
		queue = append(queue, -1)
	}

	// 获取 c1 最多能装多少
	best := 0
	// 最后一个节点是 Dummy 节点，去掉
	for ind := 0; ind < len(queue)-1; ind++ {
		if queue[ind] > best {
			best = queue[ind]
		}
	}
	fmt.Printf("best: %d\n", best)

	// 总重量减去 c1 必须小于或等于 c2，才能装载
	return sum-best <= c2
}

func main() {
	tests := []struct {
		weights  []int
		c1       int
		c2       int
		expected bool
	}{
		{
			[]int{20, 28, 25, 25},
			70,
			30,
			true,
		},
	}

	for _, test := range tests {
		got := MaxLoading(test.weights, test.c1, test.c2)
		if got != test.expected {
			fmt.Printf("got %v, but %v expected\n", got, test.expected)
			panic("should equal")
		}
	}
}
