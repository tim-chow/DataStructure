import java.util.*;

class Node<T> {
    public static class Entry<T> {
        public Node<T> node;
        public int index;

        @Override
        public String toString() {
            String nodeString = "null";
            if (node != null)
                nodeString = node.toString();
            return String.format("Entry{node=%s, index=%d}", nodeString, index);
        }
    }

    private T element;
    private int parent;

    public Node(T element) {
        this(element, -1);
    }

    public Node(T element, int parent) {
        this.element = element;
        this.parent = parent;
    }


    public T getElement() {
        return element;
    }

    public int getParent() {
        return parent;
    }

    public void setParent(int parent) {
        this.parent = parent;
    }

    public Entry<T> findRoot(List<Node<T>> nodes) {
        Entry<T> entry = new Entry<>();
        entry.index = nodes.indexOf(this);
        entry.node = this;

        Node<T> node = this;
        while (node.getParent()  >= 0) {
            entry.index = node.getParent();
            entry.node = node = nodes.get(entry.index);
        }
        return entry;
    }

    public void merge(Node<T> anotherNode, List<Node<T>> nodes) {
        Entry<T> anotherEntry = anotherNode.findRoot(nodes);
        Entry<T> entry = this.findRoot(nodes);
        if (anotherEntry.node == entry.node)
            return;

        int anotherCount = -1 * anotherEntry.node.getParent();
        int count = -1 * entry.node.getParent();

        if (anotherCount > count) {
            entry.node.setParent(anotherEntry.index);
            anotherEntry.node.setParent(-1*(anotherCount + count));
        } else {
            anotherEntry.node.setParent(entry.index);
            entry.node.setParent(-1*(anotherCount + count));
        }
    }

    @Override
    public String toString() {
        return String.format("Node{element=%s, parent=%d}",
            element.toString(), parent);
    }
}

public class MFSet {
    public static void main(String[] args) {
        List<Node<Integer>> nodes = new ArrayList<>();
        for (int i = 0; i < 9; i++)
            nodes.add(new Node(i));
        int[][] R = new int[][]{new int[]{0, 2}, new int[]{2, 4},
            new int[]{4, 6}, new int[]{6, 8}};

        for (int[] pair: R) {
            nodes.get(pair[0]).merge(nodes.get(pair[1]), nodes);
        }

        System.out.println(nodes);
    }
}

