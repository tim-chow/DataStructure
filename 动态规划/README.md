### 动态规划

动态规划用于求解<strong>多阶段决策问题</strong>的<strong>最优解</strong>。

其基本思想和分治法类似<sup>注释1</sup>，都是先将待求解问题划分成若干个子问题（<strong><em>阶段</em></strong>），然后从<strong>初始状态</strong>开始，顺序求解子问题，每个子问题的决策都依赖当前状态，并且在作出决策之后，又会引起状态的转移。一个<strong>决策序列</strong>就是在状态的变化中产生出来的。<strong>在求解任一子问题的时候，需要列出所有可能的局部解，然后通过决策保留那些有可能到达全局最优解的局部解，丢弃其它局部解</strong>。按此方式，依次解决各个子问题，一直到达<strong>结束状态</strong>。

能够使用动态规划求解的问题，一般具有以下三个性质：<br />
<li><strong>最优化原理</strong></br><strong style="color">无论过去的状态和决策如何，对于过去的决策，所形成的状态而言，余下的决策必须是最优决策</strong></li>
<li><strong>无后效性</strong></br>某个阶段的状态一旦确定，就不再受以后的决策的影响</li>
<li><strong>有重叠子问题</strong><sup>注释2</sup></br>子问题之间不互相独立，某个子问题可能被多次使用到，<strong>因此可以将解过的子问题缓存起来，以减少重复计算，这也是动态规划的优势</strong></li>

使用动态规划解决问题的一般步骤是：</br>
<li><strong>划分阶段</strong></br>根据问题的时间或空间特征将问题划分成若干个阶段，<strong style="color:red">值得注意的是：划分后的阶段一定是可排序的或有序的，否则无法使用动态规划求解</strong></li>
<li><strong>确定状态和状态变量</strong></br>将问题发展到各个阶段时所处的实际情况用状态表示出来，<strong style="color:red">状态的选择要具有无后效性</strong></li>
<li><strong>确定决策和状态转移方程</strong></br>如前所述，每次决策既受限于当前状态，又会引起状态转移。<strong style="color:red">状态转移方程就是从前一阶段到后一阶段的递推关系</strong>。比如对于 01 背包问题，状态转移方程是：</br><code>f(i, j) = max{f(i-1, j), f(i-1, j-w[i]) + c[i]}</code>（其中 f(i, j) 表示将前 i 个物品放进总重量为 j 的背包中所能获得的最大价值）</li>
<li><strong>寻找边界条件</strong></br>边界条件就是<strong>结束状态</strong></li>

---

### 注释

* 注释1：  
动态规划和分治法的最大差别是：动态规划划分后得到的子问题不互相独立

* 注释2：  
<em>有重叠子问题</em>并不是适用动态规划的必要条件

---

### Read Also

* [https://zhuanlan.zhihu.com/p/93857890](https://zhuanlan.zhihu.com/p/93857890)

