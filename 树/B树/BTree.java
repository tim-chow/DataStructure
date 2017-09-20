import java.util.*;

class BTreeNode<T extends Comparable> {
    private int m; // 阶数
    private BTreeNode<T> parent; // 父节点
     // 关键字列表
    private List<T> keyWords = new ArrayList<>();
    // 儿子节点列表
    private List<BTreeNode<T>> children = new ArrayList<>();

    public BTreeNode(int m) {
        if (m < 3) 
            throw new RuntimeException("m < 3");
        this.m = m;
    }

    public int getM() {
        return m;
    }

    private BTreeNode<T> getParent() {
        return parent;
    }

    private BTreeNode<T> setParent(BTreeNode<T> parent) {
        this.parent = parent;
        return this;
    }

    private List<T> getKeyWords() {
        return keyWords;
    }

    private BTreeNode<T> getChild(int index) {
        return children.get(index);
    }

    private BTreeNode<T> addChild(BTreeNode<T> child) {
        children.add(child);
        return this;
    }

    private BTreeNode<T> addChild(int index, BTreeNode<T> child) {
        children.add(index, child);
        return this;
    }

    private BTreeNode<T> setKeyWord(int index, T keyWord) {
        keyWords.set(index, keyWord);
        return this;
    }

    private int[] addKeyWord(T keyWord) {
        if (keyWords.size() == 0) {
            keyWords.add(keyWord);
            return null;
        }

        // 利用二分查找算法寻找插入位置
        int[] position = BinarySearch.binarySearch(keyWords, keyWord);
        keyWords.add(position[1], keyWord);
        return position;
    }

    private void addKeyWord(int index, T keyWord) {
        keyWords.add(index, keyWord);
    }

    public boolean isLeafNode() {
        return children.size() == 0;
    }

    public int getKeyWordCount() {
        return keyWords.size();
    }

    private T getKeyWord(int index) {
        return keyWords.get(index);
    }

    private T removeKeyWord(int index) {
        return keyWords.remove(index);
    }

    public void insert(T element) {
        if (element == null)
            throw new RuntimeException("element == null");

        BTreeNode<T> node = this;
        int[] position;
        while (node != null) {
            position = BinarySearch.binarySearch(node.getKeyWords(), element);
            if (node.isLeafNode()) {
                node.addKeyWord(position[1], element);
                // 根节点关键字个数是1到m-1
                if (node.getParent() == null &&
                    node.getKeyWordCount() >= 1 &&
                    node.getKeyWordCount() <= node.getM() - 1)
                    break;
                split(node); // 插入之后，按需进行分裂
                break;
            }
            node = node.getChild(position[1]);
        }
    }

    // 判断是否需要进行分裂
    public static boolean isSatisfy(int m, int size) {
        if (m % 2 == 1 && (m+1)/2-1 <= size && size <= m-1)
            return true;
        if (m % 2 == 0 && m/2-1 <= size && size <= m-1)
            return true;
        return false;
    }

    private BTreeNode<T> removeChild(int index) {
        return children.remove(index);
    }

    private static <T extends Comparable> void split(BTreeNode<T> node) {
        while (node != null && node.getKeyWordCount() > 0 &&
                    !isSatisfy(node.getM(), node.getKeyWordCount())) {
            int middle = node.getKeyWordCount() / 2;
            BTreeNode<T> right = new BTreeNode<>(node.getM());

            for (int ind=0; node.getKeyWordCount() > middle + 1; ind++) {
                right.addKeyWord(ind, node.removeKeyWord(middle + 1));
                if (!node.isLeafNode())
                    right.addChild(node.removeChild(middle + 1).setParent(right));
            }
            if (!node.isLeafNode())
                right.addChild(node.removeChild(middle + 1).setParent(right));

            // 如果node是根节点
            if (node.getParent() == null) {
                BTreeNode<T> left = new BTreeNode<>(node.getM());
                for (int ind=0; node.getKeyWordCount() > 1; ind++) {
                    left.addKeyWord(ind, node.removeKeyWord(0));
                    if (!node.isLeafNode())
                        left.addChild(node.removeChild(0).setParent(left));
                }
                if (!node.isLeafNode())
                    left.addChild(node.removeChild(0).setParent(left));

                node.addChild(left.setParent(node))
                    .addChild(right.setParent(node));
                break;
            }

            T keyWord = node.removeKeyWord(middle);
            int[] position = node.getParent().addKeyWord(keyWord);
            node.getParent().addChild(position[1] + 1,
                right.setParent(node.getParent()));
            node = node.getParent();
        }
    }

    @Override
    public String toString() {
        return String.format("BTreeNode{keyWords=%s, children=%s}",
            keyWords, children);
    }

    public static class SearchResult<T extends Comparable> {
        public BTreeNode<T> node;
        public int position;

        public SearchResult(BTreeNode<T> node, int position) {
            this.node = node;
            this.position = position;
        }

        @Override
        public String toString() {
            return String.format("SearchResult{node=%s, position=%d}", node, position);
        }
    }

    public SearchResult<T> search(T element) {
        if (element == null)
            throw new RuntimeException("element == null");

        BTreeNode<T> node = this;
        while (node != null) {
            int[] position = BinarySearch.binarySearch(
                node.getKeyWords(), element);
            if (position[0] == position[1])
                return new SearchResult<T>(node, position[1]);
            if (node.isLeafNode())
                break;
            node = node.getChild(position[1]);
        }

        return null;
    }

