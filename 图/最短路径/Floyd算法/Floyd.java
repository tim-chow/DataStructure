public class Floyd {
    public final static int INFINITY = Integer.MAX_VALUE / 2; //防止溢出

    public static int floyd(int[] vertexes, int[][] arches,
            int i, int j, int k, int[][] D, int[][] P) {
        if (k == 0)
            return arches[i][j];
        if (i == j)
            return D[i][j] = 0;
        if (D[i][j] != INFINITY)
            return D[i][j];

        // 选择k进行中转
        int lengthK = floyd(vertexes, arches, i, k, k - 1, D, P) +
            floyd(vertexes, arches, k, j, k - 1, D, P);
        // 不选择k进行中转
        int lengthWithoutK = floyd(vertexes, arches, i, j, k - 1, D, P);
        D[i][j] = lengthWithoutK;
        if (lengthK < lengthWithoutK) {
            D[i][j] = lengthK;
            P[i][j] = k;
        }
        return D[i][j];
    }

    public static void main(String[] args) {
        // 顶点0是用来占位的
        int[] vertexes = new int[]{0, 1, 2, 3, 4, 5};
        int[][] arches = new int[][]{
            //           0         1         2         3         4         5
            new int[]{INFINITY, INFINITY, INFINITY, INFINITY, INFINITY, INFINITY}, // 0
            new int[]{INFINITY, INFINITY,        3,        8, INFINITY,       -4}, // 1
            new int[]{INFINITY, INFINITY, INFINITY, INFINITY,        1,        7}, // 2
            new int[]{INFINITY, INFINITY,        4, INFINITY, INFINITY, INFINITY}, // 3
            new int[]{INFINITY,        2, INFINITY,       95, INFINITY, INFINITY}, // 4
            new int[]{INFINITY, INFINITY, INFINITY, INFINITY,        6, INFINITY}, // 5
        };
        int size = vertexes.length;

        int[][] D = new int[size][size]; // D[i][j]表示从顶点i 到 顶点j的最短路径
        int[][] P = new int[size][size]; // P[i][j]表示从顶点i 到 顶点j要经过的顶点
        for (int i = 0; i < size; i++)
            for (int j = 0; j < size; j++) {
                D[i][j] = INFINITY;
                P[i][j] = j;
            }

        for (int i = 1; i < size; i++)
            for (int j = 1; j < size; j++)
                floyd(vertexes, arches, i, j, size-1, D, P);

        for (int i = 1; i < size; i++)
            for (int j = 1; j < size; j++)
                System.out.println(i + " ---> " + j + " = "
                    + D[i][j] + ", 经过" + P[i][j]);
    }
}

