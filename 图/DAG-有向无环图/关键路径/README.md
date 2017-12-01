### 基本概念
AOE网（Activity On Edge Network）是：
<ul>
<li>使用弧表示活动，</li>
<li>权值表示活动的持续时间，</li>
<li>顶点表示事件</li>
</ul>
的有向图。  

需要注意的是：  
<ul>
<li><strong>只有进入到某个顶点的活动都结束，该顶点所代表的事件才会发生</strong></li>
<li><strong>当某个事件发生时，其后的活动才可以开始</strong></li>
</ul>
在AOE网中，只有一个入度为0的顶点，称之为源点；只有一个出度为0的点，称之为汇点。它们分别代表工程的开始和结束。  
从源点到顶点v<sub>i</sub>的最长路径，就是v<sub>i</sub>所代表的事件的<strong>最早发生时间</strong>，记作ve(i)，该时间决定了 所有以该顶点为弧尾的弧所代表的活动的 最早发生时间，将a<sub>i</sub>所代表的活动的最早发生时间记作e(i)。  
同时每个活动（或事件）还可以有一个<strong>最迟发生时间</strong>，记作l(i)（或vl(i)）。该时间表示<strong>在不影响工程进度的情况，活动（或事件）最迟必须开始的时间</strong>。
<ul>
<li>将l(i) = e(i)的活动叫做<strong>关键活动</strong></li>
<li>将从源点到汇点的最长路径叫做<strong>关键路径</strong>，显然关键路径上的活动都是关键活动</li>
</ul>
<strong>综上，寻找关键路径，本质就是寻找所有的关键活动。而辨别关键活动，就是寻找l(i) = e(i)的活动。</strong>  
假设弧&lt;j, k&gt;表示活动a<sub>i</sub>，a<sub>i</sub>的持续时间用duration(&lt;j, k&gt;)表示，那么：  

* e(i) = ve(j)
* l(i) = vl(k) - duration(&lt;j, k&gt;)

最终，将寻找关键路径转换成了<strong>寻找每个事件的最早发生时间和最迟发生时间</strong>。

更多详细内容，请移步参考文档。

---

### 参考文档  
给大家推荐一篇关于AOE网的比较好的文章：[https://www.cnblogs.com/william-lee/p/5043753.html](https://www.cnblogs.com/william-lee/p/5043753.html)。  
代码中，使用的测试用例，就是这篇文章中的测试用例。  