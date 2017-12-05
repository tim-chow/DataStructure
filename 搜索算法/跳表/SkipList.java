import java.util.*;

public class SkipList<T extends Comparable> {
    public static class Node<T extends Comparable> {
        T data;
        Node<T> next;
        Node<T> down;

        public String toString() {
            return String.format(
                "Node{data=%s, next=%s, down=%s}", data, next, down);
        }
    }

    List<Node<T>> indexList = new ArrayList<>();
    {
        indexList.add(new Node<T>());
    }

    @SuppressWarnings("unchecked")
    public void add(T data) {
        if (data == null)
            throw new RuntimeException("data == null");
        Random random = new Random();
        int k = 0, height = indexList.size();
        while (random.nextDouble() <= 0.5d && k < height)
            k++;

        if (k == height) {
            // 添加新索引
            Node<T> headNode = new Node<>();
            headNode.down = indexList.get(height - 1);
            indexList.add(headNode);
        }

        Node<T> node, next, newNode, previousNewNode = null;
        node = indexList.get(k);
        while (node != null) {
            while (node.next != null && 
                    node.next.data != null &&
                    node.next.data.compareTo(data) == -1)
                node = node.next;
            next = node.next;
            newNode = new Node<T>();
            newNode.data = data;
            newNode.next = next;
            if (previousNewNode != null)
                previousNewNode.down = newNode;
            node.next = newNode;
            previousNewNode = newNode;

            node = node.down;
        }
    }

    @SuppressWarnings("unchecked")
    public void delete(T data) {
        int level = indexList.size() - 1;
        Node<T> node = indexList.get(indexList.size() - 1);

        for (; node != null; level--) {
            while (node.next != null && node.next.data != null) {
                int compare = node.next.data.compareTo(data);
                if (compare == 0) {
                    node.next = node.next.next;
                    break;
                } 
                if (compare == 1)
                    break;
                node = node.next;
            }

            if (level != 0 && node.next == null)
                indexList.remove(level);

            node = node.down;
        }
    }

    @SuppressWarnings("unchecked")
    public Node<T> get(T data) {
        Node<T> node = indexList.get(indexList.size() - 1);

        while (node != null) {
            while (node.next != null && node.next.data != null) {
                int compare = node.next.data.compareTo(data);
                if (compare == 0)
                    return node.next;
                if (compare == 1)
                    break;
                node = node.next;
            }
            
            node = node.down;
        }

        return null;
    }

    public static void main(String[] args) {
        SkipList<Integer> skipList = new SkipList<>();
        skipList.add(8);
        skipList.add(7);
        skipList.add(10);
        skipList.add(3);
        skipList.add(4);
        skipList.add(1);
        skipList.add(5);
        skipList.add(6);
        skipList.add(9);
        skipList.add(2);
        skipList.add(11);
        skipList.add(12);
        skipList.add(10);

//        skipList.delete(4);
//        skipList.delete(9);
//        skipList.delete(6);
//        skipList.delete(11);
//        skipList.delete(12);
//        skipList.delete(10);
//        skipList.delete(4);
//        skipList.delete(1);
//        skipList.delete(3);
//        skipList.delete(2);
//
        skipList.add(2);
        skipList.add(4);
        for (Node<Integer> node: skipList.indexList) {
            System.out.println("==========");
            while (node.next != null) {
                node = node.next;
                Integer data = node.data;
                System.out.println(String.format("data = %s", data));

                Node<Integer> down = node.down;
                while (down != null) {
                    System.out.println(data.equals(down.data));
                    down = down.down;
                }
            }
        }

        Node<Integer> node = skipList.get(333);
        if (node == null)
            return;
        Node<Integer> down = node.down;
        while (down != null) {
            System.out.println(String.format("down.data = " + down.data));
            down = down.down;
        }
    }
}

