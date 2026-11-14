---
title: "为什么会出现The following packages were automatically installed and are no longer required"
authors: [mingqiang]
tags: ["旧站归档", "Linux", "运维"]
---

这篇文章最初发表于 2019-08-16，现从旧站迁入。

<!-- truncate -->

每次apt安装新软件的时候，都会弹出这样一长串提示，神烦

[![](/img/wordpress-archive/2019/08/unnamed-file-25.png)](/img/wordpress-archive/2019/08/unnamed-file-25.png)

原因是这些包是apt在安装其他包的时候根据包提供的依赖关系自动安装上去的，apt记住了他们是自动安装的，当没有包依赖于他们的时候，apt就会 认为他们已经无用。

要解决这个问题只能一个个标记。

其中pydio的许多都是没用的，可以删除，但是太多了，用脚本解决。

```text
import os

s = '''pydio-plugin-access.ftp
  pydio-plugin-access.s3 pydio-plugin-access.sftp pydio-plugin-access.smb pydio-plugin-access.webdav pydio-plugin-action.antivirus
  pydio-plugin-action.avatar pydio-plugin-action.cart pydio-plugin-action.compression pydio-plugin-action.disclaimer pydio-plugin-action.powerfs
  pydio-plugin-action.skeleton pydio-plugin-action.timestamp pydio-plugin-auth.customdb pydio-plugin-auth.ftp pydio-plugin-auth.ldap
  pydio-plugin-auth.radius pydio-plugin-auth.remote pydio-plugin-auth.smb pydio-plugin-authfront.cas pydio-plugin-authfront.cyphered
  pydio-plugin-authfront.duosecurity pydio-plugin-authfront.httpserver pydio-plugin-authfront.otp pydio-plugin-authfront.webftp
  pydio-plugin-editor.ckeditor pydio-plugin-editor.eml pydio-plugin-editor.etherpad pydio-plugin-editor.exif pydio-plugin-editor.webodf
  pydio-plugin-editor.zoho pydio-plugin-index.elasticsearch pydio-plugin-meta.comments pydio-plugin-meta.mount pydio-plugin-metastore.s3
  pydio-plugin-metastore.xattr pydio-plugin-shorten.gateway pydio-plugin-shorten.multi pydio-plugin-uploader.plupload ssl-cert'''

l = s.split(' ')

with open('clean.sh','w') as f:
        for each in l:
                f.write('sudo apt remove -y '+each+' n')

os.system('chmod +X clean.sh')
os.system('sh ./clean.sh')
```

Whenever a package is installed automatically by `apt-get` because it's a dependency of some other package, `apt-get` notes that fact; then if it notices that nothing depends on such a package any more, it will suggest that the package be removed. This is particularly useful for libraries.

That's all that's meant by "no longer required": `apt-get` doesn't know whether you're using the packages or not, but it knows that they were installed automatically and nothing depends on them any more.

To tell `apt-get` that a package shouldn't be considered as automatically installed, run [`apt-mark`](http://manpages.debian.org/cgi-bin/man.cgi?query=apt-mark) and mark it as manual\[ly installed\]:

```text
apt-mark manual git rsync
```

Or install it explicitly (this won't do anything if the latest version of the package is already installed, except for marking it as manually installed):

```text
apt-get install git rsync
```

Since these packages are already installed, `apt-get` won't install them again, but it will mark them as explicitly installed and won't suggest their removal. (If the packages aren't the newest versions available, `apt-get` will upgrade them.)
