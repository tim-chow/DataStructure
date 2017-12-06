public class SequentialStack<T> {
    public static final int DEFAULT_CAPACITY = 100;
    private T[] baseArray = (T[]) new Object[0];
    private int base = 0;
    private int top = base;
    private int capacity;

    public SequentialStack() {
        this(DEFAULT_CAPACITY);
    }

    public SequentialStack(int capacity) {
        this.capacity = capacity;
        ensureCapacity(capacity);
    }

    public boolean isEmpty() {
        return top - base == 0;
    }

    public int size() {
        return top - base;
    }

    private void ensureCapacity(int newSize) {
        if (newSize < top - base)
            return;

        T[] newArray = (T[]) new Object[newSize];
        for (int i = base; i < top; ++i)
            newArray[i - base] = baseArray[i];
        top = top - base;
        base = 0;
        baseArray = newArray;
    }

    public void trimToSize() {
        ensureCapacity(size());
    }

    public void clear() {
        top = base;
        ensureCapacity(capacity);
    }

    public void push(T data) {
        if (top == baseArray.length)
            ensureCapacity(baseArray.length + capacity);
        baseArray[top++] = data;
    }

    public T pop() {
        if (isEmpty())
            throw new RuntimeException("empty stack");
        return baseArray[--top];
    }

    public T getTop() {
        if (isEmpty())
            throw new RuntimeException("empty stack");
        return baseArray[top - 1];
    }

    public void println() {
        for (int i = base; i < top; ++i) 
            System.out.println(baseArray[i]);
    }

    public static int[] conversion(int n, int base) {
        SequentialStack<Integer> stack = new SequentialStack<Integer>();
        while (n != 0) {
            stack.push(n % base);
            n = n / base;
        }
        int size = stack.size();
        int[] result = new int[size];
        for (int i = 0; i < size; ++i)
            result[i] = stack.pop();
        return result;
    }

    public static boolean isPair(int[] array) {
        SequentialStack<Integer> stack = new SequentialStack<Integer>();
        for (int ele: array) {
            if (ele == 0)
                continue;
            if (ele < 0)
                stack.push(ele);
            else {
                if (stack.size() == 0 || (stack.pop() + ele != 0))
                    return false;
            }
        }
        return stack.size() == 0;
    }
}

