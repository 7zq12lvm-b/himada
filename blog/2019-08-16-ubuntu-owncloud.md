---
title: "基于Ubuntu+Owncloud的私有云网盘"
authors: [mingqiang]
tags: ["旧站归档", "Linux"]
---

这篇文章最初发表于 2019-08-16，现从旧站迁入。

<!-- truncate -->

百度网盘实在是太太太太太太慢了，前些日子鼓捣的那个文件分享系统也收费，又想试试其他的开源软件，打算搞搞大名鼎鼎的owncloud。

但是刚开始就碰上了问题，以前装pydio没装成功，好像碰到了一些依赖的问题，也没解决，今天按照官网装ownlcloud的过程中又出现了。

```text
dpkg: error processing package pydio-plugin-auth.ldap (--configure):
  dependency problems - leaving unconfigured
 dpkg: dependency problems prevent configuration of pydio-plugin-auth.ftp:
  pydio-plugin-auth.ftp depends on pydio-core (= 8.2.3-1); however:
   Package pydio-core is not configured yet.
  pydio-plugin-auth.ftp depends on pydio-plugin-access.ftp; however:
   Package pydio-plugin-access.ftp is not configured yet.
```

寻找解决办法的时候突然想到了那句著名的，万物皆文件，嘿，那么我把所有和pydio相关的文件都删除，那不就相当于卸载干净了？

```text
find / -name *pydio*
rm -rf  XXXXX
```

一通骚操作，问题解决。然后继续按照owncloud官网教程安装。

```text
Ubuntu_16.04 owncloud-files-10.2.1-1+1.2
Add (at least temporarily) a download repository. This requires registering trusted key. (More information). Run the following shell commands as root to trust the repository:
wget -nv https://download.owncloud.org/download/repositories/production/Ubuntu_16.04/Release.key -O Release.key apt-key add - < Release.key
Run the following shell commands as root to add the repository and install from there.
echo 'deb http://download.owncloud.org/download/repositories/production/Ubuntu_16.04/ /' > /etc/apt/sources.list.d/owncloud.list apt-get update apt-get install owncloud-files
```

屏幕闪烁过后安装完成。apt-get默认将owncloud网站文件安装到了/var/www/owncloud文件夹下，与apache默认目录不同，于是

```text
cp -R /var/www/owncloud/*  目标文件夹
```

打开网站，却提示：

[![](/img/wordpress-archive/2019/08/unnamed-file-13.png)](/img/wordpress-archive/2019/08/unnamed-file-13.png)

不影响！装低版本的php去！宝塔面板真是个好东西！

[![](/img/wordpress-archive/2019/08/unnamed-file-14.png)](/img/wordpress-archive/2019/08/unnamed-file-14.png)

设置php版本为7.0(吐槽，php编译安装真的太特么慢了)

进去了，哈哈哈哈哈

[![](/img/wordpress-archive/2019/08/unnamed-file-15.png)](/img/wordpress-archive/2019/08/unnamed-file-15.png)

等等，有问题

[![](/img/wordpress-archive/2019/08/unnamed-file-16.png)](/img/wordpress-archive/2019/08/unnamed-file-16.png)

没权限？？chmod 777 -R config

出来了，但是......\
唉当时手贱选了16.04版本32位的ubuntu弄得现在老出相关问题。算了不就是不能上传大于40GB的文件吗，反正小破主机只有40GB的存储容量，我也不会存那么大的文件。

配置用户和数据库

[![](/img/wordpress-archive/2019/08/unnamed-file-17.png)](/img/wordpress-archive/2019/08/unnamed-file-17.png)

又是权限问题

[![](/img/wordpress-archive/2019/08/unnamed-file-18.png)](/img/wordpress-archive/2019/08/unnamed-file-18.png)

宝塔文件夹的用户组是www，好像没有写权限，懒得搞了，chmod 777吧又不行了

[![](/img/wordpress-archive/2019/08/unnamed-file-19.png)](/img/wordpress-archive/2019/08/unnamed-file-19.png)

chmod 0770 -R data

啊啊啊啊改了之后还是不行

[![](/img/wordpress-archive/2019/08/unnamed-file-20.png)](/img/wordpress-archive/2019/08/unnamed-file-20.png)

你给它0770，他说你没权限，你给它777他说不安全？？？

试试更改一下用户组，我记得apache的用户组是www

chown -R www:www \*

搞定

[![](/img/wordpress-archive/2019/08/unnamed-file-21.png)](/img/wordpress-archive/2019/08/unnamed-file-21.png)

我错了，速度依然很慢。因为小破主机的带宽只有1M，上传倒是很快。

设置页面里有很多警告提示：

有一个缓存相关的，在官网文档里找到了解决办法，安装redis和memcache的php扩展

[![](/img/wordpress-archive/2019/08/unnamed-file-22.png)](/img/wordpress-archive/2019/08/unnamed-file-22.png)
