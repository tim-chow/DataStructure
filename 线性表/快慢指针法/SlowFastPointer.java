public class SlowFastPointer {
    public static class Node<T> {
        private T data;
        private Node<T> next;

        public void setNext(Node<T> next) {
            this.next = next;
        }

        public Node<T> getNext() {
            return next;
        }

        public Node(T data) {
            this.data = data;
        }

        public String toString() {
            return String.format("Node{data=%s}", data);
        }
    }

    // 利用快慢指针求链表中间节点
    public static <T> Node<T> getMiddle(Node<T> node) {
        Node<T> slow = node, fast = node;
        while (fast != null && fast.getNext() != null) {
            slow = slow.getNext();
            fast = fast.getNext().getNext();
        }
        return slow;
    }

    // 利用快慢指针求链表的倒数第K个节点
    public static <T> Node<T> getKth(Node<T> node, int k) {
        Node<T> slow = node, fast = node;
        // 快指针先走K步
        for (int i = 0; i < k - 1 && fast != null; i++)
            fast = fast.getNext();
        while (fast != null) {
            fast = fast.getNext();
            slow = slow.getNext();
        }
        return slow;
    }


    public static void main(String[] args) {
        Node<Integer> node = null, firstNode = null;
        for (int i = 0; i < 9; i++) {
            if (node == null) {
                firstNode = new Node<Integer>(i);
                node = firstNode;
                continue;
            }
            node.setNext(new Node<Integer>(i));
            node = node.getNext();
        }

        System.out.println(getMiddle(firstNode));
        System.out.println(getKth(firstNode, 3));
    }
}
