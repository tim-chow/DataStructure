#coding: utf8

class BagProblem:
    def __init__(self, goods):
        self._goods = goods
        self._cache = {}

    def dp(self, total_weight):
        return self._dp(total_weight, 0, tuple())

    def _dp(self, total_weight, sn, chosen):
        # 如果该子问题已经求解过，则直接从缓存中获取结果，
        # + 以减少重复计算
        if (total_weight, sn, chosen) in self._cache:
            return self._cache[key]

        goods = self._goods
        # 结束状态是 对最后一个物品作出了决策，或者
        # + 背包已经装满
        if sn >= len(goods) or total_weight == 0:
            return chosen

        # 所有可能是局部解是：
        # + 1，第sn个物品无法装入背包
        if goods[sn][0] > total_weight:
            result = self._dp(total_weight, sn+1, chosen)
            self._cache[(total_weight, sn, chosen)] = result
            return result

        # + 2，选择第sn个物品
        total_weight_1 = total_weight - goods[sn][0]
        chosen_1 = self._dp(total_weight - goods[sn][0], 
            sn+1, chosen + (goods[sn], ))
        # + 3，不选择第sn个物品
        chosen_2 = self._dp(total_weight, sn+1, chosen)

        # 保留可能到达最优解的局部解
        if sum(good[1] for good in chosen_1) > \
            sum(good[1] for good in chosen_2):
            result = chosen_1
        else:
            result = chosen_2

        # 将解过的子问题缓存起来
        self._cache[(total_weight, sn, chosen)] = result
        return result

if __name__ == "__main__":
    goods = [(3, 4), (2, 4), (5, 8), (7, 10)]
    bag = BagProblem(goods)
    print bag.dp(11)

