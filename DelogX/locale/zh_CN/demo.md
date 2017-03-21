# 示例页面

本页面的作用是向用户展示 Markdown 的实际效果，您可以用文本编辑器打开本页面的文件 `demo.md` 并查看其中的源代码。

## 标题 Header

# 一级标题 H1

## 二级标题 H2

### 三级标题 H3

#### 四级标题 H4

##### 五级标题 H5

###### 六级标题 H6

## 正文 Paragraph

我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 我能够吞下玻璃而不伤身体。The quick brown fox jumps over the lazy dog. 

### 强调 Emphasis

强调包括**加重强调**与*强调*。

混合起来的***特殊强调***也不错。

### 删除线 Strike

~~一段过期了的文字。~~

### 引用 Quotes

> Markdown 是一种轻量级标记语言，创始人为约翰·格鲁伯（John Gruber）。
> 它允许人们“使用易读易写的纯文本格式编写文档，然后转换成有效的 XHTML（或者 HTML）文档”。
> 这种语言吸收了很多在电子邮件中已有的纯文本标记的特性。

也可以嵌入引用

> 另一个引用
> > Markdown 是一种轻量级标记语言，创始人为约翰·格鲁伯（John Gruber）。
> > 它允许人们“使用易读易写的纯文本格式编写文档，然后转换成有效的 XHTML（或者 HTML）文档”。
> > 这种语言吸收了很多在电子邮件中已有的纯文本标记的特性。
>
> 非常容易！

也可以嵌入代码

> 一个 Python 循环
>
>     for i in range(5):
>         print(i)
>

### 列表 Lists

#### 无序列表

* 一个无序列表项
* 另一个无序列表项
* 以及又一个

#### 有序列表

1. 这是一个有序列表
2. 我排在第二位
3. 我是说楼上各位都是垃圾

#### 分行的无序列表

* 无序列表可以  
  分成多行  
  以及更多行
* 就像我现在做的  
  这样

#### 分行的有序列表

1. 有序列表也  
   可以分行
2. 这是另一项  
   还是再分一行吧  
   > 甚至加入一行引用

## 代码 Code

代码可以直接写在正文中，例如 `echo -e "\033[32mHello"` 或者 `lolololol`，也可以写成代码块的形式，例如

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

## 链接 Links

行内式链接：[GitHub](https://github.com/)

参考式链接：[Wikipedia][1]

电子邮件：<email@example.com>

[1]: https://www.wikipedia.org/

## 图片 Images

图片与链接的语法非常接近。

![Flask](http://flask.pocoo.org/static/logo.png "一张图片")

## 水平线 Horizontal Lines

***

---

* * *

## 表格 Tables

| 序号 | 一 | 二 | 三 |
|-|-|-|-|
| 1 | 选项1 | 选项1 | 选项1 |
| 2 | 选项2 | 选项2 | 选项2 |
| 3 | 选项3 | 选项3 | 选项3 |
