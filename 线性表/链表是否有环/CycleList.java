public class CycleList {
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

    public static <T> boolean isCycle(Node<T> firstNode) {
        Node<T> slow = firstNode, fast = firstNode;

        while (fast != null && fast.getNext() != null) {
            fast = fast.getNext().getNext();
            slow = slow.getNext();

            if (fast == slow)
                return true;
        }
        return false;
    }

    public static <T> int cycleLength(Node<T> firstNode) {
        Node<T> slow = firstNode, fast = firstNode;
        int count = 0, start = 0;
        boolean isFirst = true;
        while (fast != null && fast.getNext() != null) {
            fast = fast.getNext().getNext();
            slow = slow.getNext();
            count++;

            if (fast == slow) {
                if (isFirst) {
                    isFirst = false;
                    start = count;
                    continue;
                }
                return count - start;
            }
        }
        return 0;
    }

    public static <T> Node<T> findJointNode(Node<T> firstNode) {
        Node<T> slow = firstNode, fast = firstNode, meetPoint = null;

        while (fast != null && fast.getNext() != null) {
            fast = fast.getNext().getNext();
            slow = slow.getNext();

            if (fast == slow) {
                meetPoint = fast;
                break;
            }
        }

        if (meetPoint == null)
            return null;
        slow = firstNode;

        while (slow != meetPoint) {
            slow = slow.getNext();
            meetPoint = meetPoint.getNext();
        }
        return meetPoint;
    }

    public static void main(String[] args) {
        Node<Integer> firstNode = null, node = null, jointNode = null;
        for (int i = 0; i < 10; i++) {
            if (firstNode == null) {
                node = firstNode = new Node<Integer>(i);
                continue;
            }
            node.setNext(new Node<Integer>(i));
            if (i == 4)
                jointNode = node.getNext();
            node = node.getNext();
        }
        node.setNext(jointNode);

        System.out.println(isCycle(firstNode));
        System.out.println(cycleLength(firstNode));
        System.out.println(findJointNode(firstNode));
    }
}
