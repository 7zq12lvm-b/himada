---
title: "记录一次文件分享系统的安装过程"
authors: [mingqiang]
tags: ["旧站归档", "运维"]
---

这篇文章最初发表于 2019-08-17，现从旧站迁入。

<!-- truncate -->

每次想要从手机移动文件到电脑上，都要用QQ的发送到电脑功能，但是电脑QQ的开启速度实在很慢，又很麻烦，有了服务器之后想搞一个文件上传下载的平台，这样每次只需要打开浏览器就可以了，十分方便。

比较了几款类似的产品，最终选择了信呼文件分享系统。

从信呼官网下载安装包并解压到网站根目录。

将网站主目录绑定到./public文件夹下

软件包依赖于php composer

进入系统目录如下命令操作。

`composer install //如果你自己下载vendor包到目录下，这个就不需要了`

`php -r "file_exists('.env') or copy('.env.example', '.env');" //创建配置文件并修改里面配置参数，如数据库信息`

修改.env文件，设置一下数据库信息。

注意：.env是隐藏文件，ubuntu下ll -a命令可查看

原截图中的数据库配置如下，密码已替换为占位值：

```dotenv
APP_NAME=信呼文件管理平台
APP_ENV=local
APP_DEBUG=true
DB_HOST=127.0.0.1
DB_DATABASE=rockdock
DB_USERNAME=root
DB_PASSWORD=REPLACE_WITH_DB_PASSWORD
DB_PREFIX=rockdock_
ROCK_XINHUKEY=
```

创建数据库并填入相关信息

`php artisan rock:docs checkbase //检测数据库是否存在，不存在就创建`

`php artisan migrate //导入系统表`

`php artisan db:seed //创建后台管理员`

出现如下错误：

[![](/img/wordpress-archive/2019/08/unnamed-file-11.png)](/img/wordpress-archive/2019/08/unnamed-file-11.png)

原因是权限不够

`chmod  -R 775 *`

`cd storage`

`chmod -R 777 *`

成功！

[![](/img/wordpress-archive/2019/08/unnamed-file-12.png)](/img/wordpress-archive/2019/08/unnamed-file-12.png)

还是要钱！！！踏马的！！！算了，去官网看看。
