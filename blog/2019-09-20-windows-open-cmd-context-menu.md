---
title: "右键菜单添加打开CMD选项"
authors: [mingqiang]
tags: ["旧站归档", "其他"]
---

这篇文章最初发表于 2019-09-20，现从旧站迁入。

<!-- truncate -->

每次都得win+r才能打开cmd，还得一次一次cd，神烦。添加右键菜单更加方便快捷，自动进入当前目录。

WIN+R，输入regedit，展开HKEY\_CLASSES\_ROOT——Directory——Background——Shell——cmd——command，可以看到数据的值应该就是CMD的快捷方式了。双击并把它复制下来。

![](/img/wordpress-archive/2019/09/image-27-1024x286.png)

接着在shell下面新建一个“项”，名字就是右键需要现实的，如“CMD”，接着在“CMD”下面再新建一个“项”，名称为“command”，把上一步复制的值粘贴进去。

![](/img/wordpress-archive/2019/09/image-28-1024x289.png)

搞定。
