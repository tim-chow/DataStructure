import java.util.*;

class BPlusTreeNode<T extends Comparable> {
    private int m; // 阶数(大于等于2)
    private List<T> keyWords = new ArrayList<>();
    private List<BPlusTreeNode<T>> children = new ArrayList<>();
    private BPlusTreeNode<T> parent = null;
    // 通过next指针将B+树的叶子节点连接起来，
    // + 在本实现中，根节点的next指针指向最左的叶子节点，
    // + 非终端节点的next指针都是空的，
    // + 最右面的叶子节点的next指针也是空的
    private BPlusTreeNode<T> next = null;

    public BPlusTreeNode(int m) {
        if (m < 2)
            throw new RuntimeException("m < 2");
        this.m = m;
    }

    public int getM() {
        return m;
    }

    public int getKeyWordCount() {
        return keyWords.size();
    }

    private List<T> getKeyWords() {
        return keyWords;
    }

    private BPlusTreeNode<T> addKeyWord(T keyWord) {
        keyWords.add(keyWord);
        return this;
    }

    private BPlusTreeNode<T> addKeyWord(int index, T keyWord) {
        keyWords.add(index, keyWord);
        return this;
    }

    private BPlusTreeNode<T> setKeyWord(int index, T keyWord) {
        keyWords.set(index, keyWord);
        return this;
    }

    private T removeKeyWord(int index) {
        return keyWords.remove(index);
    }

    public T getKeyWord(int index) {
        return keyWords.get(index);
    }

    private BPlusTreeNode<T> addChild(BPlusTreeNode<T> child) {
        children.add(child);
        return this;
    }

    private BPlusTreeNode<T> addChild(int index, BPlusTreeNode<T> child) {
        children.add(index, child);
        return this;
    }

    public BPlusTreeNode<T> getChild(int index) {
        return children.get(index);
    }

    private BPlusTreeNode<T> removeChild(int index) {
        return children.remove(index);
    }

    private int getChildIndex(BPlusTreeNode<T> child) {
        return children.indexOf(child);
    }

    public int getChildCount() {
        return children.size();
    }

    public boolean isLeafNode() {
        return children.size() == 0;
    }

    private BPlusTreeNode<T> setParent(BPlusTreeNode<T> parent) {
        this.parent = parent;
        return this;
    }

    public BPlusTreeNode<T> getParent() {
        return parent;
    }

    private BPlusTreeNode<T> setNext(BPlusTreeNode<T> next) {
        this.next = next;
        return this;
    }

    public BPlusTreeNode<T> getNext() {
        return next;
    }

    public static class SearchResult<T extends Comparable> {
        public BPlusTreeNode<T> node;
        public int position;

        public SearchResult(BPlusTreeNode<T> node, int position) {
            this.node = node;
            this.position = position;
        }

        @Override
        public String toString() {
            return String.format("SearchResult{node=%s, position=%d}", node, position);
        }
    }

    public void insert(T element) {
        if (element == null)
            throw new RuntimeException("element == null");
        if (getKeyWordCount() == 0) {
            // 第一个叶子节点，也就是根节点的next指向的节点
            BPlusTreeNode<T> firstLeafNode = new BPlusTreeNode<>(getM());
            firstLeafNode.setParent(this).addKeyWord(element);
            this.setNext(firstLeafNode)
                .addChild(firstLeafNode)
                .addKeyWord(element);
            return;
        }

        BPlusTreeNode<T> node = this;
        while (node != null) {
            int[] position = BinarySearch.binarySearch(node.getKeyWords(), element);
            // 如果b+树中，已经存在该关键字，则直接返回
            if (position[0] == position[1])
                break;
            
            // 所有的插入都发生在叶子节点
            if (node.isLeafNode()) {
                node.addKeyWord(position[1], element);
                // 如果根节点只有一个儿子，并且该儿子是叶子节点，
                // + 那么该叶子节点，无需满足最小关键字个数的限制
                if (node.getParent() == this &&
                        node.getParent().getChildCount() == 1 &&
                        node.getKeyWordCount() <= node.getM())
                    break;
                // 超过最大关键字个数的限制，则进行分裂
                split(node);
                break;
            }

            int insertPosition = position[0];
            if (position[0] == -1) {
                // 如果要插入的关键字，比B树中任何节点都小，
                // + 那么在插入过程中，需要更新索引节点
                insertPosition = position[1];
                node.setKeyWord(insertPosition, element);
            }
            node = node.getChild(insertPosition);
        }
    }

