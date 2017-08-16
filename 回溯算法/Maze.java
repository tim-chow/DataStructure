import java.util.*;

class Node {
    private int row;
    private int column;
    private boolean isWall;
    private List<Node> nextNodes = new ArrayList<>();
    private int cursor = 0;

    public Node(int row, int column, boolean isWall) {
        this.row = row;
        this.column = column;
        this.isWall = isWall;
    }

    public int getRow() {
        return row;
    }

    public int getColumn() {
        return column;
    }

    public boolean getIsWall() {
        return isWall;
    }

    public Node addNextNode(Node nextNode) {
        if (nextNode == null)
            throw new RuntimeException("nextNode == null");
        nextNodes.add(nextNode);
        return this;
    }

    public Node getNextNode() {
        if (cursor >= nextNodes.size())
            return null;
        return nextNodes.get(cursor++);
    }

    @Override
    public String toString() {
        return String.format("(%d, %d)", row, column);
    }

    @Override
    public boolean equals(Object o) {
        if (!getClass().isInstance(o))
            return false;
        Node o1 = (Node)o;
        return o1.getRow() == row && o1.getColumn() == column;
    }
}

public class Maze {
    private static void printResult(Stack<Node> stack, Node nextNode) {
        for (Node node: stack)
            System.out.print(node.toString() + ", ");
        System.out.println(nextNode.toString());
    }

    public static void search(Node start, Node end) {
        Stack<Node> stack = new Stack<>();
        stack.push(start);
        Node currentExpandNode, nextNode;

        while (!stack.empty()) {
            currentExpandNode = stack.peek();
            nextNode = currentExpandNode.getNextNode();
            if (nextNode == null) {
                stack.pop();
                continue;
            }

            if (nextNode.getIsWall())
                continue;

            boolean flag = true;
            for (Node node: stack)
                if (node.equals(nextNode)) {
                    flag = false;
                    break;
                }
            if (!flag)
                continue;

            if (nextNode.equals(end)) {
                printResult(stack, nextNode);
                continue;
            }
            
            stack.push(nextNode);
        }
    }

    public static void main(String[] args) {
        int[][] maze = new int[][]{
            new int[]{0, 0, 0, 0, 0},
            new int[]{0, 1, 1, 1, 0},
            new int[]{0, 0, 0, 1, 0},
            new int[]{0, 1, 1, 1, 0},
            new int[]{0, 0, 0, 0, 0}};

        Node[][] allNodes = new Node[maze.length][];
        for (int row=0; row<maze.length; ++row) {
            Node[] nodes = new Node[maze[row].length];
            for (int column=0; column<maze[row].length; ++column) 
                nodes[column] = new Node(row, column, maze[row][column] == 0);
            allNodes[row] = nodes;
        }

        for (int row=0; row<allNodes.length; ++row)
            for (int column=0; column<allNodes[row].length; ++column) {
                if (row > 0)
                    allNodes[row][column].addNextNode(allNodes[row-1][column]);
                if (row < allNodes.length - 1)
                    allNodes[row][column].addNextNode(allNodes[row+1][column]);
                if (column > 0)
                    allNodes[row][column].addNextNode(allNodes[row][column-1]);
                if (column < allNodes[row].length - 1)
                    allNodes[row][column].addNextNode(allNodes[row][column+1]);
            }

        search(allNodes[1][1], allNodes[3][1]);
    }
}

