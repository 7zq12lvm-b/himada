---
title: "__setattr__和property装饰器"
authors: [mingqiang]
tags: ["旧站归档", "Python"]
---

这篇文章最初发表于 2019-08-31，现从旧站迁入。

<!-- truncate -->

\_\_setattr\_\_和property都能起到对属性赋值进行内容检查的功能，但是有所区别。

\_\_setattr\_\_重写了赋值方法，也就是说所有属性的赋值操作都会经过setattr完成，写完针对某特定属性的赋值检查之后，必须加一句:

```text
self.__dict__[name]=value
```

不然其他所有属性都会赋值失败，如下：

![](/img/wordpress-archive/2019/08/image-95.png)

而且还有一个问题，刚才测试的时候遇到的，这么写：

```text
class a:
    def __setattr__(self,name,value):
        if name == 'score' and type(value) is int:
            self.score = value
        else:
            self.__dict__[name] = value
t=a()
t.score=100
```

会造成maximum recursion错误，因为内部调用self.score的时候，仍然会调用\_\_setattr\_\_方法，就无限深入出不来了。

而property装饰器简洁了许多：

```text
class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
```

它使score可以像属性一样调用和返回，尽管在对象内部数据保存在\_score中。而且只对score生效，其他属性赋值还是经过默认的\_\_setattr\_\_方法。

所以我觉得用property装饰器更舒服点。
