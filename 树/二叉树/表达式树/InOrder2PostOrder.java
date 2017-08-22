import java.util.*;

class Node<T> {
    private T element;
    private Node<T> left;
    private Node<T> right;

    public Node(T element) {
        this.element = element;
    }

    public Node(T element, Node<T> left, Node<T> right) {
        this(element);
        this.left = left;
        this.right = right;
    }

    public void postOrderTraverse() {
        if (left != null)
            left.postOrderTraverse();
        if (right != null)
            right.postOrderTraverse();
        System.out.println(element);
    }
}

class Operator {
    private String character;
    private int priority;
    private static Map<String, Operator> map = 
        new HashMap<>();

    public Operator(String character, int priority) {
        this.character = character;
        this.priority = priority;
        map.put(character, this);
    }

    public int getPriority() {
        return priority;
    }

    public String getCharacter() {
        return character;
    }

    public int precedenceOver(Operator operator) {
        if (operator == null)
            throw new RuntimeException("operator == null");
        if (priority == operator.getPriority())
            return 0;
        if (priority > operator.getPriority())
            return 1;
        return -1;
    }

    @Override
    public String toString() {
        return String.format("Operator{character=%s, priority=%d}",
            character, priority);
    }

    public static Operator getOperator(String character) {
        if (map.containsKey(character))
            return map.get(character);
        return null;
    }
}

class InOrder2PostOrder {
    static {
        new Operator("+", 1);
        new Operator("-", 1);
        new Operator("*", 2);
        new Operator("/", 2);
        new Operator("(", 0);
        new Operator(")", 0);
    }

    public static List<String> inOrder2PostOrder(List<String> list) {
        Stack<Operator> stack = new Stack<>();
        List<String> result = new ArrayList<>();

        for (String element: list) {
            Operator operator = Operator.getOperator(element);
            if (operator == null) {
                result.add(element);
                continue;
            }
            if ("(".equals(element)) {
                stack.push(operator);
                continue;
            }
            if (")".equals(element)) {
                while (!stack.empty()) {
                    Operator o = stack.pop();
                    if (o.getCharacter().equals("("))
                        break;
                    result.add(o.getCharacter());
                }
                continue;
            }

            while (!stack.empty()) {
                if (stack.peek().precedenceOver(operator) == -1)
                    break;
                result.add(stack.pop().getCharacter());
            }
            stack.push(operator);
        }

        while (!stack.empty())
            result.add(stack.pop().getCharacter());
        return result;
    }

    public static Node<String> generateExpressionTree(
        List<String> postOrderExpression) {
        Stack<Node<String>> stack = new Stack<>();

        for (String element: postOrderExpression) {
            Operator operator = Operator.getOperator(element);
            if (operator == null) {
                stack.push(new Node<String>(element));
                continue;
            }
            
            Node<String> right = stack.pop();
            Node<String> left = stack.pop();
            stack.push(new Node<String>(element, left, right));
        }
        return stack.pop();
    }

    public static void main(String[] args) {
        List<String> list = Arrays.asList(new String[]{
            "(", "(", "1", "+", "2", ")", "*", 
            "(", "3", "+", "4", ")", ")", "*",
            "(", "5", "+", "6", ")"});
        System.out.println(list = inOrder2PostOrder(list));
        Node<String> root;
        (root = generateExpressionTree(list)).postOrderTraverse();
    }
}

