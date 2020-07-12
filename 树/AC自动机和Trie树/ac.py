# coding: utf8


class Node(object):
    def __init__(self, char):
        self.char = char
        self.children = {}
        self.fail = None
        self.end = False


class AC(object):
    def __init__(self, *patterns):
        self._patterns = patterns
        self._root, self._output = AC.create_trie_tree(patterns)
        AC.set_fail(self._root)

    @staticmethod
    def create_trie_tree(patterns):
        root = Node(None)
        output = {}
        for pattern in patterns:
            if not pattern:
                continue
            temp = root
            for char in pattern:
                if char not in temp.children:
                    temp.children[char] = Node(char)
                temp = temp.children[char]
            else:
                temp.end = True
                output[temp] = pattern
        return root, output

    @staticmethod
    def set_fail(root):
        # 根节点的 fail 指针是 None
        # 根节点的孩子节点的 fail 指针指向根节点
        queue = []
        for child in root.children.values():
            child.fail = root
            queue.append(child)

        while queue:
            p = queue.pop(0)
            for char, n in sorted(p.children.items(), key=lambda c: c):
                queue.append(n)

                f = p.fail
                while f is not None:
                    if char in f.children:
                        n.fail = f.children[char]
                        break
                    f = f.fail

    def _generate_output(self, p):
        matches = []
        while p is not None:
            if p.end:
                matches.append(self._output[p])
            p = p.fail
        return matches

    def find(self, main_string):
        print main_string
        results = {}
        node = self._root
        for ind, char in enumerate(main_string):
            while node is not None:
                if char in node.children:
                    node = node.children[char]
                    if node.end:
                        for pattern in self._generate_output(node):
                            results.setdefault(ind-len(pattern)+1, []) \
                                .append(pattern)
                    break
                node = node.fail
            else:
                node = self._root
        return results


if __name__ == "__main__":
    ac = AC("ashe", "sha", "he", "ash", "she")
    print(ac.find("she11ashe22shahe33"))
