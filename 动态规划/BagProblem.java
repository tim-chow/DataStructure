import java.util.*;

public class BagProblem {
    private int[][] goods;
    private Map<String, int[][]> cache = new HashMap<>();

    public BagProblem(int[][] goods) {
        if (goods == null)
            throw new RuntimeException("goods == null");
        this.goods = goods;
    }

    public int[][] dp(int totalWeight) {
        if (totalWeight <= 0)
            throw new RuntimeException("totalWeight <= 0");
        return dp(totalWeight, 0, new int[0][0]);
    }

    private int[][] copyArray(int[][] origin, int expandSize) {
        int[][] newArray = new int[origin.length+expandSize][];
        for (int i=0; i<origin.length; i++) 
            newArray[i] = origin[i];
        return newArray;
    }

    private String generateKey(int totalWeight, int sn, int[][] chosen) {
        StringBuilder sb = new StringBuilder();
        sb.append(totalWeight);
        sb.append("|");
        sb.append(sn);
        sb.append("|");
        for (int[] one: chosen) {
            sb.append(one[0]);
            sb.append(",");
            sb.append(one[1]);
            sb.append("|");
        }
        return sb.toString();
    }

    private int[][] dp(int totalWeight, int sn, int[][] chosen) {
        String key = generateKey(totalWeight, sn, chosen);
        if (cache.containsKey(key))
            return cache.get(key);

        int[][] result;
        if (totalWeight == 0 || sn >= goods.length)
            return chosen;

        if (goods[sn][0] > totalWeight) {
            result = dp(totalWeight, sn+1, chosen);
            cache.put(key, result);
            return result;
        }

        int[][] chosen1 = copyArray(chosen, 1);
        chosen1[chosen1.length-1] = goods[sn];
        chosen1 = dp(totalWeight - goods[sn][0], sn+1, chosen1);
        int[][] chosen2 = dp(totalWeight, sn+1, chosen);

        int weight1 = 0, weight2 = 0;
        for (int[] one: chosen1)
            weight1 += one[1];
        for (int[] one: chosen2)
            weight2 += one[1];

        if (weight1 > weight2)
            result = chosen1;
        else
            result = chosen2;

        cache.put(key, result);
        return result;
    }

    private Map<String, int[][]> getCache() {
        return cache;
    }

    public static void main(String[] args) {
        int[][] goods = new int[][]{
            new int[]{3, 4},
            new int[]{2, 4},
            new int[]{5, 8},
            new int[]{7, 10}
        };

        BagProblem bag = new BagProblem(goods);
        int[][] result = bag.dp(12);
        for (int[] one: result)
            System.out.println("(" + one[0] + ", " + one[1] + ")");
        System.out.println(bag.getCache());
    }
}

