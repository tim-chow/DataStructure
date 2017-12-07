###### 问题描述
Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

* push(x) -- Push element x onto stack.
* pop() -- Removes the element on top of the stack.
* top() -- Get the top element.
* getMin() -- Retrieve the minimum element in the stack.

###### 解决方案

* 每次函数调用都会在运行时栈的栈顶产生一个桢（frame），桢中除了包含与函数调用相关的实参，局部变量等，还包含**恢复上一个桢的信息，比如：返回地址、前一个桢的桢指针**。当函数调用完成后，再把返回地址和前一个桢的桢指针弹出，进而得到了恢复前一个桢的所有信息。  
* 在本例中，我们可以使用一个变量保存当前栈中的最小值。当push一个比当前最小值还要小的元素的时候，需要更新最小值，但是当当前最小值被pop出去的时候，我们需要**恢复到之前的最小值**，因此在push一个新的最小值的时候，我们可以把老的最小值先入栈，然后更新当前最小值，最后将新的最小值入栈。在pop的时候，如果pop出来的元素等于当前最小值，那么再从栈中pop出下一个元素，这个元素就是前一个最小值。  

上面两种利用栈的思想是类似的：都是**将追踪前一个事物的东西，保存到栈中，然后再在合适的时机，将其弹出，以便将状态进行恢复**。  
