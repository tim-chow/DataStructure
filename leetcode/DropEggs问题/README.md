### 问题描述

There is a building of n floors. If an egg drops from the k th floor or above, it will break. If it’s dropped from any floor below, it will not break.

You’re given two eggs, Find k while minimize the number of drops for the worst case. Return the number of drops in the worst case.

For n = 10, a naive way to find k is drop egg from 1st floor, 2nd floor … kth floor. But in this worst case (k = 10), you have to drop 10 times.

Notice that you have two eggs, so you can drop at 4th, 7th & 9th floor, in the worst case (for example, k = 9) you have to drop 4 times.

Given n = 10, return 4.

Given n = 100, return 14

---

### 解题思路

因为只有 2 个鸡蛋，所以第一个鸡蛋应该<strong>按一定的距离</strong>仍，比如 10 楼、20 楼、30 楼等，如果 10 楼和 20 楼没碎，30 楼碎了，那么第二个鸡蛋就要做<strong>线性搜索</strong>，从 21 楼开始尝试，直到鸡蛋摔碎。在这种方法中，每多扔一次第一个鸡蛋，第二个鸡蛋的线性搜索次数始终是 10，所以我们需要<strong>每多扔一次第一个鸡蛋，第二个鸡蛋的线性搜索次数减少 1</strong>。设第一次从 X 层仍第一个鸡蛋，第二次从 X + (X - 1) 层仍，...，第 n 次从 X + (X - 1) + ... + (X - n - 1) 层仍。
