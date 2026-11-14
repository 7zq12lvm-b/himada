---
title: "为网站添加CDN支持"
authors: [mingqiang]
tags: ["旧站归档", "Wordpress", "网络"]
---

这篇文章最初发表于 2019-08-29，现从旧站迁入。

<!-- truncate -->

> 简单说一下自己的理解：CDN内容分发网络原理很好理解，实际实现可能很复杂。在本文中，七牛云的服务器将cdntest域绑定到了www域下，设置了解析之后，所有对cdntest的请求都会到达七牛云，七牛云的DNS将对应的www资源分发到各地的服务器，再根据每次请求的IP位置回应最快速的服务器地址。wp super cache插件的作用就是将所有原本指向本地服务器的资源地址自动更改成指向cdntest。

家境贫穷，小破主机的带宽只有1M，勉勉强强加载一个网页，碰上大图还得加载好几秒。

了解到七牛云有免费的10G CDN流量，于是乎花了三个小时的时间搞定了这个东西。

注册七牛云，选择融合CDN选项卡。

![](/img/wordpress-archive/2019/08/image-72.png)

加速域名自己创造一个，比如cdn.codebai.xyz/cdntest.codebai.xyz

这个域名的随后需要CNAME解析到七牛云提供的地址。

![](/img/wordpress-archive/2019/08/image-73-1024x263.png)

*\*

![](/img/wordpress-archive/2019/08/image-74.png)

这里HTTPS收费，所以我把博客的HTTPS关了 ，小破站不会有人攻击的。

源站填写真正的网站地址。

回源HOST是七牛云访问源站时所使用的的HOST头部，同源站相同即可。

HOST请求头在同一个IP上部署了多个网站时发挥作用。

![](/img/wordpress-archive/2019/08/image-75-1024x471.png)

找个小文件测试一下后添加就好了。

图是一开始不懂，摸索的时候截图下来的。实际上现在用的地址是cdntest.codebai.xyz

![](/img/wordpress-archive/2019/08/image-68.png)

然后添加解析

将cdntest解析到七牛云上面给的域名

到wordpress中设置wp super cache

![](/img/wordpress-archive/2019/08/image-76.png)

CDN选项卡下，站点地址指站点真正的地址，off-site url 填写可以解析到CDN服务器的那个地址。其他容易理解。

这就大功告成了。

可以看到js等文件都走CDN服务器，一定程度上加速了。

![](/img/wordpress-archive/2019/08/image-77.png)

碰上点小问题，跨域许可(CORS)没通过。 留到日后解决。

![](/img/wordpress-archive/2019/08/image-70-1024x140.png)

Access to font at 'http://cdntest.codebai.xyz/wp-content/themes/nisarg/font-awesome/fonts/fontawesome-webfont.woff2?v=4.3.0' from origin 'http://www.codebai.xyz' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.

![](/img/wordpress-archive/2019/08/image-78-1024x110.png)

![](/img/wordpress-archive/2019/08/image-79-1024x231.png)

还在想为什么从www请求cdntest是跨域，而请求js文件不是跨域。想明白了，跨域全称ajax跨域请求，请求js不是ajax请求。

提交工单。

![](/img/wordpress-archive/2019/08/image-80-1024x706.png)
