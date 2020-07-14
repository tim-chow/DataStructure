# coding: utf8


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
        element = self._array_list.pop()
        self._top = self._top - 1
        return element

    def peek(self):
        if self.is_empty():
            raise RuntimeError("stack is empty")
        return self._array_list[-1]


def is_pair(string):
    lefts = {"{", "[", "("}
    matches = {"{": "}", "[": "]", "(": ")"}

    stack = Stack()
    for char in string:
        if char in lefts:
            # 遇到左括号，压栈
            stack.push(char)
        else:
            # 遇到右括号弹出栈顶元素，并判断是否匹配
            if stack.size() == 0:
                return False
            left = stack.pop()
            if char != matches[left]:
                return False

    # 最后检查栈是否为空
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
    print(is_pair("[[()()]"))
    print(conversion(35, 18))
