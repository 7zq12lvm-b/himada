---
title: "Python标准库-array模块"
authors: [mingqiang]
tags: ["旧站归档", "Python"]
---

这篇文章最初发表于 2019-07-25，现从旧站迁入。

<!-- truncate -->

这个模块定义了一个看起来很像 `list` 的数据结构，只不过它要求所有成员的类型都要相同。

可以用下表做一个简单参考，`array` 标准库文档包含完整的类型代码列表。

[![](/img/wordpress-archive/2019/08/unnamed-file-62.png)](/img/wordpress-archive/2019/08/unnamed-file-62.png)

## 初始化

`array` 需要两个参数，第一个参数是数据类型，第二个是要传入的数据。

```text
import array
import binascii

s = b'This is the array.'
a = array.array('b', s)

print('As byte string:', s)
print('As array      :', a)
print('As hex        :', binascii.hexlify(a))

# output
# As byte string: b'This is the array.'
# As array      : array('b', [84, 104, 105, 115, 32, 105, 115, 32,
#  116, 104, 101, 32, 97, 114, 114, 97, 121, 46])
# As hex        : b'54686973206973207468652061727261792e'
```

## Arrays 和 Files

可以将数组中内容写入文件，也可以将文件中内容读取出来存到数组。

```text
import array
import binascii
import tempfile

a = array.array('i', range(5))
print('A1:', a)

# Write the array of numbers to a temporary file
output = tempfile.NamedTemporaryFile()
a.tofile(output.file)  # must pass an *actual* file
output.flush()

# Read the raw data
with open(output.name, 'rb') as input:
    raw_data = input.read()
    print('Raw Contents:', binascii.hexlify(raw_data))

    # Read the data into an array
    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print('A2:', a2)

# output
# A1: array('i', [0, 1, 2, 3, 4])
# Raw Contents: b'0000000001000000020000000300000004000000'
# A2: array('i', [0, 1, 2, 3, 4])
```
