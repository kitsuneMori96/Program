package Java;

public class IntNode {
    public int item;
    public IntNode next;   
    public IntNode prev;

    public IntNode(int i, IntNode n) {
        item = i;
        next = n;
        if (n != null) n.prev = this;
        else prev = null;
    }
}
