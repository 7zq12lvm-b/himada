---
sidebar_position: 1
---

# 历史回顾

## 问世

1995年，JavaScript问世。主要解决**输入验证**的痛点。

在此之前是普遍通过电话拨号上网的年代，网速缓慢。

而要验证某个必填字段是否已填写，或者某个输入的值是否有效，都需要与服务端往返通信一次。

估计每次页面刷新验证没过的时候人们都想锤电脑？:rage:

从那时起，JavaScript逐渐成为市面上所有主流浏览器的标配。

## 名称来由

1995年，网景公司一位名叫Brendan Eich的工程师，开始为即将发布的Netscape Navigator 2开发一个叫Mocha（后来改名为LiveScript）的脚本语言。

当时的计划是在客户端和服务器端都使用它，它在服务器端叫LiveWire。

为了赶上发布时间，网景与Sun公司结为开发联盟，共同完成LiveScript的开发。

就在Netscape Navigator 2正式发布前，网景把LiveScript改名为JavaScript，以便搭上媒体当时热烈炒作Java的顺风车。

## 标准化

由于JavaScript 1.0很成功，网景又在Netscape Navigator 3中发布了1.1版本。

这时候，微软决定向IE投入更多资源。就在Netscape Navigator 3发布后不久，微软发布了IE3，其中包含自己名为JScript（叫这个名字是为了避免与网景发生许可纠纷）的JavaScript实现。

1996年8月，微软重磅进入Web浏览器领域。

微软的JavaScript实现意味着出现了两个版本的JavaScript:Netscape Navigator中的JavaScript，以及IE中的JScript。

俗话说没规矩不成方圆，随着业界担忧日甚，1997年，JavaScript 1.1作为提案被提交给欧洲计算机制造商协会（Ecma）。

JavaScript终于踏上了标准化的征程。

第39技术委员会（TC39）承担了“标准化一门通用、跨平台、厂商中立的脚本语言的语法和语义”的任务（参见TC39-ECMAScript）。

他们花了数月时间打造出ECMA-262，也就是ECMAScript（发音为“ek-ma-script”）这个新的脚本语言标准。

1998年，国际标准化组织（ISO）和国际电工委员会（IEC）也将ECMAScript采纳为标准（ISO/IEC-16262）。

自此以后，各家浏览器均以ECMAScript作为自己JavaScript实现的依据，虽然具体实现各有不同。

## JavaScript实现

JavaScript和ECMAScript基本上是同义词，但JavaScript远远不限于ECMA-262所定义的那样。

完整的JavaScript实现包含以下几个部分：

❑ 核心（ECMAScript）

❑ 文档对象模型（DOM）

❑ 浏览器对象模型（BOM）

如果不涉及浏览器的话，ECMA-262到底定义了什么？在基本的层面，它描述这门语言的如下部分：

❑ 语法

❑ 类型

❑ 语句

❑ 关键字

❑ 保留字

❑ 操作符

❑ 全局对象

ECMAScript只是对实现这个规范描述的所有方面的一门语言的称呼。

## ECMAScript版本

#### 第一版

本质上跟网景的JavaScript 1.1相同，只不过删除了所有浏览器特定的代码，外加少量细微的修改。

ECMA-262要求支持Unicode标准（以支持多语言），而且对象要与平台无关。

#### 第二版

只是做了一些编校工作，主要是为了更新之后严格符合ISO/IEC-16262的要求，并没有增减或改变任何特性。

ECMAScript实现通常不使用第2版来衡量符合性（conformance）。

#### 第三版

第一次真正对这个标准进行更新，更新了**字符串处理**、**错误定义**和**数值输出**。

此外还增加了对**正则表达式**、**新的控制语句**、**try/catch异常处理**的支持，以及为了更好地让标准国际化所做的少量修改。

switch | do-while 等。

#### 第四版 （未正式发布）

ECMA-262第4版是对这门语言的一次彻底修订。

第4版包括强类型变量、新语句和数据结构、真正的类和经典的继承，以及操作数据的新手段。

#### 第五版 （2009年12月）ES5

发布第四版的同时，TC39委员会的一个子委员会也提出了另外一份提案，叫作“ECMAScript 3.1”，只对这门语言进行了较少的改进。

这个子委员会的人认为第4版对这门语言来说跳跃太大了。因此，他们提出了一个改动较小的提案，只要在现有JavaScript引擎基础上做一些增改就可以实现。

ES3.1子委员会赢得了TC39委员会的支持，ECMA-262第4版在正式发布之前被放弃。

**ECMAScript 3.1变成了ECMA-262的第5版，于2009年12月3日正式发布。**

第5版致力于厘清第3版存在的歧义，也增加了新功能。

新功能包括:

- 原生的解析和序列化JSON数据的JSON对象
- 方便继承和高级属性定义的方法
- 以及新的增强ECMAScript引擎解释和执行代码能力的严格模式。

> 第5版在2011年6月发布了一个维护性修订版，这个修订版只更正了规范中的错误，并未增加任何新的语言或库特性。

#### 第六版 （2015年6月）ES6

这一版包含了大概这个规范有史以来最重要的一批增强特性。
ES6正式支持了

❑ 类

❑ 模块

❑ 迭代器

❑ 生成器

❑ 箭头函数

❑ 众多新的数据类型

#### 第七版 （2016年6月）ES7

这次修订只包含少量语法层面的增强，如Array.prototype.includes和指数操作符。

