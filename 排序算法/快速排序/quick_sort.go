package main

import (
	"fmt"
)

func quickSort(a []int, start, end int) {
	if start >= end {
		return
	}
	pos := partition(a, start, end)
	quickSort(a, start, pos-1)
	quickSort(a, pos+1, end)
}

func partition(a []int, start, end int) int {
	if start > end {
		panic("start should more than end")
	}

	pivot := a[start]
	index := start // pivot 所在的位置
	for start < end {
		for end > start {
			if a[end] >= pivot {
				end -= 1
			} else {
				a[index], a[end] = a[end], a[index]
				start += 1
				index = end
				break
			}
		}

		for start < end {
			if a[start] <= pivot {
				start += 1
			} else {
				a[start], a[index] = a[index], a[start]
				end -= 1
				index = start
				break
			}
		}
	}
	return index
}

func QuickSort(a []int) {
	if len(a) == 0 {
		return
	}
	quickSort(a, 0, len(a)-1)
}

func main() {
	a := []int{3, 2, 9, -1, 88, 66, 1, 33, -3, 33, 88, 2, 9, 3}
	QuickSort(a)
	fmt.Println(a)
}
