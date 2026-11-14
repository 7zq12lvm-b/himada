---
title: "Linux的权限管理--chgrp/chown/chmod/umask"
authors: [mingqiang]
tags: ["旧站归档", "Linux"]
---

这篇文章最初发表于 2019-08-03，现从旧站迁入。

<!-- truncate -->

### chgrp命令

```text
 [root@localhost ~]# chgrp [-R] 所属组 文件名（目录名）
```

-R表示连同更改目录内所有文件

[![](/img/wordpress-archive/2019/08/unnamed-file-39.png)](/img/wordpress-archive/2019/08/unnamed-file-39.png)

[![](/img/wordpress-archive/2019/08/unnamed-file-40.png)](/img/wordpress-archive/2019/08/unnamed-file-40.png)

[![](/img/wordpress-archive/2019/08/unnamed-file-41.png)](/img/wordpress-archive/2019/08/unnamed-file-41.png)

在具有root组的时候，更改可以成功。如果我们尝试更改组为一个在/etc/group中不存在的群组时。就会发出Error。

### chown命令

更改文件的所有者：

```text
chown [-R] 所有者 文件或目录
```

同时更改所有者和所属组：

```text
chown [-R] 所有者:所属组 文件或目录
```

在 chown 命令中，所有者和所属组中间也可以使用点（.），但会产生一个问题，如果用户在设定账号时加入了小数点（例如 zhangsan.temp），就会造成系统误判。因此，建议大家使用冒号连接所有者和所属组。

当然，chown 命令也支持单纯的修改文件或目录的所属组，例如 `chown :group install.log` 就表示修改 install.log 文件的所属组，但修改所属组通常使用 chgrp 命令，因此并不推荐大家使用 chown 命令。

### 权限位置

最常见的文件权限有 3 种，即对文件的读（用 r 表示）、写（用 w 表示）和执行（用 x 表示，针对可执行文件或目录）权限。在 Linux 系统中，每个文件都明确规定了不同身份用户的访问权限，通过 ls 命令即可看到。

[![](/img/wordpress-archive/2019/08/unnamed-file-42.png)](/img/wordpress-archive/2019/08/unnamed-file-42.png)

前面的十个字母位置，第一个代表类型，比如目录、文件或者链接。后九个代表权限，分别是文件所有者、组用户、其他用户的操作权限。rwx分别代表读、写和执行。

### chmod命令

文件的基本权限由 9 个字符组成，以 rwxrw-r-x 为例，我们可以使用数字来代表各个权限，各个权限与数字的对应关系如下：r--\>4, w--\>2, x--\>1

修改时，把想赋予的权限数字相加即可得到权限值。

拿 rwxrw-r-x 来说，所有者、所属组和其他人分别对应的权限值为：

```text
所有者 = rwx = 4+2+1 = 7
所属组 = rw- = 4+2 = 6
其他人 = r-x = 4+1 = 5
chmod -R 765 文件名 //这便是命令格式
```

另外，还可以使用字母修改文件权限： 文件的基本权限就是 3 种用户身份（所有者、所属组和其他人）搭配 3 种权限（rwx），chmod 命令中用 u(ser)、g(roup)、o(thers) 分别代表 3 种身份，还用 a 表示全部的身份（all 的缩写）。另外，chmod 命令仍使用 r、w、x 分别表示读、写、执行权限。

[![](/img/wordpress-archive/2019/08/unnamed-file.gif)](/img/wordpress-archive/2019/08/unnamed-file.gif)

例如，如果我们要设定 .bashrc 文件的权限为 rwxr-xr-x，则可执行如下命令：

限为 rwxr-xr-x，则可执行如下命令：

```text
 chmod u=rwx,go=rx .bashrc
```

如果想要增加 .bashrc 文件的每种用户都可做写操作的权限，可以使用如下命令：

```text
 chmod a+w .bashrc
```

### umask命令

安全的基础在于对权限的设定，不仅所有已存在的文件和目录要设定必要的访问权限，创建新的文件和目录时，也要设定必要的初始权限。

Windows 系统中，新建的文件和目录时通过继承上级目录的权限获得的初始权限，而 Linux 不同，它是通过使用 umask 默认权限来给所有新建的文件和目录赋予初始权限的。  如何得知 umask 默认权限的值呢？直接通过 umask 命令即可：

[![](/img/wordpress-archive/2019/08/unnamed-file-43.png)](/img/wordpress-archive/2019/08/unnamed-file-43.png)

第 1 个数代表的是文件所具有的特殊权限（SetUID、SetGID、Sticky BIT），后 3 位数字 "022" 才是本节真正要用到的 umask 权限值，将其转变为字母形式为 ----w--w- 。 虽然 umask 默认权限是用来设定文件或目录的初始权限，但并不是直接将 umask 默认权限作为文件或目录的初始权限，还要对其进行 "再加工"。

文件和目录的真正初始权限，可通过以下的计算得到：

```text
 文件（或目录）的初始权限 = 文件（或目录）的最大默认权限 - umask权限
```

此处，也就是默认初始权限为755。

如果想最终得到文件或目录的初始权限值，我们还需要了解文件和目录的最大默认权限值。在 Linux 系统中，文件和目录的最大默认权限是不一样的：

- 对文件来讲，其可拥有的最大默认权限是 666，即 rw-rw-rw-。也就是说，使用文件的任何用户都没有执行（x）权限。原因很简单，执行权限是文件的最高权限，赋予时绝对要慎重，因此绝不能在新建文件的时候就默认赋予，只能通过用户手工赋予。
- 对目录来讲，其可拥有的最大默认权限是 777，即 rwxrwxrwx。

新建文件的默认权限：644

[![](/img/wordpress-archive/2019/08/unnamed-file-44.png)](/img/wordpress-archive/2019/08/unnamed-file-44.png)

新建文件目录的默认权限：755

[![](/img/wordpress-archive/2019/08/unnamed-file-45.png)](/img/wordpress-archive/2019/08/unnamed-file-45.png)

在计算文件或目录的初始权限时，不能直接使用最大默认权限和 umask 权限的数字形式做减法，这是不对的。例如，若 umask 默认权限的值为 033，按照数字形式计算文件的初始权限，666-033=633，但我们按照字母的形式计算会得到 （rw-rw-rw-) - (----wx-wx) = (rw-r--r--)，换算成数字形式是 644。

```text
 这里的减法，其实是“遮盖”的意思，也就是说，最大默认权限中和 umask 权限公共的部分，通过减法运算会被遮盖掉，最终剩下的“最大默认权限”，才是最终赋予文件或目录的初始权限。
```
