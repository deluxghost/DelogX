# Demo Page

This page is used for showing the actual style of Markdown, you can open `demo.md` by a text editor and check the source code.

## Header

# Header H1

## Header H2

### Header H3

#### Header H4

##### Header H5

###### Header H6

## Paragraph

The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. 

### Emphasis

Emphasis include **strong emphasis** and *emphasis*.

The combined ***special emphasis*** is also OK.

### Strike

~~Something expired.~~

### Quotes

> Markdown is a lightweight markup language with plain text formatting syntax.
> It's designed so that it can be converted to HTML and many other formats
> using a tool by the same name. Markdown is often used to format readme files,
> for writing messages in online discussion forums, and to create rich text
> using a plain text editor. 

and nested quotes:

> Another quote
> > Markdown is a lightweight markup language with plain text formatting syntax.
> > It's designed so that it can be converted to HTML and many other formats
> > using a tool by the same name.
>
> That is easy!

even some nested code:

> A loop in Python
>
>     for i in range(5):
>         print(i)
>

### Lists

#### Unordered Lists

* An item in unordered list.
* Another item in unordered list.
* And another.

#### Ordered Lists

1. This is an ordered list.
2. And the second item.
3. And more.

#### Wrapped Unordered Lists

* Unordered lists  
  can be written in  
  multiple lines.
* Just like  
  what I am doing.

#### Wrapped Ordered Lists

1. And same as  
   ordered lists
2. Another item  
   and another line  
   > even a quote

## Code

You can write code in a line, such as `echo -e "\033[32mHello"` or `lolololol`, or in a code block:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

## Links

Inline link: [GitHub](https://github.com/)

Reference link: [Wikipedia][1]

E-mail: <email@example.com>

[1]: https://www.wikipedia.org/

## Images

The syntax of images is similar to links.

![Flask](http://flask.pocoo.org/static/logo.png "a picture")

## Horizontal Lines

***

---

* * *

## Tables

| Index | A | B | C |
|-|-|-|-|
| 1 | Item1 | Item1 | Item1 |
| 2 | Item2 | Item2 | Item2 |
| 3 | Item3 | Item3 | Item3 |