    public static boolean isSatisfy(int m, int size) {
        if (size > m)
            return false;
        return size >= (m + m % 2) / 2;
    }

    private void split(BPlusTreeNode<T> node) {
        while (node != null && !isSatisfy(node.getM(), node.getKeyWordCount())) {
            int middle = node.getKeyWordCount() / 2;
            BPlusTreeNode<T> parent = node.getParent();

            // 所有的分裂都是从左向右分裂，这样方便处理next指针
            BPlusTreeNode<T> right = new BPlusTreeNode<>(node.getM());
            right.setParent(parent);
            while (node.getKeyWordCount() > middle) {
                right.addKeyWord(node.removeKeyWord(middle));
                if (!node.isLeafNode())
                    right.addChild(node.removeChild(middle).setParent(right));
            }

            if (node.isLeafNode())
                node.setNext(right.setNext(node.getNext()));

            // 要分裂的节点是根节点
            if (parent == null) {
                BPlusTreeNode<T> left = new BPlusTreeNode<>(node.getM());
                while (node.getKeyWordCount() > 0)
                    left.addKeyWord(node.removeKeyWord(0))
                        .addChild(node.removeChild(0).setParent(left));
                node.addChild(left.setParent(node))
                    .addChild(right.setParent(node))
                    .addKeyWord(left.getKeyWord(0))
                    .addKeyWord(right.getKeyWord(0)); 
                break;
            }

            int[] position = BinarySearch.binarySearch(parent.getKeyWords(), right.getKeyWord(0));
            parent.addKeyWord(position[1], right.getKeyWord(0));
            parent.addChild(position[1], right);

            node = parent;
            // 根节点特殊：没有最小关键字个数的限制，只有最大关键字个数的限制
            if (node.getParent() == null && node.getKeyWordCount() <= node.getM())
                break;
        }
    }

    public SearchResult<T> search(T element) {
        if (element == null)
            throw new RuntimeException("element == null");
        if (getKeyWordCount() == 0) // 空树
            return null;

        BPlusTreeNode<T> node = this;
        while (node != null) {
            int[] position = BinarySearch.binarySearch(node.getKeyWords(), element);
            if (position[0] == -1) 
                break;
            if (position[0] != position[1] && node.isLeafNode())
                break;
            if (position[0] == position[1] && node.isLeafNode())
                return new SearchResult<T>(node, position[0]);
            node = node.getChild(position[0]);
        }

        return null;
    }

    @Override
    public String toString() {
        return String.format("BPlusTreeNode{keyWords=%s, children=%s, m=%d}", 
            keyWords, children, m);
    }

    public void delete(T element) {
        // 首先找到要删除的关键字
        SearchResult<T> searchResult = search(element);
        if (searchResult == null)
            return;

        // 把该关键字从叶子节点中删掉
        BPlusTreeNode<T> node = searchResult.node;
        int position = searchResult.position;
        node.removeKeyWord(position);

        // 如果删除关键字之后，节点的关键字个数为0
        // 需要将空分支删掉
        if (node.getKeyWordCount() == 0) {
            BPlusTreeNode<T> temp = node;
            while (temp.getKeyWordCount() == 0 && temp.getParent() != null) {
                int index = temp.getParent().getChildIndex(temp);
                temp.getParent().removeKeyWord(index);
                temp.getParent().removeChild(index);
                temp = temp.getParent();
            }
            if (this.getNext() == node)
                this.setNext(node.getNext());
            if (temp.getParent() == null)
                return;
            node = temp;
        }

        // 按需修改索引
        if (position == 0) {
            BPlusTreeNode<T> temp = node.getParent();
            while (temp != null) {
                int[] index = BinarySearch.binarySearch(temp.getKeyWords(), element);
                if (index[0] != index[1])
                    break;
                temp.setKeyWord(index[0], node.getKeyWord(0));
                temp = temp.getParent();
            }
        }

        adjust(node);
    }

    private boolean canBorrow() {
        return getKeyWordCount() > (getM()+getM()%2)/2;
    }

