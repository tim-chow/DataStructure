import java.util.*;

class HeapSort {
    public static <T extends Comparable> void adjust(List<T> array, int index, int end) {
        int leftChildIndex, rightChildIndex;

        while ((leftChildIndex = 2 * index + 1) < end) {
            T element = array.get(index);
            T leftChild = array.get(leftChildIndex);

            rightChildIndex = 2 * index + 2;
            if (rightChildIndex >= end) {
                if (leftChild.compareTo(element) == -1) {
                    array.set(index, leftChild);
                    array.set(leftChildIndex, element);
                }
                break;
            }

            T rightChild = array.get(rightChildIndex);

            if (element.compareTo(leftChild) <= 0 &&
                    element.compareTo(rightChild) <= 0)
                break;

            if (leftChild.compareTo(rightChild) == -1) {
                array.set(leftChildIndex, element);
                array.set(index, leftChild);
                index = leftChildIndex;
                continue;
            } 

            array.set(rightChildIndex, element);
            array.set(index, rightChild);
            index = rightChildIndex;
        }
    }

    public static <T extends Comparable> void heapify(List<T> array) {
        for (int index=array.size()/2; index>=0; index--)
            adjust(array, index, array.size());
    }

    public static <T extends Comparable> void heapSort(List<T> array) {
        heapify(array);

        int end = array.size();
        T temp;
        while (end > 1) {
            temp = array.get(0);
            end--;
            array.set(0, array.get(end));
            array.set(end, temp);
            adjust(array, 0, end);
        }
    }

    public static <T extends Comparable> void topK(List<T> array, int k) {
        for (int index = k / 2; index >= 0; index--) 
            adjust(array, index, k);

        for (int index = k; index < array.size(); index++) {
            if (array.get(index).compareTo(array.get(0)) == 1) {
                T temp = array.get(0);
                array.set(0, array.get(index));
                array.set(index, temp);
                adjust(array, 0, k);
            }
        }
    }

    public static void main(String[] args) {
        List<Integer> array = Arrays.asList(new Integer[]{3, 1, 2, 4, 6, 5, 10, 7, 9, -1, 30});
        //heapify(array);
        heapSort(array);
        //topK(array, 3);
        System.out.println(array);
    }
}

