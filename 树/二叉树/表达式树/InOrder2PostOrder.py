# coding: utf8


class Operator(object):
    def __init__(self, char):
        self.char = char

    @staticmethod
    def get_operator(char):
        if char == "+":
            return PlusOperator()
        if char == "-":
            return MinusOperator()
        if char == "*":
            return MultiplyOperator()
        if char == "/":
            return DivisionOperator()
        return None

    def __str__(self):
        return self.char

    def execute(self, left, right):
        raise NotImplementedError


class PlusOperator(Operator):
    def __init__(self):
        Operator.__init__(self, "+")

    def __cmp__(self, other):
        if isinstance(other, (PlusOperator, MinusOperator)):
            return 0
        return -1

    def execute(self, left, right):
        return left + right

class MinusOperator(Operator):
    def __init__(self):
        Operator.__init__(self, "-")

    def __cmp__(self, other):
        if isinstance(other, (PlusOperator, MinusOperator)):
            return 0
        return -1

    def execute(self, left, right):
        return left - right


class MultiplyOperator(Operator):
    def __init__(self):
        Operator.__init__(self, "*")

    def __cmp__(self, other):
        if isinstance(other, (MultiplyOperator, DivisionOperator)):
            return 0
        return 1

    def execute(self, left, right):
        return left * right


class DivisionOperator(Operator):
    def __init__(self):
        Operator.__init__(self, "/")

    def __cmp__(self, other):
        if isinstance(other, (MultiplyOperator, DivisionOperator)):
            return 0
        return 1

    def execute(self, left, right):
        return left / right


class Operand(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Bracket(object):
    def __init__(self, char):
        self.char = char

    @staticmethod
    def get_bracket(char):
        if char == "(":
            return LeftBracket()
        if char == ")":
            return RightBracket()
        return None

    def __str__(self):
        return self.char


class LeftBracket(Bracket):
    def __init__(self):
        Bracket.__init__(self, "(")


class RightBracket(Bracket):
    def __init__(self):
        Bracket.__init__(self, ")")


def inorder_to_postorder(inorder_tokens):
    """
    中缀表达式转后缀表达式
    """
    postorder_tokens = []
    stack = []
    for token in inorder_tokens:
        # 遇到操作数时，直接输出
        if isinstance(token, Operand):
            postorder_tokens.append(token)
            continue

        # 遇到左括号时，将其压进栈中
        if isinstance(token, LeftBracket):
            stack.append(token)
            continue

        # 遇到右括号时，弹出栈顶的操作符，并输出，直到遇到左括号，
        # 并且左括号不输出，右括号不进栈
        if isinstance(token, RightBracket):
            while stack:
                element = stack.pop()
                if isinstance(element, LeftBracket):
                    break
                postorder_tokens.append(element)
            continue

        # 遇到其它操作符时，弹出栈顶的操作符，并输出，直到栈空或栈顶的操作符的优先级小于该操作符的优先级
        # 或遇到左括号，然后将该操作符压入栈中
        if isinstance(token, Operator):
            while stack:
                if isinstance(stack[-1], LeftBracket) or stack[-1] < token:
                    break
                postorder_tokens.append(stack.pop())
            stack.append(token)
            continue

        raise RuntimeError("unreachable")

    # 最后将栈中的操作符弹出，直到栈空
    while stack:
        postorder_tokens.append(stack.pop())

    return postorder_tokens


class Node(object):
    def __init__(self, keyword, left=None, right=None):
        self.keyword = keyword
        self.left = left
        self.right = right


def postorder_to_expression_tree(tokens):
    """
    后缀表达式转表达式树
    """
    stack = []
    for token in tokens:
        # 遇到操作数时，则生成单节点，然后放到栈中
        if isinstance(token, Operand):
            stack.append(Node(token.value))
            continue
        # 遇到操作符时，则生成一个新节点，并从栈中弹出两个元素，
        # 同时把这两个元素作为新节点的子树，然后将该新节点放入栈中
        if isinstance(token, Operator):
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(token.char, left, right))
            continue

        raise RuntimeError("unreachable")

    # 最后栈中的元素就是表达式树的根
    return stack[-1]


def test():
    expression = "(1+2)*(3+4)+(5*(6+7))+80/(20-10)"  # 94

    class Reader(object):
        def __init__(self, string):
            self._string = string
            self._operators = set(list("+-*/()"))
            self._cursor = 0

        def read(self):
            if self._cursor >= len(self._string):
                return

            char = self._string[self._cursor]
            self._cursor = self._cursor + 1
            if char in self._operators:
                return char

            chars = [char]
            while self._cursor < len(self._string):
                char = self._string[self._cursor]
                if char in self._operators:
                    return "".join(chars)
                self._cursor = self._cursor + 1
                chars.append(char)
            return "".join(chars)

    reader = Reader(expression)
    tokens = []
    while True:
        token = reader.read()
        if token is None:
            break
        operator = Operator.get_operator(token)
        if operator is not None:
            tokens.append(operator)
            continue
        bracket = Bracket.get_bracket(token)
        if bracket is not None:
            tokens.append(bracket)
            continue
        tokens.append(Operand(int(token)))

    postorder_tokens = inorder_to_postorder(tokens)

    stack = []
    for token in postorder_tokens:
        if isinstance(token, Operand):
            stack.append(token)
        elif isinstance(token, Operator):
            right = stack.pop()
            left = stack.pop()
            stack.append(Operand(token.execute(left.value, right.value)))
    print(stack[-1].value)


if __name__ == "__main__":
    test()
