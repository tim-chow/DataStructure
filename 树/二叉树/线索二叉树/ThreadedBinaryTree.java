class Node<T> {
    private T element;
    // false means child node, true means threading node
    private boolean ltag = false; 
    private boolean rtag = false;
    private Node<T> left;
    private Node<T> right;
    private Node<T> inOrderThreadingPrevious;

    public Node(T element) {
        this.element = element;
    }

    public T getElement() {
        return element;
    }

    public Node<T> getLeft() {
        return !ltag ? left: null;
    }

    public Node<T> getRight() {
        return !rtag ? right: null;
    }

    public Node<T> getPrevious() {
        return ltag ? left : null;
    }

    public Node<T> getNext() {
        return rtag ? right : null;
    }

    public Node<T> setLeft(Node<T> left) {
        this.left = left;
        ltag = false;
        return this;
    }

    public Node<T> setRight(Node<T> right) {
        this.right = right;
        rtag = false;
        return this;
    }

    public Node<T> setPrevious(Node<T> previous) {
        left = previous;
        ltag = true;
        return this;
    }

    public Node<T> setNext(Node<T> next) {
        right = next;
        rtag = true;
        return this;
    }

    public synchronized void inOrderThreading() {
        inOrderThreadingPrevious = null;
        inOrderThreading(this);
    }

    private void inOrderThreading(Node<T> root) {
        if (root.getLeft() != null)
            inOrderThreading(root.getLeft());
        // here is different from inOrderTraverse
        if (root.getLeft() == null)
            root.setPrevious(inOrderThreadingPrevious);
        if (inOrderThreadingPrevious != null && 
                inOrderThreadingPrevious.getRight() == null) {
            inOrderThreadingPrevious.setNext(root);
        }

        inOrderThreadingPrevious = root;
        //
        if (root.getRight() != null)
            inOrderThreading(root.getRight());
    }

    public void inOrderTraverse1() {
        if (getLeft() != null)
            getLeft().inOrderTraverse1();
        System.out.println(this);
        if (getRight() != null)
            getRight().inOrderTraverse1();
    }

    public void inOrderTraverse2() {
        Node<T> p = this;
        while (p != null) {
            while (p.getLeft() != null)
                p = p.getLeft();
            System.out.println(p);
            
            while (p.getNext() != null) {
                p = p.getNext();
                System.out.println(p);
            }
            p = p.getRight();
        }
    }

    @Override
    public String toString() {
        return element.toString();
    }
}

public class ThreadedBinaryTree {
    public static void main(String[] args) {
        Node<Integer> root = new Node<Integer>(1);
        root.setLeft(new Node<Integer>(2))
            .setRight(new Node<Integer>(3));
        root.getLeft().setLeft(new Node<Integer>(4))
            .setRight(new Node<Integer>(5));
        root.getRight().setRight(new Node<Integer>(7));

        root.inOrderThreading();
        root.inOrderTraverse1();
        root.inOrderTraverse2();
    }
}

