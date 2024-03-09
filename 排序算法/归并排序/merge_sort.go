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

func mergeSortRecursive(a []int, start, end int) {
	if end <= start {
		return
	}
	mid := (start + end) / 2
	mergeSortRecursive(a, start, mid)
	mergeSortRecursive(a, mid+1, end)
	merge(a, start, mid, end)
}

func MergeSortRecursive(a []int) {
	mergeSortRecursive(a, 0, len(a)-1)
}

func MergeSort(a []int) {
	step := 1
	for step <= len(a) {
		step *= 2
		for start := 0; start < len(a); start += step {
			end := start + step - 1
			mid := (start + end) / 2
			if end >= len(a) {
				end = len(a) - 1
				mid = start + step/2 - 1
				if mid > end {
					mid = end
				}
			}
			merge(a, start, mid, end)
		}
	}
}

func main() {
	a := []int{3, 2, 9, -1, 88, 66, 1, 33, -3, 33, 88, 2, 9, 3}
	MergeSort(a)
	fmt.Println(a)
	a = []int{3, 2, 9, -1, 88, 66, 1, 33, -3, 33, 88, 2, 9, 3}
	MergeSortRecursive(a)
	fmt.Println(a)
}
