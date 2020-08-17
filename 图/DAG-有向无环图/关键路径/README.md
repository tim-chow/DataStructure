### 基本概念

AOE 网（Activity On Edge Network）是使用：

<ul>
  <li>弧表示活动</li>
  <li>权值表示活动的持续时间</li>
  <li>顶点表示事件</li>
</ul>
的有向图。

在 AOE 网中，有如下两条原则：

<ul>
  <li><strong>只有进入到某个顶点的所有活动都结束，该顶点所代表的事件才会发生</strong></li>
  <li><strong>当某个事件发生时，其后的活动才可以开始</strong></li>
</ul>

在 AOE 网中，只有一个入度为 0 的顶点，称之为源点；只有一个出度为 0 的点，称之为汇点。它们分别代表工程的开始和结束。

从源点到顶点 v<sub>i</sub> 的最长路径是 v<sub>i</sub> 所代表的事件的<strong>最早发生时间</strong>，记作 ve(i)，该时间决定了所有以该顶点为弧尾的弧所代表的活动的最早发生时间。将 a<sub>i</sub> 所代表的活动的最早发生时间记作e(i)。

每个活动和事件还有一个<strong>最迟发生时间</strong>，分别记作 l(i) 和 vl(i)，该时间表示<strong>为了不影响工程进度，活动和事件最迟必须开始的时间</strong>。

<ul>
  <li>将 l(i) = e(i) 的活动叫<strong>关键活动</strong></li>
  <li>将从源点到汇点的最长路径叫<strong>关键路径</strong>，显然关键路径上的活动都是关键活动</li>
</ul>

<strong>综上所述，寻找关键路径本质就是寻找所有关键活动。而关键活动就是 l(i) = e(i) 的活动。</strong>

设弧 &lt;j, k&gt; 表示活动 a<sub>i</sub>，a<sub>i</sub> 的持续时间为 duration(&lt;j, k&gt;)，那么：

* e(i) = ve(j)
* l(i) = vl(k) - duration(&lt;j, k&gt;)

最终将寻找关键路径转换成了<strong>寻找每个事件的最早发生时间和最迟发生时间</strong>。

---

### 参考文档

* [https://www.cnblogs.com/william-lee/p/5043753.html](https://www.cnblogs.com/william-lee/p/5043753.html)。
