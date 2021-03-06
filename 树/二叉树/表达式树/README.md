### 中缀表达式转后缀表达式<sup>注释1</sup>

使用栈保存操作符，具体步骤是：

* 遇到操作数时，直接输出

* 遇到左括号时，将其压进栈中

* 遇到右括号时，弹出栈顶的操作符，并输出，直到遇到左括号，并且**左括号不输出，右括号不进栈**

* 遇到其它操作符时，弹出栈顶的操作符，并输出，直到**栈空**或**栈顶的操作符的优先级小于该操作符的优先级**或**遇到左括号**，**然后将该操作符压进栈中**

* 最后将栈中的操作符弹出，直到栈空

---

### 表达式树

表达式树的叶子节点是操作数（operand），其它节点是操作符（operator）。

下面是将后缀表达式转换成表达式树的方法：

从前向后，遇到操作数时，则生成单节点，然后放到栈中；遇到操作符时，则生成一个新节点，并从栈中弹出 2 个元素，同时把这 2 个元素作为新节点的子树，然后将该新节点放进栈中。最后栈中的元素，就是表达式树的根。

---

### 注释

* 注释1：  
前缀表达式也叫波兰表达式；后缀表达式也叫逆波兰表达式，这两种表达式的优点是：**不需要使用括号来表达优先级** 
