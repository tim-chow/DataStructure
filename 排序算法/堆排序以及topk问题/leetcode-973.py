# 距离原点最近的 K 个点：https://leetcode.com/problems/k-closest-points-to-origin/

from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        if not points or k <= 0:
            return []
        if len(points) <= k:
            return points

        # 将数组的前 k 个元素堆化
        for idx in range(k // 2, -1, -1):
            self.adjust(points, idx, k - 1)
        for idx in range(k, len(points)):
            if self._less_than(points[0], points[idx]):
                continue
            points[0], points[idx] = points[idx], points[0]
            self.adjust(points, 0, k - 1)
        return points[:k]

    def _less_than(self, point1: List[int], point2: List[int]) -> bool:  # noqa
        return (point1[0] * point1[0] + point1[1] * point1[1]) < (point2[0] * point2[0] + point2[1] * point2[1])

    # 大根堆
    def adjust(self, arr: List[List[int]], start: int, end: int) -> None:  # noqa
        if start >= end:
            return
        while 2 * start + 1 <= end:
            left: int = 2 * start + 1
            right: int = 2 * start + 2
            # 如果没有右孩子
            if right > end:
                if self._less_than(arr[start], arr[left]):
                    arr[start], arr[left] = arr[left], arr[start]
                break
            if not self._less_than(arr[start], arr[left]) and not self._less_than(arr[start], arr[right]):
                break
            if not self._less_than(arr[left], arr[right]):
                # 与左孩子交换
                arr[start], arr[left] = arr[left], arr[start]
                start = left
                continue
            arr[start], arr[right] = arr[right], arr[start]
            start = right
