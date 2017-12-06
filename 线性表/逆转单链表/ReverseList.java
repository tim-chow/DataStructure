public class ReverseList {
    public static class Node<T> {
        private T data;
        private Node<T> next;

        public Node(T data) {
            this.data = data;
        }

        public Node<T> getNext() {
            return next;
        }

        public void setNext(Node<T> next) {
            this.next = next;
        }

        @Override
        public String toString() {
            return "Node{" +
                    "data=" + data +
                    '}';
        }
    }

    // 使用三指针法逆转单链表
    public static <T> Node<T> reverseList(Node<T> firstNode) {
        if (firstNode == null)
            return null;
        Node<T> p1 = firstNode, p2 = p1.getNext(), p3;
        firstNode.setNext(null);
        while (p2 != null) {
            p3 = p2.getNext();
            p2.setNext(p1);

            p1 = p2;
            p2 = p3;
        }
        return p1;
    }

    public static void main(String[] args) {
        Node<Integer> node = null, firstNode = null;
        for (int i = 0; i < 10; i++) {
            if (firstNode == null) {
                node = firstNode = new Node<Integer>(i);
                continue;
            }
            node.setNext(new Node<Integer>(i));
            node = node.getNext();
        }

        firstNode = reverseList(firstNode);
        for (node = firstNode; node != null; node = node.getNext())
            System.out.println(node);


    }
}
