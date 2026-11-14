---
title: "记录一次使用Charles修改数据包的过程"
authors: [mingqiang]
tags: ["旧站归档", "网络"]
---

这篇文章最初发表于 2019-08-14，现从旧站迁入。

<!-- truncate -->

最近在油管看到一个视频，是一个tik tok 也就是抖音海外版的合集，看了之后感觉有点搞笑又温情满满，就想去tik tok看看外国小姐姐。然而从google play上下载打开之后发现一片空白，没有任何视频弹出。查了一下发现是字节跳动为了防止中国大陆大量的低质量用户污染国外环境，限制了来自中国用户的访问。查询发现解决办法之一是拔掉手机卡，设置英文系统语言，并且通过梯子访问就可以了，但是拔手机卡实在太麻烦怎么能忍，最后发现可以通过Charles抓包并修改请求包体的方式欺骗服务器达成目的。

[![](/img/wordpress-archive/2019/08/unnamed-file-30.png)](/img/wordpress-archive/2019/08/unnamed-file-30.png)

首先安装Charles，完毕后启动

点击标签栏Proxy-\>Proxy Settings，设置如下

[![](/img/wordpress-archive/2019/08/unnamed-file-31.png)](/img/wordpress-archive/2019/08/unnamed-file-31.png)

然后点击Proxy-\>SSL Proxy Settings，设置https代理的参数如下

[![](/img/wordpress-archive/2019/08/unnamed-file-32.png)](/img/wordpress-archive/2019/08/unnamed-file-32.png)

随后需要手机连接到电脑的WIFI或者同一局域网内，手机访问chls.pro/ssl下载证书并安装，这样手机便可以通过电脑代理访问HTTPS网址。

打开手机上Tik Tok软件，并注意Charles上相关的网址。

[![](/img/wordpress-archive/2019/08/unnamed-file-33.png)](/img/wordpress-archive/2019/08/unnamed-file-33.png)

点击Tools-\>Rewrite

[![](/img/wordpress-archive/2019/08/unnamed-file-34.png)](/img/wordpress-archive/2019/08/unnamed-file-34.png)

*可以发现服务器是在请求头的这几个相关参数中侦测地区*

[![](/img/wordpress-archive/2019/08/unnamed-file-35.png)](/img/wordpress-archive/2019/08/unnamed-file-35.png)

按左，上，下三个顺序填写修改方式。

由于二级域名总是变化，我们使用通配符\*替代二级域名，表示重写一切相关的请求头。

然后在手机上wifi上设置代理为192.168.1.107:8888(主机的固定IP)。

然后就可以愉快滴看外国小姐姐啦！
