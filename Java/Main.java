package Java;

class intlist{
    int value;
    intlist next;
    public intlist(int v,intlist n){
        value=v;
        next=n;
    }
    public int size(){
        if(this.next==null){
            return 1;
        }
        else return 1+this.next.size();
    }
    public int iterationsize(){
        int i=0;
        intlist p=this;
        while(p!=null){
            i++;
            p=p.next;
        }
        return i;
    }
}

public class Main{
    public static void main(String[] args){
        intlist l=new intlist(15,null);
        l=new intlist(10,l);
        l=new intlist(5,l);
    }
}
