---
title: "python的一些特殊方法"
authors: [mingqiang]
tags: ["旧站归档", "Python"]
---

这篇文章最初发表于 2019-08-24，现从旧站迁入。

<!-- truncate -->

**\_\_repr\_\_方法**

\_\_repr\_\_（）是 Python 类中的一个特殊方法，由于 object 类己提供了该方法， 而所有的 Python 类 都是 object 类的子类， 因此所有的 Python 对象都具有 \_\_repr\_\_（） 方法。

\_repr＿（）是一个非常特殊的方法，它是一个“ 自我描述” 的方法，该方法通常用于实现这样 一个功能： 当程序员直接打印该对象时，系统将会输出该对象的“自我描述”信息， 用来告诉外界该对象具有的状态信息。

```text
class Apple:
    # 实现构造器
    def __init__(self, color, weight):
        self.color = color;
        self.weight = weight;
    # 重写toString()方法，用于实现Apple对象的“自我描述”
    def __repr__(self):
        return "Apple[color=" + self.color +\
            ", weight=" + str(self.weight) + "]"
a = Apple("红色" , 5.68)
# 打印Apple对象
print(a)
```

**\_\_del\_\_方法**

\_\_init\_\_方法用于初始化一个python对象，而\_\_del\_\_则用来销毁python对象，也就是说在任何python对象被系统回收时，系统自动调用\_\_del\_\_方法。也叫作垃圾回收(GC)过程。

python采用自动引用计数来回收对象内存空间，如果一个对象的引用计数变成了 0，则说明程序中不再有变量引用该对象，表明程序不 再需要该对象，因此 Python 就会回收该对象。

![](/img/wordpress-archive/2019/08/image-92.png)

只有一个对象的引用计数为0的时候，\_\_del\_\_方法才会被调用。

**\_\_dir\_\_方法**

对象的  **\_\_dir\_\_方法** 用于列出该对象内部的所有属性（包括方法）名，该方法将会返回包含所 有属性（方法）名的序列。 当程序对某个对象执行 dir(object）函数时，实际上就是将该对象的 **\_\_dir\_\_方法**返回值进行排 序，然后包装成列表。

![](/img/wordpress-archive/2019/08/image-94.png)

**\_\_dict\_\_属性**

**\_\_dict\_\_属性** 用于查看对象内部存储的所有属性名和属性值组成的字典， 通常程序直接使用该属性即可。 程序使用 **\_\_dict\_\_属性** 既可查看对象的所有内部状态， 也可通过字典语法来访问或修改指定属性的值。 例如如下程序。

```text
class Item:
    def __init__ (self, name, price):
        self.name = name
        self.price = price
im = Item('鼠标', 28.9)
print(im.__dict__)  # ①
# 通过__dict__访问name属性
print(im.__dict__['name'])
# 通过__dict__访问price属性
print(im.__dict__['price'])
im.__dict__['name'] = '键盘'
im.__dict__['price'] = 32.8
print(im.name) # 键盘
print(im.price) # 32.8
```

**\_\_getattr\_\_和\_\_setattr\_\_**

我知道了！！！BeautifulSoup能用属性的方式查看节点信息，应该就是用的\_\_getattr\_\_方法

当程序操作（包括访问、设置、删除）对象的属性时， Python 系统同样会执行该对象特定的 方法。

这些方法共涉及如下几个。

**\_\_getattribute\_\_（self, name）**： 当程序访问对象的 name 属性fl才被自动调用。 \
**\_\_getattr\_\_（self, name）**： 当程序访问对象的 name 属性且该属性不存在时被自动调用 。 \
**\_\_setattr\_\_（self, name, value）**：当程序对对象的 name 属性赋值时被自动调用。 \
**\_\_delattr\_\_（self, name）**：当程序删除对象的 name 属性时被自动调用 。

重写上面的方法，可以为 Python 类“合成”属性一一当属性不存在时， 程序会委托给上面的方法来实现，因此程序可通过重写这些方法来“合成”属性。

```text
class Rectangle:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
    def __setattr__(self, name, value):
        print('----设置%s属性----' % name)
        if name == 'size':
            self.width, self.height = value
        else:
            self.__dict__[name] = value
    def __getattr__(self, name):
        print('----读取%s属性----' % name)
        if name == 'size':
            return self.width, self.height
        else:
            raise AttributeError
    def __delattr__(self, name):
        print('----删除%s属性----' % name)
        if name == 'size':
            self.__dict__['width'] = 0
            self.__dict__['height'] = 0

rect = Rectangle(3, 4)
print(rect.size)
rect.size = 6, 8
print(rect.width)
del rect.size
print(rect.size)
```

注意这里用self.\_\_dict\_\_\[name\]设置属性很巧妙。

\

**\_\_call\_\_属性**

程序可通过判断该属性（或方法）是否包含 call 属性来确定其是否可调用。

![](/img/wordpress-archive/2019/08/image-96.png)

实际上，一个函数（甚至对象）之所以能执行，关键就在于\_\_call\_\_（）方法。实际上 x(argl, arg2, … ) 只是 x.\_\_call\_\_（argl, arg2， …）的快捷写法，因此我们甚至可以为自定义类添加\_\_call\_\_ 方法，从而使得该类的实例也变成可调用的。

![](/img/wordpress-archive/2019/08/image-97.png)

\
\
