---
title: "Python中的字符编码"
authors: [mingqiang]
tags: ["旧站归档", "Python"]
---

这篇文章最初发表于 2019-08-14，现从旧站迁入。

<!-- truncate -->

**一、编码类型：**

ascii：美国人发明的最早的编码格式，用1个字节也就是8个二进制位存储英文和字符，前期用了128个，后期加入了欧洲某些字符，基本上就是箭盘山给所有的字符。

unicode：2个字节，最大65535个字符，因为ASCII数量太少满足不了实际需求所以后来扩充的。

utf-8：Unicode的具体实现方式之一，因为现实中很多字符不需要两个字节来编码，比如，一个全英文网页，用unicode编码比用ascii编码大了一倍，所以人们发明了可变长度的unicode编码也就是utf-8，动态变化字节长度。具体规则不再详述。

GBK：中文国标码。在unicode未推出之前，我国为了满足汉字的网络传输而制定的编码规范。

**二、转码：**

在运行Python程序的过程中，会涉及到三个方面的编码：

1. Python程序文件本身的编码(test.py文件的编码）--自身文件
2. Python程序运行时环境的编码(比如securecrt，类似mysql客户端连接时的编码）--客户端
3. Python程序读取外部文件的编码（引用外部文件的编码）--外部文件

下面对于以上三种情况为什么需要转码分别进行说明：

1\>**自身文件编码问题**

python2默认编码为ascii，如果我们写的代码里面有非ascii字符，比如中文字符，py程序就会不认识。 中文编程时需要在文件头指定编码格式为utf8：

`#-*- coding:utf-8 -*- `

python3默认编码即为utf-8，无需任何操作。

2\>**客户端编码问题**

我们在使用mysql时，如果客户端设置为latin，而服务端为utf-8，查询内容有中文时，就会出现乱码。同样，我们在使用python时，secureCRT也是客户端，服务端就是我们连接的服务器。如果客户端（secureCRT）和服务端（python）编码不一致时，就会出现乱码。

情况二解决办法：设置客户端的编码格式和服务端一致！

3\>**读取外部文件时，出现乱码**

当我们从windows上编辑一个文件，上传到linux上时，会惊奇的发现^M符号。这个就是因为windows和linux的回车换行符不一致导致的，此时如果是python文件时，python也会报错。

[![](/img/wordpress-archive/2019/08/unnamed-file-26.png)](/img/wordpress-archive/2019/08/unnamed-file-26.png)

**三、编码转换：**

**unicode为桥梁**，utf-8和gbk互转需要经过unicode这个翻译，不然他们二者是无法直接沟通。

[![](/img/wordpress-archive/2019/08/unnamed-file-27.png)](/img/wordpress-archive/2019/08/unnamed-file-27.png)

具体来说，python2和python3又有细微区别。

[![](/img/wordpress-archive/2019/08/unnamed-file-28.png)](/img/wordpress-archive/2019/08/unnamed-file-28.png)

*python2*

[![](/img/wordpress-archive/2019/08/unnamed-file-29.png)](/img/wordpress-archive/2019/08/unnamed-file-29.png)

*python3*

python2单独搞了个unicode类型，相当于二进制，而python3来了个大变革：

1. 把字符串的编码变成了unicode,文件默认编码变成了utf-8。
2. 把str 和bytes 做了明确区分， str 就是unicode格式的字符， bytes就是单纯二进制

```text
>>> a=u'中国'#unicode编码格式的字符串
>>> a_utf8=a.encode('utf-8')  #将unicode转成utf-8编码格式>>>a_utf8'xe4xb8xadxe5x9bxbd'
>>>a_unicode=a_utf8.decode('utf-8') #从utf8编码格式转回unicode编码格式
>>> a_unicode
u'u4e2du56fd'
>>> a
u'u4e2du56fd'
>>> a
u'u4e2du56fd'
>>>
>>> b_gbk=a_unicode.encode('gbk')  #将上面unicode格式的转成gbk编码格式
>>> b_gbk'xd6xd0xb9xfa'
>>> b_unicode=b_gbk.decode('gbk') #转回unicode编码格式
>>> b_unicode   #最后发现，a_unicode、b_unicode和原始的unicode编码的a都相等。
u'u4e2du56fd'
>>> a_unicode
u'u4e2du56fd'
>>> a
u'u4e2du56fd'
```

\
