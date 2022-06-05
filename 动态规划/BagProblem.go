package main

import "fmt"

// Good 代表物品
type Good struct {
	// 重量
	Weight int
	// 价值
	Cost int
}

type BagProblem struct {
	// 物品列表
	goods []*Good
	// 背包的最大重量
	maxWeight int
}

func (b *BagProblem) copyGoods(goods []*Good) []*Good {
	dest := make([]*Good, len(goods))
	copy(dest, goods)
	return dest
}

func (b *BagProblem) dp(from int, currentWeight int, chosenGoods []*Good) (int, []*Good) {
	// 如果当前的重量等于最大重量，那么返回；
	// 如果已经无物品可选，那么返回
	copied := b.copyGoods(chosenGoods)
	if currentWeight == b.maxWeight || from >= len(b.goods) {
		return currentWeight, copied
	}

	// 如果装不进来
	if currentWeight+b.goods[from].Weight > b.maxWeight {
		// 那么放弃选择当前物品
		return b.dp(from+1, currentWeight, copied)
	}

	// 如果能装进来，那么存在两种情况
	// 1. 选择当前物品
	newChosenGoods := append(copied, b.goods[from])
	w1, c1 := b.dp(from+1, currentWeight+b.goods[from].Weight, newChosenGoods)
	// 2. 不选择当前物品
	w2, c2 := b.dp(from+1, currentWeight, copied)
	totalCost1 := 0
	for _, good := range c1 {
		totalCost1 += good.Cost
	}
	totalCost2 := 0
	for _, good := range c2 {
		totalCost2 += good.Cost
	}
	if totalCost1 >= totalCost2 {
		return w1, c1
	} else {
		return w2, c2
	}
}

func (b *BagProblem) GetBestChoice() (int, []*Good) {
	chosenGoods := make([]*Good, 0)
	return b.dp(0, 0, chosenGoods)
}

func NewBagProblem(goods []*Good, maxWeight int) *BagProblem {
	return &BagProblem{goods: goods, maxWeight: maxWeight}
}

func main() {
	goods := []*Good{{3, 4}, {2, 4}, {5, 8}, {7, 10}, {3, 3}, {8, 11}}
	var maxWeight int
	maxWeight = 15
	bagProblem := NewBagProblem(goods, maxWeight)
	weight, chosenGoods := bagProblem.GetBestChoice()
	fmt.Printf("weight = %d\n", weight)
	for _, good := range chosenGoods {
		fmt.Printf("(%d, %d)\n", good.Weight, good.Cost)
	}
}
