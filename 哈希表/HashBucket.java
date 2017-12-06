@SuppressWarnings("unchecked")
public class HashBucket<K, V> {
    public static class Entry<K, V> {
        private K key;
        private V value;

        Entry(K key, V value) {
            this.key = key;
            this.value = value;
        }

        public K getKey() {
            return key;
        }

        public V getValue() {
            return value;
        }

        private void setValue(V value) {
            this.value = value;
        }
    }

    private int bucketSize;
    private int bucketCount;
    private Object[] underFlying;

    public HashBucket(int bucketSize, int bucketCount) {
        this.bucketSize = bucketSize;
        this.bucketCount = bucketCount;
        underFlying = new Object[bucketSize * bucketCount];
    }

    public HashBucket() {
        this(4, 100);
    }

    private int[] getBucket(K key) {
        int bucketNo = key != null ? key.hashCode() % bucketCount: 0;
        int from = bucketNo * bucketSize;
        int to = from + bucketSize - 1;
        return new int[]{from, to};
    }

    public int put(K key, V value) {
        int[] bucket = getBucket(key);
        for (int index = bucket[0]; index <= bucket[1]; index++) {
            if (underFlying[index] == null) {
                underFlying[index] = new Entry<K, V>(key, value);
                return 0; // put successfully
            }
            Entry<K, V> entry = (Entry<K, V>) underFlying[index];
            if (entry.getKey().equals(key)) {
                entry.setValue(value);
                return 1; // already in hash table
            }
        }
        return 2; //no space
    }

    public V get(K key) {
        int[] bucket = getBucket(key);
        int index = getKey(key, bucket[0], bucket[1]);
        if (index == -1)
            return null;
        return ((Entry<K, V>) underFlying[index]).getValue();
    }

    public boolean delete(K key) {
        int[] bucket = getBucket(key);
        int index = getKey(key, bucket[0], bucket[1]);
        if (index == -1)
            return false;
        underFlying[index] = null;
        for (int i = index; i < bucket[1]; i++) {
            underFlying[i] = underFlying[i + 1];
            underFlying[i + 1] = null;
        }
        return true;
    }

    private int getKey(K key, int from, int to) {
        for (int index = from; index <= to; index++) {
            if (underFlying[index] == null)
                break;
            if (((Entry<K, V>) underFlying[index]).getKey().equals(key))
                return index;
        }
        return -1;
    }

    public static void main(String[] args) {
        HashBucket<Integer, Integer> hashBucket =
                new HashBucket<Integer, Integer>(2, 100);
        System.out.println(hashBucket.put(1, 1));
        System.out.println(hashBucket.put(101, 101));
        System.out.println(hashBucket.put(101, 1010));
        System.out.println(hashBucket.put(201, 201));
        System.out.println(hashBucket.put(202, 202));
        System.out.println(hashBucket.delete(1));
        System.out.println(hashBucket.get(101));
        System.out.println(hashBucket.put(201, 201));
    }
}