    public BTreeNode<T> delete(T element) {
        SearchResult<T> searchResult = search(element);
        if (searchResult == null)
            return this;

        BTreeNode<T> node = searchResult.node;
        if (!node.isLeafNode()) {
            BTreeNode<T> realDeletedNode = node;
            realDeletedNode = node.getChild(searchResult.position + 1);
            while (!realDeletedNode.isLeafNode())
                realDeletedNode = realDeletedNode.getChild(0);
            node.setKeyWord(searchResult.position,
                realDeletedNode.getKeyWord(0));
            realDeletedNode.removeKeyWord(0);
            node = realDeletedNode;
        } else
            node.removeKeyWord(searchResult.position);

        if (node.getParent() == null)
            return this;

        adjust(node); 

        return this;
    }

    private static boolean canBorrow(int m, int size) {
        if (m%2 == 1 && size > (m+1)/2-1)
            return true;
        if (m%2 == 0 && size > m/2-1)
            return true;
        return false;
    }

    private int getChildIndex(BTreeNode<T> node) {
        return children.indexOf(node);
    }

    public int getChildCount() {
        return children.size();
    }

    // 非常值得注意的是一定要更改子节点的父指针的指向
    private static <T extends Comparable> void adjust(BTreeNode<T> node) {
        while (node != null &&
                !isSatisfy(node.getM(), node.getKeyWordCount())) {
            BTreeNode<T> parent = node.getParent();
            int index = parent.getChildIndex(node);
            BTreeNode<T> leftBrother = null;
            BTreeNode<T> rightBrother = null;

            if (index == 0)
                rightBrother = parent.getChild(index + 1);
            else if (index == parent.getChildCount() - 1)
                leftBrother = parent.getChild(index - 1);
            else {
                leftBrother = parent.getChild(index - 1);
                rightBrother = parent.getChild(index + 1);
            }

            // 从右孩子借
            if (rightBrother != null &&
                canBorrow(rightBrother.getM(),
                    rightBrother.getKeyWordCount())) {
                T borrowedKeyWord = rightBrother.removeKeyWord(0);
                BTreeNode<T> borrowedChild = null;
                if (!rightBrother.isLeafNode())
                    borrowedChild = rightBrother.removeChild(0);
                T parentKeyWord = parent.getKeyWord(index);
                parent.setKeyWord(index, borrowedKeyWord);

                node.addKeyWord(node.getKeyWordCount(), parentKeyWord);
                if (borrowedChild != null)
                    node.addChild(borrowedChild.setParent(node));
                break;
            }

            // 从左孩子借
            if (leftBrother != null &&
                canBorrow(leftBrother.getM(),
                    leftBrother.getKeyWordCount())) {
                T borrowedKeyWord = leftBrother.removeKeyWord(
                    leftBrother.getKeyWordCount() - 1);
                BTreeNode<T> borrowedChild = null;
                if (!leftBrother.isLeafNode())
                    borrowedChild = leftBrother.removeChild(
                        leftBrother.getChildCount() - 1);
                T parentKeyWord = parent.getKeyWord(index - 1);
                parent.setKeyWord(index - 1, borrowedKeyWord);
                
                node.addKeyWord(0, parentKeyWord);
                if (borrowedChild != null)
                    node.addChild(0, borrowedChild.setParent(node));
                break;
            }

            // 与右孩合并
            if (rightBrother != null) {
                T parentKeyWord = parent.removeKeyWord(index);
                parent.removeChild(index + 1);
                node.addKeyWord(node.getKeyWordCount(), parentKeyWord);

                while (rightBrother.getKeyWordCount() > 0) {
                    node.addKeyWord(
                        node.getKeyWordCount(),
                        rightBrother.removeKeyWord(0));
                }
                while (rightBrother.getChildCount() > 0)
                    node.addChild(rightBrother.removeChild(0).setParent(node));
            }
            // 与左孩子合并
            else {
                // 把node合并到它的左兄弟，比把node的左兄弟合并到node要简单点
                T parentKeyWord = parent.removeKeyWord(index - 1);
                parent.removeChild(index);
                leftBrother.addKeyWord(
                    leftBrother.getKeyWordCount(),
                    parentKeyWord);

                while (node.getKeyWordCount() > 0) {
                    leftBrother.addKeyWord(
                        leftBrother.getKeyWordCount(),
                            node.removeKeyWord(0));
                }
                while (node.getChildCount() > 0)
                    leftBrother.addChild(node.removeChild(0).setParent(leftBrother));
                node = leftBrother;
            }

            if (parent.getParent() == null) {
                if (parent.getKeyWordCount() >= 1)
                    break;

                parent.removeChild(0);
                while (node.getKeyWordCount() > 0) {
                    parent.addKeyWord(
                        parent.getKeyWordCount(),
                        node.removeKeyWord(0));
                }
                while (node.getChildCount() > 0)
                    parent.addChild(node.removeChild(0).setParent(parent));
                break;
            }
            node = parent;
        }
    }
}

public class BTree {
    public static void main(String[] args) {
        BTreeNode<Integer> root = new BTreeNode<>(5);
        for (int element: new int[]{
26, 46, 12, 20, 14, 45, 9, 35, 5, 23, 40, 24, 2, 15, 
25, 21, 49, 22, 18, 42, 38, 7, 3, 27, 11, 31, 16, 41, 
19, 28, 4, 34, 1, 29, 43, 10, 32, 8, 13, 33, 44, 37, 
36, 39, 30, 47, 17, 48, 0, 6
        })
            root.insert(element);
        System.out.println(root);
        System.out.println("\n");

        for (int element: new int[]{
5, 13, 33, 10, 23, 40, 12, 27, 9, 15, 34, 1, 47, 41, 
19, 46, 6, 11, 32, 35, 2, 7, 43, 3, 16, 14, 24, 45, 49, 
36, 25, 4, 48, 22, 42, 31, 38, 17, 20, 44, 29, 37, 26, 
28, 39, 0, 18, 21, 8, 30
        })
        {
            System.out.println(element);
            System.out.println(root.delete(element));
        }
    }
}

