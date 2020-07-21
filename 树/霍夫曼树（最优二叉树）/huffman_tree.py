# coding: utf8

import heapq


class Node(object):
    """
    霍夫曼树的节点
    """
    def __init__(self, char, weight, left=None, right=None):
        self.char = char
        self.weight = weight
        self.left = left
        self.right = right

    def __cmp__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("instance of %s expected" % self.__class__.__name__)
        if other.weight == self.weight:
            return 0
        if other.weight > self.weight:
            return -1
        return 1

    def __str__(self):
        return "%s{char=%s, weight=%d, left=%s, right=%s}" % (
            self.__class__.__name__,
            self.char,
            self.weight,
            self.left and self.left.char,
            self.right and self.right.char
        )


class HuffmanTree(object):
    """
    霍夫曼树实现
    """
    def __init__(self, chars):
        root = self.create(chars)
        self._encode_map, self._decode_map = self.generate_code_map(root)

    @staticmethod
    def create(chars):
        if len(chars) == 0:
            return

        nodes = []
        # 构造 n 棵只有根节点的二叉树
        for char, weight in chars:
            heapq.heappush(nodes, Node(char, weight))

        # 重复下面的步骤，直到森林中只有一棵树
        while len(nodes) > 1:
            # 从森林中选出根节点权值最小的两棵树
            left = heapq.heappop(nodes)
            right = heapq.heappop(nodes)
            # 构造一棵新树，并把上面的两棵树作为新树的子树，新树的根节点的权值是两者的权值之和
            node = Node(None, left.weight + right.weight, left, right)
            # 将新树放进森林
            heapq.heappush(nodes, node)

        return nodes[0]

    @staticmethod
    def generate_code_map(root):
        encode_map = {}
        decode_map = {}

        if root is None:
            return encode_map, decode_map

        temp_map = {root: []}
        queue = [root]
        while queue:
            node = queue.pop()
            # 将从根节点到叶子节点的路径上的二进制位作为叶子节点的编码
            if node.left is None and node.right is None:
                code = "".join(temp_map[node])
                encode_map[node.char] = code
                decode_map[code] = node.char
                continue

            node_code = temp_map[node]
            # 所有左分支都表示 0
            if node.left is not None:
                temp_map[node.left] = node_code + ['0']
                queue.append(node.left)

            # 所有右分支都表示 1
            if node.right is not None:
                temp_map[node.right] = node_code + ['1']
                queue.append(node.right)

        return encode_map, decode_map

    def encode(self, string):
        """
        编码
        """
        result = []
        for char in string:
            if char not in self._encode_map:
                raise ValueError("unknown char %s" % char)
            result.append(self._encode_map[char])
        return "".join(result)

    def decode(self, encoded_string):
        start = 0
        end = start + 1
        result = []
        while end <= len(encoded_string):
            sub_string = encoded_string[start:end]
            if sub_string not in self._decode_map:
                end = end + 1
                continue
            result.append(self._decode_map[sub_string])
            start = end
            end = end + 1
        return "".join(result)


def test():
    chars = [("A", 5), ("B", 24), ("C", 7), ("D", 17),
             ("E", 34), ("F", 5), ("G", 13)]
    huffman_tree = HuffmanTree(chars)
    string = "AFGECBDAAAFFF"
    assert string == huffman_tree.decode(huffman_tree.encode(string))


if __name__ == "__main__":
    test()
