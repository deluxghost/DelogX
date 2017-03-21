# DelogX

[![GitHub license](https://img.shields.io/badge/license-Apache%202-blue.svg?style=flat-square)](https://raw.githubusercontent.com/deluxghost/DelogX/master/LICENSE)
[![Travis](https://img.shields.io/travis/rust-lang/rust.svg?style=flat-square)](https://travis-ci.org/deluxghost/DelogX/)

DelogX is a lite, tiny, micro and dynamic Markdown based blog framework, written in Python and powered by Flask.

## Features

* Lite, tiny, micro, little and small.
* Easy to install and deploy.
* Write and publish with Markdown.
* Manage articles in one directory.
* No database and admin panel, everything is file.
* Compatible with Windows, OS X, Linux and even WSL or Android.
* Compatible with Python 2.7/3.3+.
* Configure everything, including localization.
* Customize your blog with plugins and themes.
* Deploy on Apache, Nginx or just built-in server.

## Installation

Install DelogX with pip:

```shell
pip install DelogX
```

You may need root permissions:

```shell
sudo pip install DelogX
```

## Getting Started

After installing, Create a new directory to store your blog application, and enter it.

```shell
mkdir my_blog
cd my_blog
```

Then run command:

```delogx init```

and follow the instructions to initialize.

When the process is complete, run:

```python debug.py```

and visit "http://127.0.0.1:8000" to test if everything is ok.

If everything is ok, you can read the [documentation] to learn about how to config and how to add posts.

[documentation]: https://github.com/deluxghost/DelogX/wiki
