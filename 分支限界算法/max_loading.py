# coding: utf8


class Node(object):
    def __init__(self):
        self.chosen = []
        self.weight = 0

    def __repr__(self):
        return '%s{chosen=%s, weight=%d}' % (
            self.__class__.__name__,
            self.chosen,
            self.weight)


class DummyNode(Node):
    def __init__(self):
        Node.__init__(self)


class MaxLoading(object):
    def __init__(self, weights, carrying_capacity):
        self._weights = weights
        self._number = len(weights)
        self._carrying_capacity = carrying_capacity

        # 在装了第 i 个物品之后，剩余物品的总重量
        self._remaining = [0] * self._number
        for ind in range(self._number - 2, -1, -1):
            self._remaining[ind] = self._remaining[ind+1] + \
                self._weights[ind+1]

    def max_loading(self):
        queue = [Node(), DummyNode()]

        for ind in range(self._number):
            node = queue.pop(0)
            while not isinstance(node, DummyNode):
                if node.weight + self._weights[ind] <= self._carrying_capacity:
                    # 装第 ind 个物品
                    new_node = Node()
                    new_node.chosen = [item for item in node.chosen] + [ind]
                    new_node.weight = node.weight + self._weights[ind]
                    queue.append(new_node)

                if node.weight + self._weights[ind] + \
                        self._remaining[ind] > self._carrying_capacity:
                    # 不装第 ind 个物品
                    queue.append(node)

                node = queue.pop(0)
            queue.append(DummyNode())

        best = None
        for node in queue[:len(queue)-1]:
            if best is None or node.weight > best.weight:
                best = node
        return best


if __name__ == "__main__":
    import pprint
    pprint.pprint(
        MaxLoading([20, 23, 26, 24], 70)
        .max_loading())
