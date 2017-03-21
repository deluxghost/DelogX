DelogX is a lite, tiny, micro and dynamic Markdown based blog framework,
written in Python and powered by Flask.

Features
--------

-  Lite, tiny, micro, little and small.
-  Easy to install and deploy.
-  Write and publish with Markdown.
-  Manage articles in one directory.
-  No database and admin panel, everything is file.
-  Compatible with Windows, OS X, Linux and even WSL or Android.
-  Compatible with Python 2.7/3.3+.
-  Configure everything, including localization.
-  Customize your blog with plugins and themes.
-  Deploy on Apache, Nginx or just built-in server.

Installation
------------

Install DelogX with pip:

.. code:: shell

    pip install DelogX

You may need root permissions:

.. code:: shell

    sudo pip install DelogX

Getting Started
---------------

After installing, Create a new directory to store your blog application,
and enter it.

.. code:: shell

    mkdir my_blog
    cd my_blog

Then run command:

.. code:: shell

    delogx init

and follow the instructions to initialize.

When the process is complete, run:

.. code:: shell

    python debug.py

and visit "http://127.0.0.1:8000" to test if everything is ok.

If everything is ok, you can read the
`documentation <https://github.com/deluxghost/DelogX/wiki>`__ to learn
about how to config and how to add posts.
