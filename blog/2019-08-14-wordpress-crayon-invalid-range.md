---
title: "WordPress插件crayon-syntax-highlighter出现invalid range错误"
authors: [mingqiang]
tags: ["旧站归档", "Wordpress"]
---

这篇文章最初发表于 2019-08-14，现从旧站迁入。

<!-- truncate -->

[![](/img/wordpress-archive/2019/08/unnamed-file-37.png)](/img/wordpress-archive/2019/08/unnamed-file-37.png)

```text
 // Override
 function clean_id($id) {
        $id = CrayonUtil::space_to_hyphen( strtolower(trim($id)) );

        return preg_replace('/[^w-+#]/msi', '', $id);
 }
```

找到报错的这一行，将`return preg_replace('/[^w-+#]/msi', '', $id);`改为`return preg_replace('/[^w-+#]/msi', '', $id);`\
