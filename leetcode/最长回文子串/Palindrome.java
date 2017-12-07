public class Palindrome {
    public static int[] maxLengthPalindrome(String string) {
        int length = string.length();
        int[][] P = new int[length][length];
        for (int i = 0; i < length; i++)
            for (int j = 0; j < length; j++)
                P[i][j] = -1;

        for (int i = 0; i < length; i++)
            for (int j = length - 1; j > i; j--)
                maxLengthPalindrome(string, P, i, j);

        int[] result = new int[]{-1, -1};
        for (int i = 0; i < length - 1; i++)
            for (int j = i + 1; j < length; j++) {
                if (P[i][j] == 1 && (result[0] == -1 || j - i > result[1] - result[0])) {
                    result[0] = i;
                    result[1] = j;
                }
            }
        return result;
    }

    private static int maxLengthPalindrome(String string, int[][] P, int i, int j) {
        if (i > j)
            return P[i][j] = 0;

        if (P[i][j] != -1)
            return P[i][j];

        if (i == j)
            return P[i][j] = 1;

        if (string.charAt(i) == string.charAt(j)) {
            if (j - i == 1)
                return P[i][j] = 1;
            return P[i][j] = maxLengthPalindrome(string, P, i + 1, j - 1);
        }
        return P[i][j] = 0;
    }

    public static void main(String[] args) {
        int[] result = maxLengthPalindrome("abc8dcbeeb8");
        System.out.println(result[0] + " ---> " + result[1]);
    }
}
