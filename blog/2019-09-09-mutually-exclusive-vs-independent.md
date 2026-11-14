---
title: "互不相容和相互独立的区别"
authors: [mingqiang]
tags: ["旧站归档", "数学笔记", "概率论与数理统计"]
---

这篇文章最初发表于 2019-09-09，现从旧站迁入。

<!-- truncate -->

互不相容又叫互斥，即两个事件不能同时发生，强调“同时发生”。

发生了A就不能发生B，发生了B就不能发生A.

而[相互独立](https://www.baidu.com/s?wd=%E7%9B%B8%E4%BA%92%E7%8B%AC%E7%AB%8B&tn=SE_PcZhidaonwhc_ngpagmjz&rsv_dl=gh_pc_zhidao)即使两个事件各自发生与否与另一个事件的发生与否没有关系；

A和B独立的意思就是，A发生和B发生没有关系，A发生不会影响B发生，A和B也可能同时发生，不过A和B互不影响。

设有A、B两个集合

如果A、B互不相容，则A∩B=Φ，P（A∩B）= 0，P(B│A)= P(A│B)=0

如果A、B[相互独立](https://www.baidu.com/s?wd=%E7%9B%B8%E4%BA%92%E7%8B%AC%E7%AB%8B&tn=SE_PcZhidaonwhc_ngpagmjz&rsv_dl=gh_pc_zhidao)，则 P（A∩B）= P（A）P（B）， P(B│A)= P(B)， P(A│B)=P（A）

[![](/img/wordpress-archive/2019/09/unnamed-file.jpg)](/img/wordpress-archive/2019/09/unnamed-file.jpg)

**拓展资料：**

要有两事件A,B。A，B发生的概率分别为P（A）、P（B），AB事件同时发生的概率为P（AB）。若A、B不相容，则P(AB)=0，反之未必。

加法公式对应互不相容性，乘法公式对应独立性。 如果A和B互不相容 P（A U B）= P（A）+P（B） 如果A和B[相互独立](https://www.baidu.com/s?wd=%E7%9B%B8%E4%BA%92%E7%8B%AC%E7%AB%8B&tn=SE_PcZhidaonwhc_ngpagmjz&rsv_dl=gh_pc_zhidao) P（AB） = P（A） \* P（B）
