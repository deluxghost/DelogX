# 你好，DelogX

欢迎使用 DelogX。这是一个由 Python 编写的，基于 Flask 框架的轻量级动态 Markdown 博客系统。

## 快速入门

DelogX 采用文件系统管理文章和页面，每一篇文章或一个页面都指向一个普通 Markdown 文件。反过来说，每一个合格的 Markdown 文件都可以作为一篇文章或一个页面。

### 元信息

每一个 `.md` 文件本身都包含了文章或页面的全部元信息：

* 标题：如果文件的首行是一个符合 Markdown 语法的一级标题，那么这个一级标题会被作为该文章或页面的标题，否则就会以 URL 作为标题；
* 修改时间：就是该文件的修改时间，页面的修改时间会被忽略。
* 正文：去掉标题后的其他所有文本。

### 隐藏内容

在类 UNIX 操作系统上，如果一个文件的文件名以一个点号（`.`）开头，那么这个文件会被视为一个隐藏文件。在 DelogX 中，这样的 `.md` 文件也会被隐藏——文章不会在文章列表中显示，页面不会出现在导航栏中。但是，这些内容仍然可以通过正确的 URL 访问。

### 排序

所有文章都会按照修改时间倒序排列，也就是说，刚刚修改过的文章永远出现在首页。

页面通常会由 Python 解释器自动排序，但您也可以手动更改它们的顺序，方法是在页面文件的后缀名前加上一个正整数形式的“副后缀名”，例如 `hello-world.1.md`、`demo.2.md`。所有包含序号的页面将会被排列在其他页面之前。

### URL

文章或页面都要通过一个唯一的 URL 来访问，DelogX 的 URL 由前缀和文件名两部分组成。URL 前缀可以在配置文件中进行设置，它们的形式类似于 `/post`。

文件名部分则需要去掉文件全名中的后缀名（`.md`）、开头点号（`.`）和排序序号（例如 `.1`、`.2`），因为这些内容属于元信息。并且，URL 会被自动地 urlencode。

例如，一个页面 `.hidden-page.2.md` 的 URL **可能**是 `/page/hidden-page`。如果加上域名的话，则是 `http://yourblog.com/page/hidden-page`。

### Markdown

DelogX 支持大多数标准 Markdown 语法（异同见 [python-markdown 文档]{: target="_blank"}），同时支持如下 Extra 语法：

* 表格
* 删除线
* 围栏式代码块
* 标签属性

本文附有一份非常精简的“Markdown 快速入门”。

[python-markdown 文档]: http://pythonhosted.org/Markdown/#differences

### 代码高亮

DelogX 采用 [highlight.js]{: target="_blank"} 作为代码高亮引擎。通常情况下，它可以自动识别代码块和编程语言，但通过围栏式代码块，您也可以手动指定编程语言：

````markdown
```python
from __future__ import print_function
print("Hello Python3!")
```
````

DelogX 默认提供了 GitHub 色彩方案，您也可以按照 highlight.js 的文档来自定义高亮支持语言和色彩方案。

[highlight.js]: https://highlightjs.org/

### 静态文件

DelogX 将 CSS、JS、图片等静态文件存储在 `static` 目录中，您可以通过链接 `http://yourblog.com/static/filename` 来访问目录中的内容。

### 配置文件

DelogX 的配置文件是 `config.json`，您可以查阅 DelogX 的文档以了解每一个选项。

### 更多细节

您可以访问下列关于 DelogX 的资源：

* 源代码：<https://github.com/deluxghost/DelogX>
* Wiki 文档：<https://github.com/deluxghost/DelogX/wiki>

## Markdown 快速入门

### HTML 兼容性

Markdown 被设计成兼容 HTML 格式，因此，您可以直接在 Markdown 文件中插入 HTML 代码。

### 标题

```markdown
# 一级标题
## 二级标题
###### 六级标题

# 另一个一级标题 #
## 另一个二级标题 ##
#### 四级标题 ####

另一种一级标题
============

另一种二级标题
------------
```

### 强调

```markdown
强调通常包括**加重强调**和*普通强调*。
前者通常表现为粗体，后者通常表现为斜体。
两者也可以***混合起来***使用。
```

### 列表

```markdown
* 无序列表项
* 无序列表项
* 无序列表项
* 无序列表项
```

```markdown
1. 有序列表项
2. 有序列表项
3. 有序列表项
4. 有序列表项
```

### 引用

```markdown
> 引用起始于一个大于号
> 您可以在每行开头都写一个
>
> > 嵌入引用也是可以的
> > 例如这样
```

### 代码

```markdown
行内式代码可以用一对反引号括起来，例如 `import urllib` 这样。
```

如果想要输入一个代码块，您可以直接将代码复制过来，然后增加一级缩进：

```markdown
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
```

DelogX 还支持另一种能够指定编程语言的围栏式代码块：

````markdown
```python
from __future__ import print_function
print("Hello Python3!")
```
````

### 链接

```markdown
行内式链接：[GitHub](http://github.com/)

参考式链接：[Wikipedia][1]

[1]: https://www.wikipedia.org/
```

### 图片

```markdown
![MyPhoto](/static/images/photo.png "一张图片")
```

### 水平线

```markdown
***

---

* * *
```

### 表格

```markdown
| ID   | A       | B       | C       |
|------|---------|---------|---------|
| 1    | Option1 | Option1 | Option1 |
| 2    | Option2 | Option2 | Option2 |
| 3    | Option3 | Option3 | Option3 |

实际上，去掉空格和多余的横线也可以：

| ID | A | B | C |
|-|-|-|-|
| 1 | Option1 | Option1 | Option1 |
| 2 | Option2 | Option2 | Option2 |
| 3 | Option3 | Option3 | Option3 |
```
