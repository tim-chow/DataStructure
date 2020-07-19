# coding: utf8


class Node(object):
    def __init__(self, keyword, left=None, right=None):
        self.keyword = keyword
        self.left = left
        self.right = right


class NodeFactory(object):
    nodes = {}

    @classmethod
    def get_node(cls, keyword):
        if keyword not in cls.nodes:
            cls.nodes[keyword] = Node(keyword)
        return cls.nodes[keyword]


def find_pos(sequence, target):
    for pos, element in enumerate(sequence):
        if target == element:
            return pos
    return -1


def generate_tree(preorder, inorder, postorder):
    if len(preorder) != len(inorder) or len(inorder) != len(postorder):
        raise RuntimeError("invalid sequence")

    if len(preorder) == 0:
        return None

    if len(preorder) == 1:
        return NodeFactory.get_node(preorder[0])

    if preorder[0] != postorder[-1]:
        raise RuntimeError("invalid sequence")

    # 先序序列的第一个节点和后序序列的最后一个节点是根节点
    root = NodeFactory.get_node(preorder[0])

    # 如果根节点是中序序列的第一个节点，说明根节点的左子树为空，先序序列的第二个节点是根节点的右孩子
    if preorder[0] == inorder[0]:
        root.left = None
        root.right = NodeFactory.get_node(preorder[1])
    # 如果根节点是中序序列的最后一个节点，说明根节点的右子树为空，先序序列的第二个节点是根节点的左孩子
    elif preorder[0] == inorder[-1]:
        root.left = NodeFactory.get_node(preorder[1])
        root.right = None
    # 否则，根节点的左右子树都不为空
    else:
        # 先序序列的第二个节点是根节点的左孩子
        root.left = NodeFactory.get_node(preorder[1])
        # 后序序列的倒数第二个节点是根节点的右孩子
        root.right = NodeFactory.get_node(postorder[-2])

    if root.left is None:
        right_preorder = preorder[1:]
        right_inorder = inorder[1:]
        right_postorder = postorder[:-1]
        generate_tree(right_preorder, right_inorder, right_postorder)
    elif root.right is None:
        left_preorder = preorder[1:]
        left_inorder = inorder[:-1]
        left_postorder = postorder[:-1]
        generate_tree(left_preorder, left_inorder, left_postorder)
    else:
        pos = find_pos(preorder, root.right.keyword)
        if pos == -1:
            raise RuntimeError("invalid sequence")
        left_preorder = preorder[1:pos]
        right_preorder = preorder[pos:]

        pos = find_pos(inorder, root.keyword)
        if pos == -1:
            raise RuntimeError("invalid sequence")
        left_inorder = inorder[:pos]
        right_inorder = inorder[pos+1:]

        pos = find_pos(postorder, root.left.keyword)
        if pos == -1:
            raise RuntimeError("invalid sequence")
        left_postorder = postorder[:pos+1]
        right_postorder = postorder[pos+1:-1]

        generate_tree(left_preorder, left_inorder, left_postorder)

        generate_tree(right_preorder, right_inorder, right_postorder)

    return root


def test():
    def preorder_traverse(p):
        keywords = []
        if p is None:
            return keywords
        keywords.append(p.keyword)
        keywords.extend(preorder_traverse(p.left))
        keywords.extend(preorder_traverse(p.right))
        return keywords

    def inorder_traverse(p):
        keywords = []
        if p is None:
            return keywords
        keywords.extend(inorder_traverse(p.left))
        keywords.append(p.keyword)
        keywords.extend(inorder_traverse(p.right))
        return keywords

    def postorder_traverse(p):
        keywords = []
        if p is None:
            return keywords
        keywords.extend(postorder_traverse(p.left))
        keywords.extend(postorder_traverse(p.right))
        keywords.append(p.keyword)
        return keywords

    nodes = [Node(ind) for ind in range(7)]
    nodes[0].left = nodes[1]
    nodes[0].right = nodes[2]
    nodes[1].left = nodes[3]
    nodes[1].right = nodes[4]
    nodes[2].left = nodes[5]
    nodes[3].right = nodes[6]

    root = nodes[0]
    del nodes

    preorder = preorder_traverse(root)
    inorder = inorder_traverse(root)
    postorder = postorder_traverse(root)

    generated_root = generate_tree(preorder, inorder, postorder)

    assert preorder == preorder_traverse(generated_root)
    assert inorder == inorder_traverse(generated_root)
    assert postorder == postorder_traverse(generated_root)


if __name__ == "__main__":
    test()
