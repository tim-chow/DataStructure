# 寻找数组中第 K 大的元素：https://leetcode.com/problems/kth-largest-element-in-an-array/

from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        if not nums or k <= 0 or k > len(nums):
            return -1
        low: int = 0
        high: int = len(nums) - 1
        current: int = self.partition(nums, low, high)
        target = len(nums) - k
        while current != target:
            if current > target:
                high = current - 1
                current = self.partition(nums, low, high)
                continue
            if current < target:
                low = current + 1
                current = self.partition(nums, low, high)
                continue
        return nums[target]

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
