### 问题描述

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

* push(x) -- Push element x onto stack.
* pop() -- Removes the element on top of the stack.
* top() -- Get the top element.
* getMin() -- Retrieve the minimum element in the stack.

---

### 解题思路

使用一个变量保存当前的最小值，当 push 一个比当前最小值还要小的元素时，更新最小值。但是当当前最小值被 pop 出去时，需要**恢复到之前的最小值**，解决方法是：在 push 新的最小值时，把老的最小值压入栈，然后更新当前最小值，最后将新的最小值入栈。在 pop 时，如果 pop 出来的元素等于当前最小值，那么再从栈中 pop 出下一个元素，这个元素就是前一个最小值。

其基本思想是：**将“路径信息”保存到栈中，在合适的时机将其弹出，以恢复状态**。
