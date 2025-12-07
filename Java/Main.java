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
    public int get(int i){
        int n=0;
        intlist p=this;
        while(p!=null){
            if(n==i){
                return p.value;
            }
            n++;
            p=p.next;
        }
        return -1;  
    }
}

public class Main{
    public static void main(String[] args){
        intlist l=new intlist(15,null);
        l=new intlist(10,l);
        l=new intlist(5,l);
        System.out.println(l.size());
        System.out.println(l.iterationsize());
        System.out.println(l.get(2));
    }
}
