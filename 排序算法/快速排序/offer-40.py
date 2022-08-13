# 获取最小的 k 个数：https://leetcode.cn/problems/zui-xiao-de-kge-shu-lcof/

from typing import List


class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        if not arr or k <= 0:
            return []
        if len(arr) <= k:
            return arr
        low: int = 0
        high: int = len(arr) - 1
        current: int = self.partition(arr, low, high)
        target = k
        while current != target:
            if current > target:
                high = current - 1
                current = self.partition(arr, low, high)
                continue
            if current < target:
                low = current + 1
                current = self.partition(arr, low, high)
                continue
        return arr[:target]

    def partition(self, nums: List[int], start: int, end: int) -> int:  # noqa
        if start > end:
            raise RuntimeError("start should be less than or equal end")
        pivot: int = nums[start]
        index: int = start
        while start < end:
            while end > start:
                if nums[end] >= pivot:
                    end -= 1
                    continue
                nums[index], nums[end] = nums[end], nums[index]
                index = end
                start += 1
                break
            while start < end:
                if nums[start] <= pivot:
                    start += 1
                    continue
                nums[index], nums[start] = nums[start], nums[index]
                index = start
                end -= 1
                break
        return index
