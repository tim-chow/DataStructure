import sys


class MinStack(object):
    def __init__(self):
        self._stack = []
        self._min_value = sys.maxint

    def push(self, x):
        if x < self._min_value:
            self._stack.append(self._min_value)
            self._min_value = x
        self._stack.append(x)

    def pop(self):
        value = self._stack.pop(-1)
        if value == self._min_value:
            self._min_value = self._stack.pop(-1)
        return value

    def top(self):
        return self._stack[-1]

    def getMin(self):
        return self._min_value


if __name__ == "__main__":
    import unittest
    import random

    class MinStackTest(unittest.TestCase):
        def testMinStack(self):
            min_stack = MinStack()
            elements = list(range(1, 100))
            random.shuffle(elements)
            for element in elements:
                min_stack.push(element)
            self.assertEqual(min_stack.getMin(), 1)

    unittest.main()
