# coding: utf8


class Node(object):
    def __init__(self, element):
        self.element = element
        self.parent = -1

    def __str__(self):
        return "%s{element=%s, parent=%d}" % (
            self.__class__.__name__,
            self.element,
            self.parent)

    __repr__ = __str__


class MFSet(object):
    def __init__(self, s, r):
        self._nodes = [Node(e) for e in s]
        self._r = r
        self.divide()

    def find_root(self, x):
        temp = x
        while self._nodes[temp].parent >= 0:
            temp = self._nodes[temp].parent
        return temp

    def merge(self, x, y):
        si = self.find_root(x)
        sj = self.find_root(y)
        if si == sj:
            return

        node_si = self._nodes[si]
        node_sj = self._nodes[sj]

        if -1 * node_si.parent >= -1 * node_sj.parent:
            node_si.parent = node_si.parent + node_sj.parent
            node_sj.parent = si
        else:
            node_sj.parent = node_si.parent + node_sj.parent
            node_si.parent = sj

    def divide(self):
        for x, y in self._r:
            self.merge(x, y)

    @property
    def nodes(self):
        return self._nodes


if __name__ == "__main__":
    s = [0, 1, 2, 3, 4, 5]
    r = [(0, 2), (2, 4), (1, 3), (3, 5)]
    mfset = MFSet(s, r)
    print(mfset.nodes)
