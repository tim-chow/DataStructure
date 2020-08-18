# coding: utf8


class Entry(object):
    """
    条目
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Node(object):
    """
    同义词子表的节点
    """
    def __init__(self, entry=None, next_node=None):
        self.entry = entry
        self.next_node = next_node


class HashTable(object):
    """
    基于除留余数和链地址法实现的哈希表
    """
    def __init__(self, initial_capacity=None, rehash_factor=None):
        """
        :param initial_capacity: 初始容量，默认值是 32
        :param rehash_factor: 扩容因子，默认值是 2
        """
        self._initial_capacity = initial_capacity or 32
        self._capacity = self._initial_capacity
        self._underlying_array = [None for _ in range(self._capacity)]
        self._item_count = 0
        self._rehash_factor = rehash_factor or 2

    def __setitem__(self, key, value):
        """
        插入条目
        """
        hash_value = hash(key) % self._capacity
        node = self._underlying_array[hash_value]
        if node is None:
            node = self._underlying_array[hash_value] = Node()
        while node.next_node is not None:
            # 如果 key 已经存在，更新 value
            if node.next_node.entry.key == key:
                node.next_node.entry.value = value
                return
            node = node.next_node
        node.next_node = Node(Entry(key, value))
        self._item_count = self._item_count + 1
        self.rehash()

    def __getitem__(self, key):
        """
        获取条目
        """
        hash_value = hash(key) % self._capacity
        node = self._underlying_array[hash_value]
        if node is None:
            raise KeyError()
        node = node.next_node
        while node is not None:
            if node.entry.key == key:
                return node.entry.value
            node = node.next_node
        raise KeyError()

    def __delitem__(self, key):
        """
        删除条目
        """
        hash_value = hash(key) % self._capacity
        node = self._underlying_array[hash_value]
        if node is None:
            raise KeyError()
        while node.next_node is not None:
            if node.next_node.entry.key == key:
                node.next_node = node.next_node.next_node
                self._item_count = self._item_count - 1
                break
            node = node.next_node
        else:
            raise KeyError()

    def rehash(self):
        """
        扩容
        """
        if (self._item_count + 0.0) / self._capacity <= self._rehash_factor:
            return

        # 申请新空间
        self._capacity = self._capacity + self._initial_capacity
        new_underlying_array = [None for _ in range(self._capacity)]

        # 重新映射
        for node in self._underlying_array:
            if node is None:
                continue
            temp = node.next_node
            while temp is not None:
                # 映射到新的存储空间
                hash_value = hash(temp.entry.key) % self._capacity
                head = new_underlying_array[hash_value]
                if head is None:
                    head = new_underlying_array[hash_value] = Node()
                while head.next_node is not None:
                    head = head.next_node
                head.next_node = Node(temp.entry)
                temp = temp.next_node
        self._underlying_array = new_underlying_array

    def __len__(self):
        return self._item_count


if __name__ == "__main__":
    import unittest


    class HashTableTest(unittest.TestCase):
        def testSetItem(self):
            hash_table = HashTable(initial_capacity=32)
            # 测试冲突
            hash_table[1] = 1
            hash_table[33] = 33
            self.assertEqual(hash_table[1], 1)
            self.assertEqual(hash_table[33], 33)
            # 测试 key 重复
            hash_table[33] = 34
            self.assertEqual(hash_table[33], 34)

        def testRehash(self):
            hash_table = HashTable(initial_capacity=2, rehash_factor=2)
            keys = list(range(1, 6))
            # 插入新条目，触发 rehash
            for key in keys:
                hash_table[key] = key
                self.assertEqual(hash_table[key], key)
            item_count = len(hash_table)
            self.assertEqual(item_count, len(keys))

            # 测试 rehash 后，是否出现错误
            for key in keys:
                self.assertEqual(hash_table[key], key)
            self.assertEqual(len(hash_table), len(keys))

            # 在 rehash 之后，插入一个新条目
            new_key = keys[-1] + 1
            hash_table[new_key] = new_key
            self.assertEqual(hash_table[new_key], new_key)
            self.assertEqual(len(hash_table), item_count + 1)

        def testDelItem(self):
            import random

            hash_table = HashTable()
            keys = list(range(100))

            # 插入条目
            for key in keys:
                hash_table[key] = key

            # 逐个删除
            random.shuffle(keys)
            item_count = len(hash_table)
            self.assertEqual(item_count, len(keys))
            for key in keys:
                self.assertEqual(hash_table[key], key)
                del hash_table[key]
                self.assertRaises(KeyError, hash_table.__getitem__, key)
                item_count = item_count - 1
                self.assertEqual(len(hash_table), item_count)

    unittest.main()
