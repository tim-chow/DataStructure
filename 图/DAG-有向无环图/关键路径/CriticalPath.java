import java.util.*;

class HeadNode<T> {
    T data;
    AdjacentNode firstAdjacentNode;
    int inDegree;

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
        boolean isAdded = vertexes.get(from).addArch(to, weight);
        if (!isAdded)
            return;
        vertexes.get(to).inDegree++;
    }

    public List<Integer> topologicalSort(int... starts) {
        List<Integer> stack = new LinkedList<>();
        for (int start: starts)
            if (vertexes.get(start).inDegree == 0)
                stack.add(start);

        int size = vertexes.size();
        int[] inDegrees = new int[size];
        for (int i = 0; i < size; i++)
            inDegrees[i] = vertexes.get(i).inDegree;

        int top, index;
        List<Integer> result = new LinkedList<>();

        while (stack.size() > 0) {
            HeadNode headNode = vertexes.get(top = stack.remove(
                stack.size() - 1));
            result.add(top);

            for (AdjacentNode adjacentNode = headNode.firstAdjacentNode;
                    adjacentNode != null; adjacentNode = adjacentNode.next) {
                if (--inDegrees[index = adjacentNode.index] == 0)
                    stack.add(index);
            }
        }
        return result;
    }

    public List<Integer> DFS() {
        int size = vertexes.size();
        boolean[] visited = new boolean[size];
        for (int i = 0; i < size; i++)
            visited[i] = false;
        List<Integer> finished = new ArrayList<>();
        for (int i = 0; i < size; i++)
            if (!visited[i])
                DFS(i, visited, finished);
        return finished;
    }

    public void DFS(int index, boolean[] visited, List<Integer> finished) {
        int adjacentIndex;
        for (AdjacentNode adjacentNode = vertexes.get(index).firstAdjacentNode;
                adjacentNode != null; adjacentNode = adjacentNode.next) {
            if (visited[adjacentIndex = adjacentNode.index])
                continue;
            DFS(adjacentIndex, visited, finished);
        }

        if (!visited[index]) {
            visited[index] = true;
            finished.add(index);
        }
    }

    public void topologicalOrder(int[] ve, List<Integer> T, int... starts) {
        List<Integer> stack = new LinkedList<>();
        for (int start: starts)
            if (vertexes.get(start).inDegree == 0)
                stack.add(start);

        int size = vertexes.size();
        int[] inDegrees = new int[size];
        for (int i = 0; i < size; i++)
            inDegrees[i] = vertexes.get(i).inDegree;
        int top, index;

        while (stack.size() > 0) {
            HeadNode headNode = vertexes.get(top = stack.remove(
                stack.size() - 1));
            T.add(top);

            for (AdjacentNode adjacentNode = headNode.firstAdjacentNode;
                    adjacentNode != null; adjacentNode = adjacentNode.next) {
                if (--inDegrees[index = adjacentNode.index] == 0)
                    stack.add(index);
                int newE = ve[top] + adjacentNode.weight;
                if (newE > ve[index])
                    ve[index] = newE;
            }
        }
    }

    public void criticalPath(int start) {
        int size = vertexes.size();
        int[] ve = new int[size];
        List<Integer> T = new ArrayList<>();
        topologicalOrder(ve, T, start);

        int[] vl = new int[size];
        for (int i = 0; i < size; i++)
            vl[i] = -1;
        vl[size - 1] = ve[size - 1];

        int cursor = T.size() - 1;
        while (cursor >= 0) {
            int top = T.get(cursor--);
            for (AdjacentNode adjacentNode = vertexes.get(top).firstAdjacentNode;
                adjacentNode != null; adjacentNode = adjacentNode.next) {
                int newL = vl[adjacentNode.index] - adjacentNode.weight;
                if (vl[top] == -1 || newL < vl[top])
                    vl[top] = newL;
            }
        }

        // 求关键活动
        for (int index: T) {
            HeadNode headNode = vertexes.get(index);
            for (AdjacentNode adjacentNode = headNode.firstAdjacentNode;
                    adjacentNode != null; adjacentNode = adjacentNode.next) {
                int e = ve[index];
                int l = vl[adjacentNode.index] - adjacentNode.weight;
                if (e == l)
                    System.out.println("critical activity: " + 
                        index + " ---> " + adjacentNode.index);
            }
        }
    }
}

public class CriticalPath {
    public static void main(String[] args) {
        Network<Integer> network = new Network<>();

        /* 拓扑排序测试用例
        for (int i = 0; i <= 12; i++)
            network.addVertex(i);
        for (int[] arch:
            new int[][]{new int[]{0, 1}, new int[]{0, 5}, new int[]{0, 6},
                new int[]{2, 0}, new int[]{2, 3},
                new int[]{3, 5}, new int[]{5, 4}, new int[]{6, 4}, new int[]{6, 9},
                new int[]{7, 6}, new int[]{8, 7}, 
                new int[]{9, 10}, new int[]{9, 11}, new int[]{9, 12},
                new int[]{11, 12}
        })
        network.addArch(arch[0], arch[1], 0);

        List<Integer> topologicalSort = network.topologicalSort(8, 2);
        System.out.println(topologicalSort);
        topologicalSort = network.DFS();
        System.out.println(topologicalSort);
        */

        for (int i = 0; i <= 7; ++i)
            network.addVertex(i);
        for (int[] arch: new int[][]{
                new int[]{1, 2, 3}, new int[]{1, 3, 2}, new int[]{1, 4, 6},
                new int[]{2, 4, 2}, new int[]{2, 5, 4},
                new int[]{3, 4, 1}, new int[]{3, 6, 3},
                new int[]{4, 5, 1}, new int[]{5, 7, 3}, new int[]{6, 7, 4} 
        })
            network.addArch(arch[0], arch[1], arch[2]);
        network.criticalPath(1);
    }
}

