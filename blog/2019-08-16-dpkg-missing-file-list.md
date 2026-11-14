---
title: "dpkg: warning: files list file for package问题"
authors: [mingqiang]
tags: ["旧站归档", "Python", "Linux", "运维"]
---

这篇文章最初发表于 2019-08-16，现从旧站迁入。

<!-- truncate -->

很久之前没安装成功就中断的pydio到现在还在给我制造麻烦。

[![](/img/wordpress-archive/2019/08/unnamed-file-23.png)](/img/wordpress-archive/2019/08/unnamed-file-23.png)

每次安装新东西，就出现几十行这样的warning，实在很让人心烦。

鼓捣了一阵子，不但没有让它消失，反而越来越多，几乎所有软件包都warning了。原因大概是折腾的时候删除了dpkg/info文件夹。

解决办法：重装每一个软件包。四百多个软件包，挨个填得类似，选择用脚本解决。

新建文本文件log把上图的错误日志复制进去。然后新建auto.py填写如下内容：

```text
import re
def main():
    fix = open('auto.sh', 'w+')
    for line in open("log"):
        pkg = re.match(re.compile('''dpkg: warning: files list file for
package '(.+)' '''), line)
        if pkg:
            cmd = "sudo apt-get install --reinstall -y " + pkg.group(1)
            fix.write(cmd + 'n')
if __name__ == "__main__":
    main()
```

生成的sh文件如下

[![](/img/wordpress-archive/2019/08/unnamed-file-24.png)](/img/wordpress-archive/2019/08/unnamed-file-24.png)

理论上运行这个等待安装完成就没问题了，阿里的网速太慢，warning也没什么实际危害，先不动它了。
