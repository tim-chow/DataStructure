class Stack(object):
    def __init__(self):
        self._array_list = []
        self._base = self._top = 0

    def push(self, element):
        self._array_list.append(element)
        self._top = self._top + 1

    def is_empty(self):
        return self._base == self._top

    def size(self):
        return self._top - self._base

    def pop(self):
        if self.is_empty():
            raise RuntimeError("stack is empty")
        element = self._array_list.pop(-1)
        self._top = self._top - 1
        return element

    def peek(self):
        if self.is_empty():
            raise RuntimeError("stack is empty")
        return self._array_list[-1]

def is_pair(string):
    def _is_left(char):
        return char in ["{", "[", "("]

    def _is_pair(left, right):
        pairs = {"{": "}", "[": "]", "(": ")"}
        return right == pairs[left]

    stack = Stack()
    for char in string:
        if _is_left(char):
            stack.push(char)
        else:
            if stack.size() == 0:
                return False
            left = stack.pop()
            if not _is_pair(left, char):
                return False
    return stack.size() == 0

def conversion(n, base):
    result = ["+"]
    if n < 0:
        result[0] = "-"
        n = -1 * n

    stack = Stack()
    while n != 0:
        stack.push(n % base)
        n = n / base

    while stack.size() > 0:
        result.append(stack.pop())

    return result


if __name__ == "__main__":
    print(is_pair("[[]]()"))
    print(conversion(20, 2))
