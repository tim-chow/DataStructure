class MinStack {
    private Stack<Integer> stack;
    private int minValue;
    
    /** initialize your data structure here. */
    public MinStack() {
        stack = new Stack<Integer>();
        minValue = Integer.MAX_VALUE;
    }
    
    public void push(int x) {
        if (x <= minValue) {
            stack.push(minValue);
            minValue = x;
        }
        
        stack.push(x);
    }
    
    public void pop() {
        if (stack.pop() == minValue)
            minValue = stack.pop();
    }
    
    public int top() {
        return stack.peek();
    }
    
    public int getMin() {
        return minValue;
    }
}
