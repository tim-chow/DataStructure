### 等价关系

设 R 是非空集合 S 上的二元关系，如果 R 是<strong>自反的</strong>、<strong>对称的</strong>、<strong>传递的</strong>，则称 R 是 S 上的<strong>等价关系</strong>。

<ul>
  <li><strong>自反性</strong>：如果元素 a 属于集合 S，则 (a, a) 属于 R<br />∀  a  ∈  S  =&gt;  (a, a) ∈ R</li>
  <li><strong>对称性</strong>：如果 (a, b) 属于 R，且 a 不等于 b，则 (b, a) 属于 R<br />(a, b)  ∈  R  ∧  a  ≠  b  =&gt;  (b, a)  ∈  R</li>
  <li><strong>传递性</strong>：如果 (a, b) 属于 R 且 (b, c) 属于 R，则 (a, c) 属于 R<br />(a, b)  ∈  R ∧ (b, c)  ∈  R  =&gt;  (a, c)  ∈  R</li>
</ul>

如果 (a, b) ∈ R，则称 a 和 b 是等价的，记作 a ~ b。<br />

---

### 树的双亲表示法

用一个<strong>链表</strong>存储树的全部结点，每个结点包含两个域：

* 数据域：用来保存数据

* 指针域：用来保存双亲节点在链表中的索引

因为根节点没有双亲节点，所以根节点的指针域的值是负数，可以利用这个负值来表示树的节点数量。

使用双亲表示法，便于寻找根节点和父节点。但是寻找子节点需要遍历整棵树。

---

### 如何划分等价类

按 R 将 S 划分成若干个不相交的子集 S1、S2、...、Sn，它们的并集是 S，称这些子集是 S 的<strong>等价类</strong>。

设集合 S 有 n 个元素，m 个形如 (x, y)(x, y ∈ S) 的<strong>等价偶对</strong>确定等价关系 R。将 S 划分成等价类的算法是：

<ul>
  <li>令集合 S 中的每个元素各自形成一个只包含单个结点的子集，记作 S1、S2、...、Sn</li>
  <li>依次读入 m 个等价偶对，对于任意等价偶对 (x, y)，设 x 属于 S<sub>i</sub>，y 属于 S<sub>j</sub>，当 S<sub>i</sub> 不等于 S<sub>j</sub> 时，可以将 S<sub>i</sub> 合并到 S<sub>j</sub>，并将 S<sub>i</sub> 置空（也可以将 S<sub>j</sub> 合并到 S<sub>i</sub>，并将 S<sub>j</sub> 置空）</li>
</ul>

<strong><em>进行合并时，如果总是将节点多的树合并到节点少的树，会导致树的高度变大，进而导致寻找节点所属的树的根节点的耗时增大。</em>因此合并时，选择将节点少的树合并到节点多的树，并利用根节点的游标域保存该树的节点数量的相反数。</strong>
