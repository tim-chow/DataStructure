package main

import "fmt"

func merge(a []int, start, mid, end int) {
	// 前提：a[start...mid] 有序，a[mid+1...end]有序
	// 目标：使 a[start...end] 有序

	// 临时数组
	temp := make([]int, end-start+1)
	cursor := 0
	i := start
	j := mid + 1
	for i <= mid && j <= end {
		if a[i] < a[j] {
			temp[cursor] = a[i]
			i += 1
		} else {
			temp[cursor] = a[j]
			j += 1
		}
		cursor += 1
	}
	for ; i <= mid; i++ {
		temp[cursor] = a[i]
		cursor += 1
	}
	for ; j <= end; j++ {
		temp[cursor] = a[j]
		cursor += 1
	}

	for i := 0; i < len(temp); i++ {
		a[i+start] = temp[i]
	}
}

func mergeSort(a []int, start, end int) {
	if end <= start {
		return
	}
	mid := (start + end) / 2
	mergeSort(a, start, mid)
	mergeSort(a, mid+1, end)
	merge(a, start, mid, end)
}

func MergeSort(a []int) {
	mergeSort(a, 0, len(a)-1)
}

func main() {
	a := []int{3, 2, 9, -1, 88, 66, 1, 33, -3, 33, 88, 2, 9, 3}
	MergeSort(a)
	fmt.Println(a)
}
