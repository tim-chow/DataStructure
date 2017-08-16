import java.util.*;

class Node {
    private int row;
    private int column;
    private Node[] nextNodes = new Node[0];
    private int cursor = 0;

    public Node(int row, int column) {
        this.row = row;
        this.column = column;
    }

    public int getRow() {
        return row;
    }

    public int getColumn() {
        return column;
    }

    public Node setNextNodes(Node[] nextNodes) {
        if (nextNodes == null)
            throw new RuntimeException("nextNodes == null");
        this.nextNodes = nextNodes;
        return this;
    }

    public Node getNextNode() {
        if (nextNodes == null || cursor >= nextNodes.length)
            return null;
        return nextNodes[cursor++];
    }

    public Node reset() {
        cursor = 0;
        return this;
    }

    public String toString() {
        return "Node{row=" + row + ", column=" + column + "}";
    }
}

public class Empress {
    private static void printResult(Stack<Node> stack, Node nextNode) {
        for (int i=1; i<stack.size(); i++)
            System.out.print("(" + stack.get(i).getRow() + 
                ", " + 
                stack.get(i).getColumn() + "), ");
        System.out.println("(" + nextNode.getRow() + 
            ", " + nextNode.getColumn()+ ")");
    }

    public static void search(Node root, int n) {
        Stack<Node> stack = new Stack<>();
        stack.push(root);
        Node currentExpandNode;
        Node nextNode;

        while (!stack.empty()) {
            currentExpandNode = stack.peek();
            nextNode = currentExpandNode.getNextNode();
            if (nextNode == null) {
                stack.pop().reset(); // reset here!!!
                continue;
            }

            boolean flag = true;
            for (int i=1; i<stack.size(); i++) {
                if (stack.get(i).getRow() == nextNode.getRow() ||
                        stack.get(i).getColumn() == nextNode.getColumn() ||
                        Math.abs(stack.get(i).getRow() - nextNode.getRow()) ==
                            Math.abs(stack.get(i).getColumn() - nextNode.getColumn())) {
                    flag = false;
                    break;
                }
                
            }

            if (!flag)
                continue;

            if (stack.size() == n) {
                printResult(stack, nextNode);
                continue;
            }
    
            stack.push(nextNode);
        }
    }

    public static void main(String[] args) {
        int n = 8;
        if (args.length > 0)
            n = Integer.valueOf(args[0]);

        Node[][] allNodes = new Node[n][];
        for (int row=1; row<=n; row++) {
            allNodes[row-1] = new Node[n];
            for (int column=1; column<=n; column++) {
                allNodes[row-1][column-1] = new Node(row, column);
            }
        }

        Node root = new Node(0, 0);
        root.setNextNodes(allNodes[0]);
        for (int row=0; row<n-1; row++) {
            for (Node node: allNodes[row])
                node.setNextNodes(allNodes[row+1]);
        }

        search(root, n);
    }
}

