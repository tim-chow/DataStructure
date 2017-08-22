class Node(object):
    def __init__(self, element, left=None, right=None):
        self._element = element
        self._left = left
        self._right = right

    @property
    def element(self):
        return self._element

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def postorder_traverse(self):
        if self.left:
            self.left.postorder_traverse()
        if self.right:
            self.right.postorder_traverse()
        print self.element

class Operator(object):
    operators = {}

    def __init__(self, character, priority):
        self._character = character
        self._priority = priority
        self.operators[character] = self

    @property
    def character(self):
        return self._character

    @property
    def priority(self):
        return self._priority

    def precedence_over(self, other):
        if not isinstance(other, self.__class__):
            raise RuntimeError("invalid type")
        if self.priority == other.priority:
            return 0
        if self.priority > other.priority:
            return 1
        return -1
    
    @classmethod
    def get_operator(cls, character):
        return cls.operators.get(character)

class InOrder2PostOrder:
    Operator("+", 1)
    Operator("-", 1)
    Operator("*", 2)
    Operator("/", 2)
    Operator("(", 0)
    Operator(")", 0)

    @staticmethod
    def inorder_2_postorder(list):
        result = []
        stack = []
        for element in list:
            operator = Operator.get_operator(element)
            if not operator:
                result.append(element)
                continue
            if element == "(":
                stack.append(operator)
                continue
            if element == ")":
                while stack:
                    o = stack.pop(-1)
                    if o.character == "(":
                        break
                    result.append(o.character)
                continue

            while stack:
                if stack[-1].precedence_over(operator) == -1:
                    break
                result.append(stack.pop(-1).character)
            stack.append(operator)

        while stack:
            result.append(stack.pop(-1).character)
        return result

    @staticmethod
    def eval(postorder_expression):
        expression = postorder_expression
        stack = []
        for element in expression:
            operator = Operator.get_operator(element)
            if not operator:
                stack.append(element)
                continue

            operand1 = float(stack.pop(-1))
            operand2 = float(stack.pop(-1))
            if element == "+":
                stack.append(operand1 + operand2)
            elif element == "-":
                stack.append(operand1 - operand2)
            elif element == "*":
                stack.append(operand1 * operand2)
            else:
                stack.append(operand1 / operand2)
        return stack.pop(-1)

    @staticmethod
    def generate_expression_tree(postorder_expression):
        stack = []
        for element in postorder_expression:
            operator = Operator.get_operator(element)
            if not operator:
                stack.append(Node(element))
                continue
            right = stack.pop(-1)
            left = stack.pop(-1)
            stack.append(Node(element, left, right))
        return stack.pop(-1)

if __name__ == "__main__":
    expression = "( ( 1 + 2 ) * ( 3 + 4 ) ) * ( 5 + 6 )".split(" ")
    print eval("".join(expression))
    po = InOrder2PostOrder.inorder_2_postorder(expression)
    print po
    print InOrder2PostOrder.eval(po)
    InOrder2PostOrder.generate_expression_tree(po).postorder_traverse()

