# Hello, DelogX

Welcome to DelogX. This is a lite, dynamic and Markdown based blog framework, written in Python and powered by Flask.

## Getting Started

DelogX manage posts and pages in file system，every post or page is referred to a regular Markdown file. Conversely, every valid Markdown file can be considered as a post or page.

### Metadata

Every `.md` file itself contain all metadata of the post or page:

* Title: If the first line of the file is a level 1 header in Markdown syntax, this header is the title of the post or page, otherwise the title is same as the url.
* Modification time: Just the modification time of the file. Pages have no modification time.
* Main body: The texts exclude the title.

### Hidden Content

In UNIX-like systems, if the name of a file starts with a dot (`.`), this file is a hidden file. In DelogX, similar `.md` files will be hidden too — a post will not be shown in a post list, a page will not be shown in the navbar. But you can access these content by the valid URL.

### Order

All posts are in reverse chronological order, and the newest post is at the top.

Pages are usually sorted automatically by Python, however, you can specify the order by adding an integer sub-extension, such as `hello-world.1.md` and `demo.2.md`. Pages with a specific order have higher sort priority than others.

### URL

Every post or page has an unique URL. Each URL has two parts: prefix and file name. The prefix is like `/post`, you can change them in the config file.

The file name part is the file name of the post or page, but exclude the extension name (`.md`), the dot prefix (`.`) and the specific order (such as `.1` and `.2`), because these are metadata. Then, this URL will be urlencoded.

For example, the URL of page `.hidden-page.2.md` **may** be `/page/hidden-page`, and `http://yourblog.com/page/hidden-page` with a domain.

### Markdown

DelogX support most standard Markdown syntax (difference see [python-markdown documentation]{: target="_blank"}), and following Extra syntax:

* Tables
* Strike
* Fenced Code Block
* Attributes List

You can find a very simple "Markdown Getting Started" in this post.

[python-markdown documentation]: http://pythonhosted.org/Markdown/#differences

### Code Highlighting

DelogX use [highlight.js]{: target="_blank"} as the code highlighting engine. Usually, it can identify code blocks and programming language automatically, but with fenced code block, you can specify a language:

````markdown
```python
from __future__ import print_function
print("Hello Python3!")
```
````

DelogX choose the GitHub color scheme as default, you can also customize your languages and color schemes at the highlight.js website.

[highlight.js]: https://highlightjs.org/

### Static Files

DelogX stores static files such as CSS, JS or images in `static` directory, you can sccess them by the link `http://yourblog.com/static/filename`.

### Config

The config of DelogX is `config.json`, you can see the documentation for more information.

### More

More resources of DelogX:

* Source code: <https://github.com/deluxghost/DelogX>
* Wiki documentation: <https://github.com/deluxghost/DelogX/wiki>

## Markdown Getting Started

### HTML Compatibility

Markdown is designed to compatible with HTML, therefore you can type HTML in a Markdown file directly.

### Headers

```markdown
# H1 Header
## H2 Header
###### H6 Header

# Another H1 Header #
## Another H2 Header ##
#### H4 Header ####

Another type of H1
==================

Another type of H2
------------------
```

### Emphasis

```markdown
Emphasis include **strong emphasis** and *normal emphasis*.
Usually, The former is shown as bold, and the latter is shown as italic.
You can combine them both as ***special emphasis***.
```

### Lists

```markdown
* Unordered Item
* Unordered Item
* Unordered Item
* Unordered Item
```

```markdown
1. Ordered Item
2. Ordered Item
3. Ordered Item
4. Ordered Item
```

### Quotes

```markdown
> Quote starts with a greater than symbol.
> You can write one in the beginning of each line.
>
> > Quotes can be nested
> > like this.
```

### Code

```markdown
You can write inline code in a pair of backtick, such as `import urllib`.
```

If you want a code block, just copy and paste the code, and add an indentation level:

```markdown
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
```

DelogX also support fenced code block, which can specify the programming language.

````markdown
```python
from __future__ import print_function
print("Hello Python3!")
```
````

### Links

```markdown
Inline link: [GitHub](http://github.com/)

Reference link: [Wikipedia][1]

[1]: https://www.wikipedia.org/
```

### Images

```markdown
![MyPhoto](/static/images/photo.png "a picture")
```

### Horizontal Lines

```markdown
***

---

* * *
```

### Tables

```markdown
| ID   | A       | B       | C       |
|------|---------|---------|---------|
| 1    | Option1 | Option1 | Option1 |
| 2    | Option2 | Option2 | Option2 |
| 3    | Option3 | Option3 | Option3 |

or remove needless spaces and dashes:

| ID | A | B | C |
|-|-|-|-|
| 1 | Option1 | Option1 | Option1 |
| 2 | Option2 | Option2 | Option2 |
| 3 | Option3 | Option3 | Option3 |
```
