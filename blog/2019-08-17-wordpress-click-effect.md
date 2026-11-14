---
title: "Wordpress添加鼠标点击效果"
authors: [mingqiang]
tags: ["旧站归档", "Wordpress"]
---

这篇文章最初发表于 2019-08-17，现从旧站迁入。

<!-- truncate -->

## 实现方法

## 原文的音乐播放器已停用。

将下面这一段代码复制粘贴到你的页脚文件前面，一般名为footer.php，在主题的根目录中，如下图所示。

```html
<script type="text/javascript">
/* 鼠标特效 */
var a_idx = 0;
jQuery(document).ready(function($) {
   $("body").click(function(e) {
       var a = new Array("富强", "民主");
       var $i = $("<span/>").text(a[a_idx]);
       a_idx = (a_idx + 1) % a.length;
       var x = e.pageX,
       y = e.pageY;
       $i.css({
           "z-index": 999999999999999999999999999999999999999999999999999999999999999999999,
           "top": y - 20,
           "left": x,
           "position": "absolute",
           "font-weight": "bold",
           "color": "#ff6651"
       });
       $("body").append($i);
       $i.animate({
           "top": y - 180,
           "opacity": 0
       },
       1500,
       function() {
           $i.remove();
       });
   });
});
    </script>
```