#### 第八版  （2017年6月）ES8

这一版主要增加了

❑ 异步函数（async/await）

❑ SharedArrayBuffer及Atomics API

❑ Object.values()/Object.entries()/Object. getOwnPropertyDescriptors()

❑ 字符串填充方法

❑ 另外明确支持对象字面量最后的逗号

#### 第九版  （2018年6月）ES9

这次修订包括

❑ 异步迭代

❑ 剩余和扩展属性

❑ 一组新的正则表达式特性

❑ Promise finally()

❑ 以及模板字面量修订

#### 第十版  （2019年6月）ES10

这次修订增加了

❑ Array.prototype.flat()/flatMap()

❑ String.prototype.trimStart()/trimEnd()

❑ Object.fromEntries()

❑ Symbol.prototype.description属性

❑ 明确定义了Function.prototype.toString()的返回值

❑ 固定了Array.prototype.sort()的顺序

❑ 另外，这次修订解决了与JSON字符串兼容的问题，并定义了catch子句的可选绑定

#### ECMAScript符合性

ECMA-262阐述了什么是ECMAScript符合性。要成为ECMAScript实现，必须满足下列条件：

❑ 支持ECMA-262中描述的所有“类型、值、对象、属性、函数，以及程序语法与语义”

❑ 支持Unicode字符标准。此外，符合性实现还可以满足下列要求

❑ 增加ECMA-262中未提及的“额外的类型、值、对象、属性和函数”。ECMA-262所说的这些额外内容主要指规范中未给出的新对象或对象的新属性

❑ 支持ECMA-262中没有定义的“程序和正则表达式语法”（意思是允许修改和扩展内置的正则表达式特性）

#### 浏览器对ECMAScript的支持

到了2008年，五大浏览器（**IE、Firefox、Safari、Chrome和Opera**）全部兼容ECMA-262第3版。

IE8率先实现ECMA-262第5版，并在IE9中完整支持。Firefox 4很快也做到了。

## DOM

**文档对象模型**（DOM, Document Object Model）是一个应用编程接口（API），用于在HTML中使用扩展的XML。

DOM将整个页面抽象为一组分层节点。HTML或XML页面的每个组成部分都是一种节点，包含不同的数据。

DOM通过创建表示文档的树，让开发者可以随心所欲地控制网页的内容和结构。使用DOM API，可以轻松地删除、添加、替换、修改节点。

### 为什么DOM是必需的

在IE4和Netscape Navigator 4支持不同形式的动态HTML（DHTML）的情况下，开发者首先可以做到不刷新页面而修改页面外观和内容。

由于网景和微软采用不同思路开发DHTML，开发者写一个HTML页面就可以在任何浏览器中运行的好日子就此终结。

#### DOM级别

为了保持Web跨平台的本性，1998年10月，DOM Level 1成为W3C的推荐标准。

这个规范由两个模块组成：**DOM Core**和**DOM HTML**。

前者提供了一种映射XML文档，从而方便访问和操作文档任意部分的方式；后者扩展了前者，并增加了特定于HTML的对象和方法。

::: tip 提示
DOM并非只能通过JavaScript访问，而且确实被其他很多语言实现了。不过对于浏览器来说，DOM就是使用ECMAScript实现的，如今已经成为JavaScript语言的一大组成部分。
:::

DOM Level 1的目标是映射文档结构，而DOM Level 2的目标则宽泛得多。

这个对最初DOM的扩展增加了对鼠标和用户界面事件、范围、遍历（迭代DOM节点的方法）的支持，而且通过对象接口支持了层叠样式表（CSS）。

另外，DOM Level 1中的DOM Core也被扩展以包含对XML命名空间的支持。

DOM Level 2新增了以下模块，以支持新的接口。

❑ DOM视图：描述追踪文档不同视图（如应用CSS样式前后的文档）的接口

❑ DOM事件：描述事件及事件处理的接口

❑ DOM样式：描述处理元素CSS样式的接口

❑ DOM遍历和范围：描述遍历和操作DOM树的接口

#### 其他DOM

❑ 可伸缩矢量图（SVG, Scalable Vector Graphics）

❑ 数学标记语言（MathML, Mathematical Markup Language）

❑ 同步多媒体集成语言（SMIL, Synchronized Multimedia Integration Language）

## BOM

IE3和Netscape Navigator 3提供了**浏览器对象模型**（BOM）API，用于支持访问和操作浏览器的窗口。

HTML5以正式规范的形式涵盖了尽可能多的BOM特性。

总体来说，BOM主要针对浏览器窗口和子窗口（frame），不过人们通常会把任何特定于浏览器的扩展都归在BOM的范畴内。比如，下面就是这样一些扩展：

❑ 弹出新浏览器窗口的能力

❑ 移动、缩放和关闭浏览器窗口的能力

❑ navigator对象，提供关于浏览器的详尽信息

❑ location对象，提供浏览器加载页面的详尽信息

❑ screen对象，提供关于用户屏幕分辨率的详尽信息

❑ performance对象，提供浏览器内存占用、导航行为和时间统计的详尽信息

❑ 对cookie的支持

❑ 其他自定义对象，如XMLHttpRequest和IE的ActiveXObject

因为在很长时间内都没有标准，所以每个浏览器实现的都是自己的BOM。有了HTML5，BOM的实现细节应该会日趋一致。

## ECMAscript是标准，js是对标准的实现
