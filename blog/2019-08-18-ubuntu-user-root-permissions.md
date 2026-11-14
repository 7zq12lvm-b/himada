---
title: "ubuntu赋予普通用户root权限"
authors: [mingqiang]
tags: ["旧站归档", "Linux"]
---

这篇文章最初发表于 2019-08-18，现从旧站迁入。

<!-- truncate -->

**事后PS:不可行啊，不知道为什么改了重启之后chrome等等软件都无法打开，又是权限的问题，改回来了，Linux真是很复杂**

ubuntu默认不允许ROOT登陆

但是每次执行诸如mv、cp、rm这样的命令都得加sudo再输入密码实在是太麻烦了

![](/img/wordpress-archive/2019/08/image-61.png)

方法一、修改passwd文件

1、编辑passwd文件

```text
sudo vim /etc/passwd
```

2、找到你想提权的用户（比如mrbai），将用户名后面的数字改成0

```text
找到用户test
mrbai:x:1000:1000::/home/test

修改权限
mrbai:x:0:0::/home/test
```

3、重启电脑，登录test账户。

方法二、临时使用root用户

```text
su root
```

然后输入root的密码，如果是第一次使用root用户，会提示密码错误，需要修改root账户密码

```text
passwd
```

然后输入两次相同的密码
