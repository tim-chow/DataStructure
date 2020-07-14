### 栈

栈是一种**操作受限的线性表**：

* 只允许在栈顶插入数据元素

* 只允许删除、查询栈顶的数据元素

栈有两种实现方式：

* 顺序栈

* 链栈

栈有两个指针：

* base：指向栈底

* top：指向栈顶

当栈底和栈顶重合时，栈为空

顺序栈的栈顶减去栈底等于栈的大小

---

### 栈的应用

* 十进制数转换成 K 进制数  
除基取余，倒序排列

* 判断括号是否成对出现
    1. 遇到左括号，将其压入栈
    * 遇到右括号，将栈顶的数据元素弹出，并判断是否匹配
    * 检查栈是否为空

---

### 栈的应用：翻转字符串里的单词

**原题地址：**

[https://leetcode-cn.com/problems/reverse-words-in-a-string/](https://leetcode-cn.com/problems/reverse-words-in-a-string/)

**Python 实现：**

<pre>
class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        words = []

        stack1 = []
        for char in s:
            stack1.append(char)

        stack2 = []
        while stack1:
            char = stack1.pop()
            if char != " ":
                stack2.append(char)
            else:
                word = []
                while stack2:
                    word.append(stack2.pop())
                if word:
                    words.append("".join(word))

        if stack2:
            word = []
            while stack2:
                word.append(stack2.pop())
            words.append("".join(word))
        return " ".join(words)
</pre>
