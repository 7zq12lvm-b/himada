---
title: "Python标准库-binascii模块"
authors: [mingqiang]
tags: ["旧站归档", "Python"]
---

这篇文章最初发表于 2019-07-29，现从旧站迁入。

<!-- truncate -->

在二进制和ASCII码之间转换

> The binascii module contains a number of methods to convert between binary and various ASCII-encoded binary representations. Normally, you will not use these functions directly but use wrapper modules like uu, base64, or binhex instead. The binascii module contains low-level functions written in C for greater speed that are used by the higher-level modules.
>
>
>
> — 官方文档内容

#### **binascii.a2b\_uu()**

查了半天资料也没弄懂，先留着

[![](/img/wordpress-archive/2019/08/unnamed-file-56.png)](/img/wordpress-archive/2019/08/unnamed-file-56.png)

#### **binascii.a2b\_base64**()

将str或者bytes转化成base64编码

可能会出现如下问题

[![](/img/wordpress-archive/2019/08/unnamed-file-58.png)](/img/wordpress-archive/2019/08/unnamed-file-58.png)

*这是由于编码规则决定的，base64编码必须保证原文长度是4的倍数*

b2a是解密，a2b是加密

[![](/img/wordpress-archive/2019/08/unnamed-file-60.png)](/img/wordpress-archive/2019/08/unnamed-file-60.png)

#### **binascii.a2b\_qp(data, header=False)**

\
 Convert a block of quoted-printable data back to binary and return the binary data. More than one line may be passed at a time. If the optional argument header is present and true, underscores will be decoded as spaces.

#### **binascii.b2a\_qp(data, quotetabs=False, istext=True, header=False)**

\
 Convert binary data to a line(s) of ASCII characters in quoted-printable encoding. The return value is the converted line(s). If the optional argument quotetabs is present and true, all tabs and spaces will be encoded. If the optional argument istext is present and true, newlines are not encoded but trailing whitespace will be encoded. If the optional argument header is present and true, spaces will be encoded as underscores per RFC1522. If the optional argument header is present and false, newline characters will be encoded as well; otherwise linefeed conversion might corrupt the binary data stream.

qp是另一种十分不常用的编码格式，略过不表

#### **binascii.crc32(data\[, value\])**

计算一段数据的CRC32（循环冗余检验）验证数据包是否完整

[![](/img/wordpress-archive/2019/08/unnamed-file-61.png)](/img/wordpress-archive/2019/08/unnamed-file-61.png)

#### **binascii.b2a\_hex(data)\
binascii.hexlify(data)**

两者一样，用16进制表示data，因此字符长度会翻倍

#### **binascii.a2b\_hex(hexstr)\
binascii.unhexlify(hexstr)**

同上，只不过过程相反
