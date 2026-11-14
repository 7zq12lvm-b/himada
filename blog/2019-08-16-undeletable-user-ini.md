---
title: "root用户无法删除的文件-.user.ini"
authors: [mingqiang]
tags: ["旧站归档", "Linux", "运维"]
---

这篇文章最初发表于 2019-08-16，现从旧站迁入。

<!-- truncate -->

手动删除宝塔面板自动建立的网站根目录时，发现有一个文件.user.ini总是无法删除，sudo rm 和sudo chown 777 对它都无能为力，很好奇这是怎么个情况。

原来，这个文件被命令chattr加了属性i，也就是无法修改。这里引入了两个命令chattr，lsattr。

[![](/img/wordpress-archive/2019/08/unnamed-file-46.png)](/img/wordpress-archive/2019/08/unnamed-file-46.png)

想要修改的话，chattr -i  .user.ini即可

`root@iZ2ze0lkgiu7ob8hnbggobZ:/www/wwwroot/cloud.codebai.xyz# sudo chmod 777 .user.ini   chmod: changing permissions of '.user.ini': Operation not permitted  root@iZ2ze0lkgiu7ob8hnbggobZ:/www/wwwroot/cloud.codebai.xyz# lsattr .user.ini   ----i--------e-- .user.ini  You have new mail in /var/mail/root  root@iZ2ze0lkgiu7ob8hnbggobZ:/www/wwwroot/cloud.codebai.xyz# chattr -i .user.ini `

[![](/img/wordpress-archive/2019/08/unnamed-file-47.png)](/img/wordpress-archive/2019/08/unnamed-file-47.png)
