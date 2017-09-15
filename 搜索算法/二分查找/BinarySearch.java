import java.util.*;

public class BinarySearch {
    public static <T extends Comparable> int[]
            binarySearch(List<T> array, T target) {
        if (array == null || target == null)
            throw new RuntimeException(
                "array == null || target == null");

        int low = 0, high = array.size() - 1;
        int[] result = new int[2];
        while (low <= high) {
            int middle = (low + high) / 2;
            if (array.get(middle).compareTo(target) == 0) {
                result[0] = result[1] = middle;
                return result;
            }

            if (array.get(middle).compareTo(target) == 1) {
                if (middle == low ||
                        array.get(middle-1).compareTo(target) == -1) {
                    result[0] = middle - 1;
                    result[1] = middle;
                    return result;
                }
                high = middle - 1; 
                continue;
            }

            if (middle == array.size() - 1 ||
                    array.get(middle+1).compareTo(target) == 1) {
                result[0] = middle; result[1] = middle + 1;
                return result;
            }
            low = middle + 1;
        }

        // unreachable
        return result;
    }

    public static void main(String[] args) {
        List<Integer> array = Arrays.asList(new Integer[]{1, 2, 4, 7, 8, 9, 10});
        int[] result;
        result = binarySearch(array, 11);
        System.out.println(String.format(
            "(%d, %d)", result[0], result[1]));
        result = binarySearch(array, 9);
        System.out.println(String.format(
            "(%d, %d)", result[0], result[1]));
        result = binarySearch(array, 5);
        System.out.println(String.format(
            "(%d, %d)", result[0], result[1]));
        result = binarySearch(array, 1);
        System.out.println(String.format(
            "(%d, %d)", result[0], result[1]));
        result = binarySearch(array, 0);
        System.out.println(String.format(
            "(%d, %d)", result[0], result[1]));
    }
}

