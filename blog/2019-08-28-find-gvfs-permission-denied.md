---
title: "find: ‘/run/user/1000/gvfs’: 权限不够 的解决办法"
authors: [mingqiang]
tags: ["旧站归档", "Linux"]
---

这篇文章最初发表于 2019-08-28，现从旧站迁入。

<!-- truncate -->

find时总会弹出一个这样的提示，很烦人

![](/img/wordpress-archive/2019/08/image-62.png)

*\*

![](/img/wordpress-archive/2019/08/image-63.png)

*\
查看了一下用户组*

chmod没用

![](/img/wordpress-archive/2019/08/image-64.png)

官方说这是一个**bug\[bug\#615848\]**，原因是**FUSE文件系统和权限不配**的问题，全局搜索时碰到它就会退出报错。\
其实这个目录是空的，查不查都没关系。所以，以下解决方式比较简粗暴：

```text
umount /run/user/1000/gvfs    // 卸载该文件
rm -rf /run/user/1000/gvfs    // 删除该文件
```

![](/img/wordpress-archive/2019/08/image-65.png)

舒服多了

![](/img/wordpress-archive/2019/08/image-66.png)
