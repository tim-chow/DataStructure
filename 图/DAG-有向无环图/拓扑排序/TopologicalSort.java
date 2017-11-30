import java.util.*;

class HeadNode<T> {
    private int inDegree;
    private T data;
    private AdjacentNode firstChildNode;

    public HeadNode(T data) {
        this.data = data;
    }

    public HeadNode<T> increaseInDegree(int degree) {
        inDegree += degree;
        return this;
    }

    public HeadNode<T> addAjacentNode(int to, int weight) {
        if (firstChildNode == null) {
            firstChildNode = new AdjacentNode(to, weight);
            return this;
        }

        AdjacentNode node = firstChildNode;
        while (node.getNext() != null) {
            node = node.getNext();
            if (node.getIndex() == to) {
                node.setWeight(weight);
                return null;
            }
        }
        node.setNext(new AdjacentNode(to, weight));
        return this;
    }

    public AdjacentNode getNext() {
        return firstChildNode;
    }

    public HeadNode<T> setFirstChildNode(AdjacentNode adjacentNode) {
        firstChildNode = adjacentNode;
        return this;
    }

    public int getInDegree() {
        return inDegree;
    }

    public T getData() {
        return data;
    }
}

class AdjacentNode {
    private AdjacentNode next;
    private int index;
    private int weight;

    public AdjacentNode(int index, int weight) {
        this.index = index;
        this.weight = weight;
    }

    public AdjacentNode setNext(AdjacentNode next) {
        this.next = next;
        return this;
    }

    public AdjacentNode getNext() {
        return next;
    }

    public int getIndex() {
        return index;
    }

    public int getWeight() {
        return weight;
    }

    public AdjacentNode setWeight(int weight) {
        this.weight = weight;
        return this;
    }
}

class Network<T> {
    private List<HeadNode<T>> vertexes = new ArrayList<>();
    
    public Network<T> addVertex(T data) {
        vertexes.add(new HeadNode<T>(data));
        return this;
    }

    public List<HeadNode<T>> getVertexes() {
        return vertexes;
    }

    public Network<T> addArch(int from, int to) {
        int weight = 0;
        HeadNode<T> headNode = vertexes.get(from).addAjacentNode(to, weight);
        if (headNode != null)
            vertexes.get(to).increaseInDegree(1);
        return this;
    }

    public Network<T> deleteArch(int from, int to) {
        AdjacentNode node = vertexes.get(from).getNext();
        AdjacentNode previous = null;
        while (node != null) {
            if (node.getIndex() == to) {
                if (previous == null) {
                    vertexes.get(from).setFirstChildNode(node.getNext());
                } else {
                    previous.setNext(node.getNext());
                }

                vertexes.get(to).increaseInDegree(-1);
                break;
            }
            previous = node;
            node = node.getNext();
        }

        return this;
    }

    public void topologicalSort() {
        Stack<Integer> stack = new Stack<>();
        for (int i = 0; i < vertexes.size(); ++i) {
            if (vertexes.get(i).getInDegree() == 0)
                stack.push(i);
        }

        while (!stack.empty()) {
            int from, to;
            HeadNode<T> headNode = vertexes.get(from = stack.pop());
            // 打印node
            System.out.println(headNode.getData());
            // 删除边
            AdjacentNode adjacentNode = headNode.getNext();
            while (adjacentNode != null) {
                deleteArch(from, to = adjacentNode.getIndex());
                // 如果导致某个邻接点的入度为0，将其加入到stack
                if (vertexes.get(to).getInDegree() == 0)
                    stack.push(to);
                adjacentNode = adjacentNode.getNext();
            }
        }

    }

    // 使用递归形式
    public void DFS() {
        Boolean[] visited = new Boolean[vertexes.size()];
        for (int i = 0; i < visited.length; i++)
            visited[i] = false;
        List<Integer> finished = new ArrayList<>();
        for (int i = 0; i < vertexes.size(); ++i) {
            if (!visited[i])
                DFS(i, visited, finished);
        }
        System.out.println(finished);
    }

    private void DFS(int vertextIndex,
            Boolean[] visited, List<Integer> finished) {
        HeadNode headNode = vertexes.get(vertextIndex);
        AdjacentNode adjacentNode = headNode.getNext();
        while (adjacentNode != null) {
            int adjacentIndex = adjacentNode.getIndex();
            if (!visited[adjacentIndex])
                DFS(adjacentIndex, visited, finished);
            adjacentNode = adjacentNode.getNext();
        }

        if (!visited[vertextIndex]) {
            visited[vertextIndex] = true;
            finished.add(vertextIndex);
        }
    }
}

public class TopologicalSort {
    public static void main(String[] args) {
        Network<Integer> network = new Network<Integer>();
        List<HeadNode<Integer>> vertexes = network.getVertexes();
        int i = 0;
        while (i <= 12) {
            network.addVertex(i);
            i++;
        }
        for (int[] arch:
            new int[][]{new int[]{0, 1}, new int[]{0, 5}, new int[]{0, 6},
                new int[]{2, 0}, new int[]{2, 3},
                new int[]{3, 5}, new int[]{5, 4}, new int[]{6, 4}, new int[]{6, 9},
                new int[]{7, 6}, new int[]{8, 7}, 
                new int[]{9, 10}, new int[]{9, 11}, new int[]{9, 12},
                new int[]{11, 12}
        })
        network.addArch(arch[0], arch[1]);
        //network.topologicalSort();
        System.out.println("==========");
        network.DFS();
    }
}

