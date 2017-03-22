# -*- coding: utf-8 -*-
'''The command line manager of DelogX.'''
from __future__ import print_function, unicode_literals

import argparse
import os
import shutil
import sys

VERSION = '1.0.7'


def copytree(src, dst):
    '''Copy all files in src to dst.'''
    basename = os.path.basename(src)
    if basename == '__pycache__':
        return
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        sfile = os.path.join(src, item)
        dfile = os.path.join(dst, item)
        ext = os.path.splitext(os.path.basename(sfile))[1]
        if os.path.isdir(sfile):
            copytree(sfile, dfile)
        elif ext != '.pyc':
            shutil.copyfile(sfile, dfile)


def init(init_args):
    '''Create a new blog application.'''
    module_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(module_path))
    from DelogX.entity.config import Config
    from DelogX.utils.compat import Compat
    cwd = os.getcwd()
    defaults = os.path.join(module_path, 'defaults')
    if os.listdir(cwd) and not init_args.force:
        print(
            '''The current directory is not empty,\n'''
            '''use `delogx init --force' if you want to overwrite.'''
        )
        return
    locale_dir = os.path.join(module_path, 'locale')
    locales = list()
    for lang in os.listdir(locale_dir):
        if os.path.isdir(os.path.join(locale_dir, lang)):
            locales.append(lang)
    locale = ''
    while locale not in locales:
        print('Choose Language({0}):\n> '.format(','.join(locales)), end='')
        if Compat.version() == 2:
            locale = raw_input()
        else:
            locale = input()
    copytree(defaults, cwd)
    config = Config(os.path.join(cwd, 'config.json'))
    config.let('local.locale', locale)
    config.save()
    post_dir = os.path.join(cwd, 'posts')
    page_dir = os.path.join(cwd, 'pages')
    if os.path.isfile(post_dir):
        os.remove(post_dir)
    if os.path.isfile(page_dir):
        os.remove(page_dir)
    if not os.path.exists(post_dir):
        os.makedirs(post_dir)
    if not os.path.exists(page_dir):
        os.makedirs(page_dir)
    shutil.copyfile(
        os.path.join(locale_dir, locale, 'hello-delogx.md'),
        os.path.join(post_dir, 'hello-delogx.md'))
    shutil.copyfile(
        os.path.join(locale_dir, locale, 'demo.md'),
        os.path.join(page_dir, 'demo.md'))


def main():
    '''Main function of the manager.'''
    parser = argparse.ArgumentParser(
        description='Manage a DelogX blog application.')
    parser.add_argument(
        '-ver', '--version', action='version',
        version='DelogX v{0}'.format(VERSION))
    subparsers = parser.add_subparsers(
        title='sub-commands', description='valid sub-commands',
        metavar='sub-command', help='description')
    init_parser = subparsers.add_parser(
        'init', help='create DelogX blog application at current directory')
    init_parser.add_argument(
        '-f', '--force', help='force creation of the blog',
        action='store_true')
    init_parser.set_defaults(func=init)
    args = parser.parse_args()
    if not vars(args):
        parser.print_help()
        parser.exit(0)
    args.func(args)


if __name__ == '__main__':
    main()
