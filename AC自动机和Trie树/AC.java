import java.util.*;

class TrieNode {
    private Map<Character, TrieNode> children = new HashMap<>();
    private boolean isEnd = false;
    private TrieNode fail;

    public TrieNode markAsEnd() {
        isEnd = true;
        return this;
    }

    public TrieNode unMarkAsEnd() {
        isEnd = false;
        return this;
    }

    public boolean getEnd() {
        return isEnd;
    }

    public TrieNode getFail() {
        return fail;
    }

    private TrieNode setFail(TrieNode fail) {
        this.fail = fail;
        return this;
    }

    public TrieNode addCharacter(char character, boolean isEnd) {
        if (!children.containsKey(character))
            children.put(character, new TrieNode());
        TrieNode node = children.get(character);
        if (isEnd)
            node.markAsEnd();
        return node;
    }

    public TrieNode getCharacter(char character) {
        if (!children.containsKey(character))
            return null;
        return children.get(character);
    }

    private TrieNode setFailPointers() {
        List<TrieNode> queue = new LinkedList<>();
        queue.add(this.setFail(this)); // 根节点的fail指针指向自己
        TrieNode node, fail;

        while (queue.size() > 0) {
            node = queue.remove(0);

            for (Map.Entry<Character, TrieNode> entry: node.children.entrySet()) {
                TrieNode childTrieNode = entry.getValue();
                queue.add(childTrieNode);
                childTrieNode.setFail(this);

                // 根节点的孩子节点的fail指针指向根节点
                if (node == this)
                    continue;

                if ((fail = node.getFail().getCharacter(entry.getKey())) != null)
                    childTrieNode.setFail(fail);
            }
        }
        return this;
    }

    @Override
    public String toString() {
        return String.format("TrieNode{children=%s, isEnd=%b}", 
            children, isEnd);
    }

    public static TrieNode makeTrieTree(List<String> words,
             Map<TrieNode, String> output) {
        if (words == null || words.size() == 0 || output == null)
            throw new RuntimeException(
                "words == null || words.size == 0 || output == null");

        TrieNode root = new TrieNode();
        TrieNode node;
        for (int i=0; i<words.size(); ++i) {
            node = root;
            for (int j=0; j<words.get(i).length(); ++j) {
                boolean isEnd = j == words.get(i).length() - 1 ? true : false;
                node = node.addCharacter(words.get(i).charAt(j), isEnd);
                if (isEnd) 
                    output.put(node, words.get(i));
            }
        }
        return root.setFailPointers();
    }

    private List<String> getOutput(Map<TrieNode, String> output, TrieNode node) {
        List<String> result = new LinkedList<>();

        while (node != this) {
            if (node.getEnd())
                result.add(output.get(node));
            node = node.getFail();
        }

        return result;
    }

    public Map<Integer, List<String>> find(String mainString,
            Map<TrieNode, String> output) {
        Map<Integer, List<String>> result = new HashMap<>();
        TrieNode node = this, nextNode;
        char character;
        int ind = 0, length = mainString.length();
        while (ind < length) {
            nextNode = node.getCharacter(character = mainString.charAt(ind));
            while (nextNode == null && node != this) {
                nextNode = (node = node.getFail()).getCharacter(character);
            }
            ind++;
            if (nextNode == null && node == this) {
                continue;
            }
            node = nextNode;
            if (node.getEnd())
                result.put(ind-1, getOutput(output, node));
        }
        return result;
    }

    public static Map<Integer, List<String>> find(String mainString,
            List<String> words) {
        if (words == null || mainString == null)
            throw new RuntimeException(
                "words == null || mainString == null");

        Map<TrieNode, String> output = new HashMap<>();
        TrieNode root = makeTrieTree(words, output);
        return root.find(mainString, output);
    }
}

public class AC {
    public static void main(String[] args) {
        List<String> words = Arrays.asList(new String[]{
            "say", "she", "shr", "he", "her"
        });
        System.out.println(TrieNode.find("shesaysherdogisweak", words));
    }
}

