import java.util.*;

class Node<T> implements Comparable {
    private T element;
    private int weight;
    private Node<T> left;
    private Node<T> right;
    private String code = "";

    public Node<T> setElement(T element) {
        this.element = element;
        return this;
    }

    public T getElement() {
        return element;
    }

    public Node<T> setWeight(int weight) {
        this.weight = weight;
        return this;
    }

    public int getWeight() {
        return weight;
    }

    public Node<T> setLeft(Node<T> left) {
        this.left = left;
        return this;
    }

    public Node<T> getLeft() {
        return left;
    }

    public Node<T> setRight(Node<T> right) {
        this.right = right;
        return this;
    }

    public Node<T> getRight() {
        return right;
    }

    public int compareTo(Object object) {
        Node<T> node = (Node<T>) object;
        if (getWeight() > node.getWeight())
            return 1;
        if (getWeight() == node.getWeight())
            return 0;
        return -1;
    }

    @Override
    public String toString() {
        return String.format("Node{element=%s, weight=%d, code=%s" + 
            " left=%s, right=%s}", element, weight, code, left, right);
    }

    public String getCode() {
        return code;
    }

    private Node<T> setCode(String code) {
        this.code = code;
        return this;
    }

    public Map<T, String> generateCode() {
        Map<T, String> map = new HashMap<>();
        List<Node<T>> queue = new ArrayList<>();
        queue.add(this);

        while (queue.size() > 0) {
            Node<T> node = queue.remove(0);
            if (node.getLeft() != null) {
                node.getLeft().setCode(node.getCode() + "0");
                queue.add(node.getLeft());
            }
            if (node.getRight() != null) {
                node.getRight().setCode(node.getCode() + "1");
                queue.add(node.getRight());
            }

            if (node.getLeft() == null && node.getRight() == null) {
                map.put(node.getElement(), node.getCode());
            }
        }
        return map;
    }
}

public class HuffmanTree {
    public static String encode(String string, Map<Character, String> codeMap) {
        StringBuilder sb = new StringBuilder();
        for (int index=0; index<string.length(); index++)
            sb.append(codeMap.get(string.charAt(index)));
        return sb.toString();
    }

    public static String decode(String encodedString, Node<Character> root) {
        StringBuilder sb = new StringBuilder();
        Node<Character> node = root;
        int i = 0;
        while (i < encodedString.length()) {
            if (encodedString.charAt(i) == '0')
                node = node.getLeft();
            else
                node = node.getRight();

            if (node.getLeft() == null && node.getRight() == null) {
                sb.append(node.getElement());
                node = root;
            }
            i++;
        }
        return sb.toString();
    }

    public static <T> Node<T> createHuffmanTree(Map<T, Integer> elements) {
        List<Node<T>> nodeList = new ArrayList<>();
        for (Map.Entry<T, Integer> entry: elements.entrySet()) {
            Node<T> newNode = (new Node<T>())
                                .setElement(entry.getKey())
                                .setWeight(entry.getValue());
            if (nodeList.size() == 0) {
                nodeList.add(newNode);
                continue;
            }
            int[] position = BinarySearch.binarySearch(nodeList, newNode);
            nodeList.add(position[1], newNode);
        }

        while (nodeList.size() > 1) {
            Node<T> first = nodeList.remove(0);
            Node<T> second  = nodeList.remove(0);
            Node<T> newNode = new Node<T>();
            newNode.setWeight(first.getWeight() + second.getWeight())
                .setLeft(first).setRight(second);
            if (nodeList.size() == 0)
                return newNode;
            int[] position = BinarySearch.binarySearch(nodeList, newNode);
            nodeList.add(position[1], newNode);
        }

        return null;
    }

    public static void main(String[] args) {
        Map<Character, Integer> elements = new HashMap<>();
        elements.put('a', 5);
        elements.put('f', 5);
        elements.put('c', 7);
        elements.put('g', 13);
        elements.put('e', 34);
        elements.put('b', 24);
        elements.put('d', 17);

        Node<Character> root = createHuffmanTree(elements);
        Map<Character, String> codeMap;
        System.out.println(codeMap = root.generateCode());
        String encodedString;
        System.out.println(encodedString = encode("acdgefb", codeMap));
        System.out.println(decode(encodedString, root));
    }
}

