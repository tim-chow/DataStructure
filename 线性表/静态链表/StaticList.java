@SuppressWarnings("unchecked")
public class StaticList<T> {
    public static class Node<T> {
        private T data;
        private int cursor;

        public Node(T data, int cursor) {
            this.data = data;
            this.cursor = cursor;
        }

        private void setCursor(int cursor) {
            this.cursor = cursor;
        }

        public int getCursor() {
            return cursor;
        }

        private void setData(T data) {
            this.data = data;
        }

        public T getData() {
            return data;
        }

        @Override
        public String toString() {
            return "Node{" +
                    "data=" + data +
                    ", cursor=" + cursor +
                    '}';
        }
    }

    private Node<T>[] underlying;
    private Node<T> head, space;

    public StaticList(int totalLength) {
        if (totalLength < 3)
            throw new RuntimeException("totalLength < 3");

        underlying = (Node<T>[]) new Node<?>[totalLength];
        underlying[0] = space = new Node<T>(null, 0);
        int i = 0;
        for (; i < totalLength - 1; i++) {
            underlying[i + 1] = new Node<T>(null, 0);
            underlying[i].setCursor(i + 1);
        }
        underlying[i].setCursor(0);
        head = underlying[malloc()];
        head.setCursor(0);
    }

    public T remove(T data) {
        if (data == null)
            throw new RuntimeException("data == null");

        Node<T> node = head, nextNode;
        int nextIndex, nextNodeIndex;
        while (node.getCursor() != 0) {
            nextNode = underlying[node.getCursor()];
            if (data.equals(nextNode.getData())) {
                nextIndex = nextNode.getCursor();
                nextNodeIndex = node.getCursor();
                free(nextNodeIndex);
                node.setCursor(nextIndex);
                return data;
            }
            node = underlying[node.getCursor()];
        }
        return null;
    }

    public boolean add(T data) {
        if (data == null)
            throw new RuntimeException("data == null");

        int index = malloc();
        // 没有空闲节点
        if (index == 0)
            return false;

        underlying[index].setData(data);
        underlying[index].setCursor(0);

        Node<T> node = head;
        while (node.getCursor() != 0)
            node = underlying[node.getCursor()];
        node.setCursor(index);
        return true;
    }

    // 将index放到备用链表表头
    private void free(int index) {
        underlying[index].setCursor(space.getCursor());
        space.setCursor(index);
    }

    // 从备用链表表头获取空闲节点
    private int malloc() {
        int index;
        if ((index = space.getCursor()) == 0)
            return 0;
        space.setCursor(underlying[index].getCursor());
        return index;
    }

    public static void main(String[] args) {
        StaticList<Integer> staticList = new StaticList<Integer>(4);
        System.out.println(staticList.add(1));
        System.out.println(staticList.add(2));
        System.out.println(staticList.add(3));
        System.out.println(staticList.remove(2));
        System.out.println(staticList.remove(333));
        System.out.println(staticList.add(3));
        System.out.println(staticList.remove(1));
        System.out.println(staticList.add(2));
        System.out.println(staticList.remove(3));
        int index = 0;
        for (Node<Integer> element: staticList.underlying)
            System.out.println("index = " + index++ + ", element = " + element);
    }
}
