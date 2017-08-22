import java.util.*;

abstract class BaseFrame<T> {
    public abstract BaseFrame<T> execute(int address, Object value);
    public abstract Object getResult();
    public abstract int getReturnAddress();

    public Object run() {
        Stack<BaseFrame<T>> stack = new Stack<>();
        stack.push(this);
        BaseFrame<T> activeFrame, nextFrame;
        int address = 0;
        Object value = null;
        
        while (!stack.empty()) {
            activeFrame = stack.peek();
            nextFrame = activeFrame.execute(address, value);
            if (nextFrame == null) {
                activeFrame = stack.pop();
                address = activeFrame.getReturnAddress();
                value = activeFrame.getResult();
            } else {
                stack.push(nextFrame);
                address = 0;
                value = null;
            }
        }

        return value;
    }
}

abstract class TreeFrame<T> extends BaseFrame<T> {
    private int returnAddress;
    protected BinaryTreeNode<T> root;
    protected  List<BinaryTreeNode<T>> nodes = 
        new ArrayList<>();

    public TreeFrame(int returnAddress,
        BinaryTreeNode<T> root) {
        this.returnAddress = returnAddress;
        this.root = root;
    }

    public int getReturnAddress() {
        return returnAddress;
    }

    public Object getResult() {
        return nodes;
    }
}

class PostOrderFrame<T> extends TreeFrame<T> {
    public PostOrderFrame(int returnAddress,
            BinaryTreeNode<T> root) {
        super(returnAddress, root);
    }

    @Override
    public BaseFrame<T> execute(int address, Object rawValue) {
        if (root == null)
            return null;
        List<BinaryTreeNode<T>> value = 
            (List<BinaryTreeNode<T>>) rawValue;

        switch (address) {
            case 0:
                return new PostOrderFrame<>(1, root.getLeft());
            case 1:
                nodes.addAll(value);
                return new PostOrderFrame<>(2, root.getRight());
            case 2:
                nodes.addAll(value);
                nodes.add(root);
                return null;
        }
        return null;
    }
}

class BinaryTreeNode<T> {
    private T element;
    private BinaryTreeNode left;
    private BinaryTreeNode right;

    public BinaryTreeNode(T element) {
        this.element = element;
    }

    public BinaryTreeNode<T> getLeft() {
        return left;
    }

    public BinaryTreeNode<T> getRight() {
        return right;
    }

    public BinaryTreeNode<T> setLeft(BinaryTreeNode<T> left) {
        this.left = left;
        return this;
    }

    public BinaryTreeNode<T> setRight(BinaryTreeNode<T> right) {
        this.right = right;
        return this;
    }

    public List<BinaryTreeNode<T>> preOrderTraverse() {
        List<BinaryTreeNode<T>> nodes = new ArrayList<>();
        nodes.add(this);
        if (this.getLeft() != null)
            nodes.addAll(this.getLeft().preOrderTraverse());
        if (this.getRight() != null)
            nodes.addAll(this.getRight().preOrderTraverse());
        return nodes;
    }

    public static <T> List<BinaryTreeNode<T>> preOrderTraverse(
        BinaryTreeNode<T> root) {
        List<BinaryTreeNode<T>> nodes = new ArrayList<>();
        nodes.add(root); 
        if (root.getLeft() != null)
            nodes.addAll(preOrderTraverse(root.getLeft()));
        if (root.getRight() != null)
            nodes.addAll(preOrderTraverse(root.getRight()));
        return nodes;
    }

    public List<BinaryTreeNode<T>> inOrderTraverse() {
        List<BinaryTreeNode<T>> nodes = new ArrayList<>();
        if (this.getLeft() != null)
            nodes.addAll(this.getLeft().inOrderTraverse());
        nodes.add(this);
        if (this.getRight() != null)
            nodes.addAll(this.getRight().inOrderTraverse());
        return nodes;
    }

    public List<BinaryTreeNode<T>> postOrderTraverse() {
        List<BinaryTreeNode<T>> nodes = new ArrayList<>();
        if (this.getLeft() != null)
            nodes.addAll(this.getLeft().postOrderTraverse());
        if (this.getRight() != null)
            nodes.addAll(this.getRight().postOrderTraverse());
        nodes.add(this);
        return nodes;
    }

    public static <T> List<BinaryTreeNode<T>> postOrderTraverse(
        BinaryTreeNode<T> root) {
        List<BinaryTreeNode<T>> nodes = new ArrayList<>();
        if (root.getLeft() != null)
            nodes.addAll(postOrderTraverse(root.getLeft()));
        if (root.getRight() != null)
            nodes.addAll(postOrderTraverse(root.getRight()));
        nodes.add(root);
        return nodes;
    }

    public static <T> List<BinaryTreeNode<T>> BFS(BinaryTreeNode<T> root) {
        List<BinaryTreeNode<T>> queue = new ArrayList<>();
        queue.add(root);
        BinaryTreeNode<T> node;

        for (int i=0; i<queue.size(); ++i) {
            node = queue.get(i);
            if (node.getLeft() != null)
                queue.add(node.getLeft());
            if (node.getRight() != null)
                queue.add(node.getRight());
        }
        return queue;
    }

    public String toString() {
        return element.toString();
    }
}

public class BinaryTree {
    public static void main(String[] args) {
        BinaryTreeNode<Integer> root = new BinaryTreeNode<>(100);
        BinaryTreeNode<Integer> left, right;
        root.setLeft(left = new BinaryTreeNode<Integer>(200))
            .setRight(right = new BinaryTreeNode<Integer>(300));
        left.setLeft(new BinaryTreeNode<Integer>(400))
            .setRight(null);
        right.setLeft(new BinaryTreeNode<Integer>(500))
            .setRight(new BinaryTreeNode<Integer>(600));

        System.out.println(root.preOrderTraverse());
        System.out.println(BinaryTreeNode.preOrderTraverse(root));

        System.out.println(root.inOrderTraverse());
        System.out.println(root.postOrderTraverse());
        System.out.println(BinaryTreeNode.postOrderTraverse(root));
        System.out.println((List<BinaryTreeNode<Integer>>)
            new PostOrderFrame<Integer>(-1, root).run());
        System.out.println(BinaryTreeNode.BFS(root));
    }
}
