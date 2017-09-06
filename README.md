# DelogX

[![GitHub license](https://img.shields.io/badge/license-Apache%202-blue.svg?style=flat-square)](https://raw.githubusercontent.com/deluxghost/DelogX/master/LICENSE)
[![Travis](https://img.shields.io/travis/deluxghost/DelogX.svg?style=flat-square)](https://travis-ci.org/deluxghost/DelogX/)
[![PyPI](https://img.shields.io/pypi/v/DelogX.svg?style=flat-square)](https://pypi.python.org/pypi/DelogX)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bhttps%3A%2F%2Fgithub.com%2Fdeluxghost%2FDelogX.svg?type=small)](https://app.fossa.io/projects/git%2Bhttps%3A%2F%2Fgithub.com%2Fdeluxghost%2FDelogX?ref=badge_small)

DelogX is a lite, tiny, micro and dynamic Markdown based blog framework, written in Python and powered by Flask.

## Features

* Small, little, lite, tiny and micro.
* Easy to install and deploy.
* Write and publish with Markdown.
* Manage articles in one directory.
* No database and admin panel, everything is file.
* Compatible with Windows, macOS, Linux and even WSL or Android.
* Configure everything, including localization.
* Customize your blog with plugins and themes.
* Deploy on Apache, Nginx, standalone WSGI containers or just built-in server.

## Installation

Install DelogX with pip:

```shell
pip3 install DelogX
```

You may need root permissions:

```shell
sudo pip3 install DelogX
```

## Getting Started

After installing, Create a new directory to store your blog application, and enter it.

```shell
mkdir my_blog
cd my_blog
```

Then run command:

```shell
delogx init
```

and follow the instructions to initialize.

When the process is complete, run:

```shell
python3 debug.py
```

and visit "http://127.0.0.1:8000" to test if everything is ok.

If everything is ok, you can read the [documentation] to learn about how to config and how to add posts.

[documentation]: https://github.com/deluxghost/DelogX/wiki
