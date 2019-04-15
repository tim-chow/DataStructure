# coding: utf8

class Node(object):
    def __init__(self):
        self.chosen = []
        self.current_weight = 0

    def __str__(self):
        return "Node{chosen=%s, current_weight=%d}" % (
            self.chosen, self.current_weight)

    __repr__ = __str__


class MaxLoading(object):
    def __init__(self, c1, c2, weights):
        self._c1 = c1
        self._c2 = c2
        self._weights = weights
        self._n = len(self._weights)

        if sum(self._weights) > self._c1 + self._c2 or not self._n:
            raise RuntimeError("invalid input")

        self._remains = [0] * self._n
        self._remains[self._n-1] = self._weights[self._n-1]
        # 从第i个箱子到最后一个箱子的总重量
        for i in range(self._n-2, -1, -1):
            self._remains[i] = self._weights[i] + self._remains[i+1]

    def calc(self):
        nodes = [Node()]
        children = []

        for i, wi in enumerate(self._weights):
            for node in nodes:
                # 装不进去
                if node.current_weight + wi > self._c1:
                    children.append(node)
                    continue

                node1 = Node()
                node1.chosen = node.chosen + [i]
                node1.current_weight = node.current_weight + wi
                children.append(node1)

                # 能把余下的都装下，那么不应该不装
                if self._c1 - node.current_weight >= self._remains[i]:
                    continue
                # 不装
                node2 = Node()
                node2.chosen = [item for item in node.chosen]
                node2.current_weight = node.current_weight
                children.append(node2)
            nodes = children
            children = []

        best_node = None
        for node in nodes:
            if best_node is None or best_node.current_weight < node.current_weight:
                best_node = node
        return self._remains[0] - best_node.current_weight <= self._c2

if __name__ == "__main__":
    max_loading = MaxLoading(100, 160, [101, 89, 70])
    print(max_loading.calc())
