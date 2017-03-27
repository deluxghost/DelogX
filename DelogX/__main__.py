# -*- coding: utf-8 -*-
'''The command line manager of DelogX.'''
from __future__ import print_function, unicode_literals

import argparse
import os
import shutil
import sys


def copytree(src, dst, blacklist=None):
    '''Copy all files in src to dst.'''
    if not blacklist:
        blacklist = list()
    blacklist.extend(['__pycache__', 'deploy'])
    basename = os.path.basename(src)
    if basename in blacklist:
        return
    if not os.path.exists(dst):
        print(' Creating {0}'.format(dst))
        os.makedirs(dst)
    for item in os.listdir(src):
        sfile = os.path.join(src, item)
        dfile = os.path.join(dst, item)
        ext = os.path.splitext(os.path.basename(sfile))[1]
        if os.path.isdir(sfile):
            copytree(sfile, dfile)
        elif ext != '.pyc':
            print(' Copying {0}'.format(dfile))
            shutil.copyfile(sfile, dfile)


def init(init_args):
    '''Create a new blog application.'''
    module_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(module_path))
    from DelogX.utils.compat import Compat
    from DelogX.utils.config import Config
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
        print('Choose Language({0}):'.format(','.join(locales)))
        if Compat.version() == 2:
            locale = raw_input('> ')
        else:
            locale = input('> ')
    copytree(defaults, cwd)
    print('Creating deployment scripts')
    deploy_dir = os.path.join(defaults, 'deploy')
    deploys = list()
    if init_args.apache:
        deploys.append('apache2.wsgi')
    if init_args.nginx:
        deploys.append('uwsgi.py')
    if init_args.tornado:
        deploys.append('tornado_wsgi.py')
    if init_args.gevent:
        deploys.append('gevent_wsgi.py')
    for filename in deploys:
        deploy = os.path.join(deploy_dir, filename)
        deploy_dst = os.path.join(cwd, filename)
        print(' Creating {0}'.format(deploy_dst))
        shutil.copyfile(deploy, deploy_dst)
    print('Setting language', locale)
    config = Config(os.path.join(cwd, 'config.json'))
    config.let('local.locale', locale)
    config.save()
    print('Creating demo post')
    post_dir = os.path.join(cwd, 'posts')
    print(' Creating {0}'.format(post_dir))
    if os.path.isfile(post_dir):
        os.remove(post_dir)
    if not os.path.exists(post_dir):
        os.makedirs(post_dir)
    post_path = os.path.join(post_dir, 'hello-delogx.md')
    print(' Copying {0}'.format(post_path))
    shutil.copyfile(
        os.path.join(locale_dir, locale, 'hello-delogx.md'), post_path)
    print('Creating demo page')
    page_dir = os.path.join(cwd, 'pages')
    print(' Creating {0}'.format(page_dir))
    if os.path.isfile(page_dir):
        os.remove(page_dir)
    if not os.path.exists(page_dir):
        os.makedirs(page_dir)
    page_path = os.path.join(page_dir, 'demo.md')
    print(' Copying {0}'.format(page_path))
    shutil.copyfile(
        os.path.join(locale_dir, locale, 'demo.md'), page_path)


def main():
    '''Main function of the manager.'''
    module_path = os.path.dirname(os.path.realpath(__file__))
    ver = open(os.path.join(module_path, 'VERSION'))
    VERSION = ver.read().strip()
    ver.close()
    parser = argparse.ArgumentParser(
        description='Manage a DelogX blog application.')
    parser.add_argument(
        '-V', '--version', action='version',
        version='DelogX v{0}'.format(VERSION))
    subparsers = parser.add_subparsers(
        title='sub-commands', description='valid sub-commands',
        metavar='sub-command', help='description')
    init_parser = subparsers.add_parser(
        'init', help='create DelogX blog application at current directory')
    init_parser.add_argument(
        '-f', '--force', help='force creation of the blog',
        action='store_true')
    init_parser.add_argument(
        '--mod-wsgi', '--apache2',
        dest='apache', help='deploy on Apache 2 (mod_wsgi)',
        action='store_true')
    init_parser.add_argument(
        '--uwsgi', '--nginx',
        dest='nginx', help='deploy on uWSGI or Nginx',
        action='store_true')
    init_parser.add_argument(
        '--tornado', help='deploy on Tornado',
        action='store_true')
    init_parser.add_argument(
        '--gevent', help='deploy on Gevent',
        action='store_true')
    init_parser.set_defaults(func=init)
    if len(sys.argv) <= 1:
        parser.print_help()
        parser.exit(0)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
