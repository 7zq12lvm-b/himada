---
title: "apache做http代理"
authors: [mingqiang]
tags: ["旧站归档", "网络", "运维"]
---

这篇文章最初发表于 2019-08-01，现从旧站迁入。

<!-- truncate -->

1、修改 http.conf 文件 ，增加 监听端口

```text
 Listen 3333
```

开启需要的扩展

```text
 LoadModule proxy_module modules/mod_proxy.so
 LoadModule proxy_http_module modules/mod_proxy.so
```

2、httpd.conf中

```text
ProxyRequestsOn
<Proxy *>
    Requireall granted
</Proxy>
```

3、重启服务器

```text
sudo service httpd restart
```

4、浏览器中配置
