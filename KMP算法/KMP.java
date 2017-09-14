import java.util.*;

public class KMP {
    public static int[] getNext(String mainString) {
        int length = mainString.length();
        int[] next = new int[length];

        for (int ind = 1; ind < length; ++ind) {
            for (int j = ind; j > 0;) {
                j = next[j - 1];
                if (mainString.charAt(j) == mainString.charAt(ind)) {
                    next[ind] = j + 1;
                    break;
                }
            }
        }
        return next;
    }

    public static int find(String mainString, String patternString) {
        int[] next = getNext(patternString);

        int i = 0, j = 0;
        while (i <= mainString.length() - patternString.length()) {
            if (mainString.charAt(i) != patternString.charAt(j)) {
                // backtrace
                if (j == 0)
                    i++;
                else
                    j = next[j - 1];
                continue;
            }
            i++;
            j++;
            if (j == patternString.length())
                return i - j;
        }
        return -1;
    }

    public static void main(String[] args) {
        System.out.println(find("what the fuck", "e "));
        System.out.println(find("what the fuck", "the1"));
    }
}