    private void adjust(BPlusTreeNode<T> node) {
        while (!isSatisfy(node.getM(), node.getKeyWordCount())) {
System.out.println("not satisfy");
System.out.println(node);
            BPlusTreeNode<T> parent = node.getParent();
            BPlusTreeNode<T> leftBrother = null;
            BPlusTreeNode<T> rightBrother = null;
            int index = parent.getChildIndex(node);

            if (index == 0 && parent.getChildCount() >= 2)
                rightBrother = parent.getChild(index + 1);
            else if (index == parent.getChildCount() - 1
                    && parent.getChildCount() >= 2)
                leftBrother = parent.getChild(index - 1);
            else if (parent.getChildCount() >= 3) {
                leftBrother = parent.getChild(index - 1);
                rightBrother = parent.getChild(index + 1);
            }
System.out.println("leftBrother = " + leftBrother);
System.out.println("rightBrother = " + rightBrother);

            // 从右兄弟借一个关键字
            if (rightBrother != null && rightBrother.canBorrow()) {
                T borrowedKeyWord = rightBrother.removeKeyWord(0);
                node.addKeyWord(borrowedKeyWord);
                parent.setKeyWord(index+1, rightBrother.getKeyWord(0));
                if (!rightBrother.isLeafNode())
                    node.addChild(rightBrother.removeChild(0).setParent(node));
                break;
            }
            if (leftBrother != null && leftBrother.canBorrow()) { // 从左兄弟借一个关键字
                T borrowedKeyWord = leftBrother.removeKeyWord(
                    leftBrother.getKeyWordCount() - 1);
                node.addKeyWord(0, borrowedKeyWord);
                parent.setKeyWord(index, borrowedKeyWord);
                if (!leftBrother.isLeafNode())
                    node.addChild(leftBrother.removeChild(
                        leftBrother.getChildCount() - 1).setParent(node));
                break;
            }

            if (rightBrother != null) { // 将右兄弟合并到node
System.out.println("merge rightBrother");
                parent.removeKeyWord(index + 1);
                parent.removeChild(index + 1);
                while (rightBrother.getKeyWordCount() > 0)
                    node.addKeyWord(rightBrother.removeKeyWord(0));
                while (rightBrother.getChildCount() > 0)
                    node.addChild(rightBrother.removeChild(0).setParent(node));
                if (node.isLeafNode())
                    node.setNext(rightBrother.getNext());
            } else if (leftBrother != null) { // 将node合并到左兄弟
System.out.println("merge into leftBrother");
                parent.removeKeyWord(index);
                parent.removeChild(index);
                while (node.getKeyWordCount() > 0)
                    leftBrother.addKeyWord(node.removeKeyWord(0));
                while (node.getChildCount() > 0)
                    leftBrother.addChild(node.removeChild(0).setParent(leftBrother));
                if (node.isLeafNode())
                    leftBrother.setNext(node.getNext());
                node = leftBrother;
            } else { //既没左兄弟、也没右兄弟
System.out.println("no brothers");
                // 父节点是根节点
                if (parent.getParent() == null) {
System.out.println("parent is root");
                    if (node.isLeafNode() && parent.getChildCount() == 1)
                        break;
System.out.println("replace root");
                    parent.removeKeyWord(0); parent.removeChild(0);
                    while (node.getKeyWordCount() > 0)
                        parent.addKeyWord(node.removeKeyWord(0));
                    while (node.getChildCount() > 0)
                        parent.addChild(node.removeChild(0).setParent(parent)); 
                    break;
                }
            }

            if (parent.getParent() == null)
                break;
            node = parent;
        }
    }
}

public class BPlusTree {
    public static void main(String[] args) {
        BPlusTreeNode<Integer> root = new BPlusTreeNode<>(4);
        for (int element: new int[]{24, 23, 15, 21, 1, 14, 27, 12, 9, 18, 3, 8, 25, 16, 10, 0, 20, 6, 4, 22, 28, 2, 11, 29, 19, 5, 7, 26, 17, 13})
            root.insert(element);
        System.out.println(root);

         for (int element: new int[]{17, 8, 1, 4, 21, 22, 12, 18, 9, 28, 15, 7, 13, 14, 5, 23, 24, 11, 25, 10, 29, 16, 19, 26, 2, 27, 20, 0, 6, 3}) {
             System.out.println(root);
             System.out.println("delete " + element);
             root.delete(element);
             System.out.println(root);
             System.out.println("next is: " + root.getNext());
             System.out.println("\n");
        }
    }
}

