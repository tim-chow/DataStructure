# coding: utf8


class BagProblem(object):
    def __init__(self):
        self._cache = {}

    def calc(self, goods, total_weight):
        def _calc(sequence_number, current_weight, chosen_goods):
            if current_weight == total_weight or sequence_number == len(goods):
                return current_weight, chosen_goods[:]

            # 装不进去
            if current_weight + goods[sequence_number][0] > total_weight:
                return _calc(sequence_number + 1, current_weight, chosen_goods[:])

            # + 能装进去，分两种情况：
            # 1，不选择 sequence_number
            total_weight1, chosen1 = _calc(sequence_number + 1, current_weight, chosen_goods[:])
            # 2，选择 sequence_number
            total_weight2, chosen2 = _calc(sequence_number + 1,
                                           current_weight + goods[sequence_number][0],
                                           chosen_goods + [goods[sequence_number]])
            if sum([v for _, v in chosen1]) > sum([v for _, v in chosen2]):
                return total_weight1, chosen1
            return total_weight2, chosen2
        return _calc(0, 0, [])


def test():
    bp = BagProblem()
    goods = [(3, 4), (2, 4), (5, 8), (7, 10), (3, 3), (8, 11)]
    print(goods)
    total_weight = 15
    print(bp.calc(goods, total_weight))


if __name__ == "__main__":
    test()
