# coding: utf8

class BagProblem(object):
    def __init__(self):
        self._cache = {}

    def cache(self, f):
        def _inner(sn, current_weight, chosen):
            key = (sn, current_weight)
            if key in self._cache:
                return self._cache[key]
            result = f(sn, current_weight, chosen)
            self._cache[key] = result
            return result
        return _inner

    def calc(self, goods, totoal_weight):
        @self.cache
        def _calc(sn, current_weight, chosen):
            if current_weight == totoal_weight or sn == len(goods) - 1:
                return current_weight, chosen[:]
            # 装不进去，则不装
            if current_weight + goods[sn][0] > totoal_weight:
                return _calc(sn+1, current_weight, chosen[:])
            # + 能装进去，分两种情况：
            # 1，不选择sn
            totoal_weight1, chosen1 = _calc(sn+1, current_weight, chosen[:])
            # 2，选择sn
            totoal_weight2, chosen2 = _calc(sn+1, current_weight+goods[sn][0], chosen+[goods[sn]])
            if sum([item[1] for item in chosen1]) > sum([item[1] for item in chosen2]):
                return totoal_weight1, chosen1
            return totoal_weight2, chosen2
        return _calc(0, 0, [])

if __name__ == "__main__":
    bp = BagProblem()
    goods = [(3, 4), (2, 4), (5, 8), (7, 10), (3, 3), (8, 11)]
    totoal_weight = 15
    print(bp.calc(goods, totoal_weight))
