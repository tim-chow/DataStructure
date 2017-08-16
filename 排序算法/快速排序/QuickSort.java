import java.util.*;

class QuickSort {
    public static <T extends Comparable> void sort(
        List<T> array, int start, int end) {
        if (start >= end)
            return;

        T pivot = array.get(start);
        int pos = start;
        for (int ind=start+1; ind<=end; ind++) {
            if (array.get(ind).compareTo(pivot) > 0)
                continue;
            array.set(pos, array.get(ind));
            for (int ind1=ind; ind1>=pos+2; ind1--)
                array.set(ind1, array.get(ind1-1));
            array.set(++pos, pivot);
        }

        sort(array, start, pos-1);
        sort(array, pos+1, end);
    }
    
    public static void main(String[] args) {
        List<Integer> integers = new ArrayList<>();
        integers.add(5);
        integers.add(3);
        integers.add(2);
        integers.add(9);
        integers.add(7);
        integers.add(0);
        integers.add(1);
        sort(integers, 0, integers.size() - 1);
        System.out.println(integers);
    }
}

