---
title: "Python的contextlib模块"
authors: [mingqiang]
tags: ["旧站归档", "Python"]
---

这篇文章最初发表于 2019-09-26，现从旧站迁入。

<!-- truncate -->

装饰器contextlib.contextmanager伴随with使用可以新建上下文大大简化代码.不必为类添加\_\_enter\_\_和\_\_exit\_\_方法.见代码：

```text
from contextlib import contextmanager
@contextmanager
def function():
    print('start ',ends='')
    yield 1
    print(' end')
with function() as p:
    print(p)
    print(' '+ 'test')
```

![](/img/wordpress-archive/2019/09/image-36.png)

效果如上图。相当于在yield的位置插入with块中的代码，并将yield的值赋给as后的变量。
