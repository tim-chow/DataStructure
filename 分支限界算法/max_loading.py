from typing import List


class Node:
    def __init__(self) -> None:
        self.weight: int = 0


_dummy_node: Node = Node()


class MaxLoading:
    def __init__(self, weights: List[int], c1_capacity: int, c2_capacity: int) -> None:
        self._weights: List[int] = weights
        self._c1_capacity: int = c1_capacity
        self._c2_capacity: int = c2_capacity

        # 装完第 i 件物品后，仍然剩余的总重量
        self._remaining: List[int] = [0 for _ in range(len(weights))]
        ind: int = len(self._weights) - 2
        while ind >= 0:
            self._remaining[ind] = self._remaining[ind + 1] + self._weights[ind + 1]
            ind -= 1

    def can_load(self) -> bool:
        if not len(self._weights):
            return True
        # 对第一艘船进行优化，尽量装满它
        queue: List[Node] = [Node(), _dummy_node]
        for ind in range(len(self._weights)):  # type: int
            node: Node = queue.pop(0)
            while node is not _dummy_node:
                # 情况 1：能装下
                if node.weight + self._weights[ind] <= self._c1_capacity:
                    new_node: Node = Node()
                    new_node.weight = node.weight + self._weights[ind]
                    queue.append(new_node)
                # 情况 2：可以不装
                if node.weight + self._weights[ind] + self._remaining[ind] > self._c1_capacity:
                    queue.append(node)
                node = queue.pop(0)
            queue.append(_dummy_node)

        best: int = 0
        for node in queue[:-1]:  # type: Node
            if node.weight > best:
                best = node.weight
        print(best)
        return sum(self._weights) - best <= self._c2_capacity


if __name__ == "__main__":
    print(MaxLoading([20, 28, 25, 25], 70, 30).can_load())
