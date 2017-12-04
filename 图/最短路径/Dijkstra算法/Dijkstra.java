import java.util.*;

class HeadNode<T> {
    T data;
    AdjacentNode firstAdjacentNode;

    public HeadNode(T data) {
        this.data = data;
    }

    public boolean addArch(int to, int weight) {
        if (firstAdjacentNode == null) {
            firstAdjacentNode = new AdjacentNode(to, weight);
            return true;
        }

        AdjacentNode node = firstAdjacentNode;
        AdjacentNode previous = null;
        while (node != null) {
            if (node.index == to) {
                node.weight = weight;
                return false;
            }
            previous = node;
            node = node.next;
        }
        previous.next = new AdjacentNode(to, weight);
        return true;
    }
}

class AdjacentNode {
    int index;
    int weight;
    AdjacentNode next;

    public AdjacentNode(int index, int weight) {
        this.index = index;
        this.weight = weight;
    }
}

class Network<T> {
    List<HeadNode<T>> vertexes = new ArrayList<>();

    public void addVertex(T data) {
        vertexes.add(new HeadNode<T>(data));
    }

    public void addArch(int from, int to, int weight) {
        vertexes.get(from).addArch(to, weight);
    }

    public int[][] dijkstra(int start) {
        int size = vertexes.size();
        // D的每个分量表示一个顶点的最短路径
        int[] D = new int[size];
        // P记录每个顶点的前驱
        int[] P = new int[size];
        // B[i] == Integer.MAX_VALUE 表示无法从A中的顶点直接达到该顶点
        // B[i] == 0 表示该顶点已经在A中
        // 否则，B[i]表示D_estimate[i]
        int[] B = new int[size];
        for (int i = 0; i < size; i++)
            B[i] = Integer.MAX_VALUE;
        D[start] = 0;
        B[start] = 0;

        while (start >= 0) {
            HeadNode<T> headNode = vertexes.get(start);
            AdjacentNode adjacentNode = headNode.firstAdjacentNode;
            while (adjacentNode != null) {
                int index = adjacentNode.index;
                int weight = adjacentNode.weight;
                int estimateValue = D[start] + weight;
                if (B[index] != 0 && estimateValue < B[index]) {
                    B[index] = estimateValue;
                    P[index] = start;
                }
                adjacentNode = adjacentNode.next; 
            }

            start = -1;
            for (int i = 0; i < size; i++) {
                if (B[i] == 0)
                    continue;
                if (start == -1 || B[i] < B[start])
                    start = i;
            }

            if (start != -1) {
                D[start] = B[start];
                B[start] = 0;
            }
        }

        return new int[][]{D, P};
    }
}

public class Dijkstra {
    public static void main(String[] args) {
        Network<Integer> network = new Network<>();
        for (int i = 0; i <= 5; i++)
            network.addVertex(i);
        for (int[] arch: new int[][]{
                new int[]{0, 2, 10}, new int[]{0, 4, 30}, new int[]{0, 5, 100},
                new int[]{1, 2, 5}, new int[]{2, 3, 50}, new int[]{3, 5, 10},
                new int[]{4, 3, 20}, new int[]{4, 5, 60}
            })
            network.addArch(arch[0], arch[1], arch[2]);
        int[][] DP = network.dijkstra(0);
        for (int i = 0; i < DP[0].length; i++)
            System.out.println("i = " + i + ", weight = "
                + DP[0][i] + ", previous = " + DP[1][i]);
    }
}

