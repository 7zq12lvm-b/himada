---
title: "flask中flash函数相关"
authors: [mingqiang]
tags: ["旧站归档", "Flask"]
---

这篇文章最初发表于 2019-09-20，现从旧站迁入。

<!-- truncate -->

抓包测试出来的：

以flask官方教程中的项目flaskr为例，单击share后以post提交表单

![](/img/wordpress-archive/2019/09/image-31.png)

然后服务器返回一个302重定向。

![](/img/wordpress-archive/2019/09/image-32.png)

重定向到首页。应该是flask内部的上下文机制可以确定你发送的首页请求来自于提交表单之后的重定向，所以新首页能够显示出源码中flash的内容。

![](/img/wordpress-archive/2019/09/image-33.png)

![](/img/wordpress-archive/2019/09/image-34.png)

突发奇想测试一下：将上图中原有的redirect注释掉，改成return一个字符串。

![](/img/wordpress-archive/2019/09/image-35.png)

点击share之后变成了这样！也就是说，flash不负责响应，只是修改了响应模板中的内容。必须配合redirect使用才有效。

以下是segmentfault上的问答：

lask 的 flash 闪现 和 纯粹的 ajax 都是为了实现用户的良好体验。

1、flask 的 flash 闪现，大多是用在反馈用户的提示，你可以参考一下[https://www.os373.cn/admin/login](https://www.os373.cn/admin/login)，试试输错用户名和密码之后是啥提示。但是，敲黑板，当当当，不管怎么说，这里**没有使用 ajax 的局部刷新机制，还是全页面提交内容，服务器返回相关信息，然后全面刷新之后，显示你设计好的内容提示**，对于多 form 页面，在你没有完全掌握该功能的情况下，建议少用或禁用。

2、对于 ajax，那就是 js 的局部刷新机制，在 web 上，只要能力所及，可以随便使用。
