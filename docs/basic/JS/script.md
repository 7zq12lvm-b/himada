# script 元素

## 属性

HTML规范中\<script>元素有下列8个属性。

### async

可选。表示应该**立即开始下载脚本，但不能阻止其他页面动作**，比如下载资源或等待其他脚本加载。

**只对外部脚本有效**。

### charset

可选。使用src属性指定的代码字符集。大部分浏览器不在乎它的值。

### crossorigin

可选。配置相关请求的CORS（跨源资源共享）设置。默认不适用CORS。

crossorigin=”anonymous“配置文件不必设置请求凭据标志。

crossorigin=”use-credentials“设置凭据标志，意味着出站请求会包含凭据。

### defer

可选。表示脚本可以延迟到文档完全被解析和显示之后再执行。**只对外部文件有效**。

### integrity

可选。允许对比接收到的资源和指定的加密签名以验证资资源完整性。

如果接到的资源的签名跟这个属性指定的签名不匹配，脚本不执行，页面报错。

此属性用于确保内容分发网络（CDN）不会提供恶意内容。

### language

废弃。

### src

可选。表示包含要执行的代码的外部文件。

### type

可选。替代language，表示代码块中脚本语言的内容类型（MIME类型）。

按照惯例，这个值始终都是"text/javascript"，尽管"text/javascript"和"text/ecmascript"都已经废弃了。

JavaScript文件的MIME类型通常是"application/x-javascript"，不过给type属性这个值有可能导致脚本被忽略。

在非IE的浏览器中有效的其他值还有"application/javascript"和"application/ecmascript"。

如果这个值是module，则代码会被当成ES6模块，而且只有这时候代码中才能出现import和export关键字。

## 使用

使用\<script>的方式有两种：

通过它直接在网页中嵌入JavaScript代码，以及通过它在网页中包含外部JavaScript文件。

在使用行内JavaScript代码时，要注意代码中不能出现字符串\</script>。

比如，下面的代码会导致浏览器报错：

```js
<script>
    function sayScript() {
        console.log("</script>");
    }
</script>
```

浏览器解析行内脚本的方式决定了它在看到字符串\</script>时，会将其当成结束的\</script>标签。想避免这个问题，只需要转义字符“\”即可：

```js
<script>
    function sayScript() {
        console.log("<\/script>");
    }
</script>
```
