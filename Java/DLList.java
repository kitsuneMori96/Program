package Java;

public class DLList {
    private class Node {
        int item;
        Node prev;
        Node next;

        Node(int item, Node prev, Node next) {
            this.item = item;
            this.prev = prev;
            this.next = next;
        }
    }

    private Node sentF;   // front sentinel
    private Node sentB;   // back sentinel
    private int size;

    public DLList() {
        sentF = new Node(0, null, null);
        sentB = new Node(0, null, null);

        sentF.next = sentB;
        sentB.prev = sentF;

        size = 0;
    }

    /* 在链表头部插入 x */
    public void addFirst(int x) {
        Node firstNode = sentF.next;
        Node newNode = new Node(x, sentF, firstNode);

        sentF.next = newNode;
        firstNode.prev = newNode;

        size++;
    }

    /* 在链表尾部插入 x */
    public void addLast(int x) {
        Node lastNode = sentB.prev;
        Node newNode = new Node(x, lastNode, sentB);

        lastNode.next = newNode;
        sentB.prev = newNode;

        size++;
    }

    public int getFirst() {
        if (size == 0) throw new RuntimeException("Empty list");
        return sentF.next.item;
    }

    public int getLast() {
        if (size == 0) throw new RuntimeException("Empty list");
        return sentB.prev.item;
    }

    /* 删除第一个 */
    public int removeFirst() {
        if (size == 0) throw new RuntimeException("Empty list");

        Node firstNode = sentF.next;
        int value = firstNode.item;

        Node second = firstNode.next;
        sentF.next = second;
        second.prev = sentF;

        size--;
        return value;
    }

    /* 删除最后一个 */
    public int removeLast() {
        if (size == 0) throw new RuntimeException("Empty list");

        Node lastNode = sentB.prev;
        int value = lastNode.item;

        Node before = lastNode.prev;
        before.next = sentB;
        sentB.prev = before;

        size--;
        return value;
    }

    public int size() {
        return size;
    }

    /* 打印链表，方便调试 */
    public void printList() {
        Node p = sentF.next;
        while (p != sentB) {
            System.out.print(p.item + " ");
            p = p.next;
        }
        System.out.println();
    }

    public static void main(String[] args) {
        DLList lst = new DLList();
        lst.addLast(3);
        lst.addLast(9);
        lst.addFirst(7);
        lst.printList();  // 7 3 9
        lst.removeLast(); 
        lst.printList();  // 7 3
    }
}
