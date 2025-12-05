package Java;
// 1. 定义类
class Person {
    // 2. 定义属性（成员变量）
    String name;
    int age;

    // 3. 定义构造方法
    public Person(String personName, int personAge) {
        name = personName;
        age = personAge;
    }

    // 4. 定义成员方法
    public void introduce() {
        System.out.println("Hello, my name is " + name + " and I am " + age + " years old.");
    }
}

// 使用类
public class Main {
    public static void main(String[] args) {
        // 5. 实例化对象（创建对象）
        Person person1 = new Person("Alice", 25);

        // 6. 访问对象的方法
        person1.introduce(); // 输出: Hello, my name is Alice and I am 25 years old.
    }
}