# coding: utf8

class Node(object):
    def __init__(self):
        self.chosen = []
        self.weight = 0

    def __repr__(self):
        return '%s{chosen=%s, weight=%d}' % (
            self.__class__.__name__, self.chosen, self.weight)

class DummyNode(Node):
    def __init__(self):
        Node.__init__(self)

class MaxLoading:
    def __init__(self, weight, c):
        self._w = weight # 集装箱重量数组
        self._n = len(weight) # 集装箱数量
        self._c = c # 总载重量

        # 在装了第i个物品之后，剩余物品的总重量
        self._r = [0] * self._n
        for ind in range(self._n - 2, -1, -1):
            self._r[ind] = self._r[ind+1] + self._w[ind+1]

    def max_loading(self):
        queue = [Node(), DummyNode()]

        for i in range(self._n):
            node = queue.pop(0)
            while not isinstance(node, DummyNode):
                if node.weight + self._w[i] <= self._c:
                    new_node = Node()
                    new_node.chosen = [item for item in node.chosen] + [i]
                    new_node.weight = node.weight + self._w[i]
                    queue.append(new_node)
                # 剪枝函数
                # + 如果当前重量 + 当前物品 + 剩余物品的总质量
                # + + 小于等于 总容量，那么进行剪枝
                if node.weight + self._w[i] + self._r[i] > self._c:
                    queue.append(node)
                node = queue.pop(0)
            queue.append(DummyNode())

        best = None
        for node in queue[:len(queue)-1]:
            if not best or node.weight > best.weight:
                best = node
        return best

if __name__ == "__main__":
    import pprint
    # output: 1 0 1 1
    pprint.pprint(MaxLoading([20, 10, 26, 15], 70).max_loading())

