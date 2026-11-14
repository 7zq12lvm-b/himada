---
title: "Python的with语句"
authors: [mingqiang]
tags: ["旧站归档", "Python"]
---

这篇文章最初发表于 2019-08-02，现从旧站迁入。

<!-- truncate -->

有一些需要事先设置事后清理的个工作，比如文件读写，with语句提供了非常方便的处理方式。

如果不用with语句：

```text
file = open("/tmp/foo.txt")
data = file.read()
file.close()
```

这里有两个问题:一是可能忘记关闭文件句柄； 二是文件读取数据发生异常，没有进行任何处理。下面是处理异常的加强版本：

```text
try:
    f = open('xxx')
except:
    print 'fail to open'
    exit(-1)
try:
    do something
except:
    do something
finally:
     f.close()
```

虽然这段代码运行良好，但是太冗长了。这时候就是with一展身手的时候了。除了有更优雅的语法，with还可以很好的处理上下文环境产生的异常。下面是with版本的代码：

```text
with open("/tmp/foo.txt") as file:
    data = file.read()
```

with如何工作？？依靠类中的魔法方法\_\_enter\_\_和\_\_exit\_\_。

紧跟with后面的语句被求值后，返回对象的 \_\_enter\_\_() 方法被调用，这个方法的返回值将被赋值给as后面的变量。 当with后面的代码块全部被执行完之后，将调用前面返回对象的 \_\_exit\_\_()方法。

如果有多个项，我们可以这么写：

```text
with open("x.txt") as f1, open('xxx.txt') as f2:
    do something with f1,f2
```

要使用 with 语句，首先要明白上下文管理器这一概念。有了上下文管理器，with 语句才能工作。

下面是一组与上下文管理器和with 语句有关的概念。

|  |  |
| --- | --- |
| **上下文管理协议（Context Management Protocol）**\ | 包含方法 \_\_enter\_\_() 和 \_\_exit\_\_()，支持该协议的对象要实现这两个方法。 |
| **上下文管理器（Context Manager）** | 支持上下文管理协议的对象，这种对象实现了\_\_enter\_\_() 和 \_\_exit\_\_() 方法。上下文管理器定义执行 with 语句时要建立的运行时上下文，负责执行 with 语句块上下文中的进入与退出操作。通常使用 with 语句调用上下文管理器，也可以通过直接调用其方法来使用。 |
| **运行时上下文（runtime context）** | 由上下文管理器创建，通过上下文管理器的 \_\_enter\_\_() 和\_\_exit\_\_() 方法实现，\_\_enter\_\_() 方法在语句体执行之前进入运行时上下文，\_\_exit\_\_() 在语句体执行完后从运行时上下文退出。with 语句支持运行时上下文这一概念。 |
| **上下文表达式（Context Expression）** | with 语句中跟在关键字 with 之后的表达式，该表达式要返回一个上下文管理器对象。 |

总之， with-as表达式极大的简化了每次写finally的工作，这对保持代码的优雅性是有极大帮助的。
