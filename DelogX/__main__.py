# -*- coding: utf-8 -*-
'''The command line manager of DelogX.'''
import argparse
import os
import platform
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
        locale = input('> ')
    copytree(defaults, cwd)
    print('Setting language', locale)
    #  TODO: Update config entries
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


def deploy(deploy_args):
    '''Create deployment files.'''
    module_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(module_path))
    cwd = os.getcwd()
    defaults = os.path.join(module_path, 'defaults')
    deploy_dir = os.path.join(defaults, 'deploy')
    deploys = list()
    if deploy_args.apache:
        deploys.append('mod_wsgi.wsgi')
        if platform.system() == 'Windows':
            deploys.append('apache2_win.conf')
        else:
            deploys.append('apache2.conf')
    if deploy_args.wsgi:
        deploys.append('uwsgi.py')
    if deploy_args.nginx:
        deploys.append('nginx.conf')
    if not deploys:
        print(
            '''You haven't specific any deployment method,\n'''
            '''use `delogx deploy --help' to get further information.'''
        )
        return
    srv_names = ''
    srv_appname = ''
    srv_proxy_pass = ''
    srv_user = ''
    while not srv_names:
        print('Your server names (split by space):')
        srv_names = input('> ')
    if platform.system() != 'Windows':
        import getpass
        srv_user = getpass.getuser()
        if deploy_args.apache:
            while not srv_appname:
                print('Your application names for mod_wsgi:')
                srv_appname = input('> ')
    srv_path = cwd
    if deploy_args.nginx:
        while not srv_proxy_pass:
            print('Your proxy pass address (e.g. http://127.0.0.1:8000):')
            srv_proxy_pass = input('> ')
    srv_a2_name = ''
    srv_a2_alias = ''
    if srv_names.split():
        srv_a2_name = 'ServerName ' + srv_names.split()[0]
    if len(srv_names.split()) > 1:
        srv_a2_alias = 'ServerAlias ' + ' '.join(srv_names.split()[1:])
    print('Applying variables')
    replacements = {
        '{{:server_name:}}': srv_names,
        '{{:a2server_name:}}': srv_a2_name,
        '{{:a2server_alias:}}': srv_a2_alias,
        '{{:application:}}': srv_appname,
        '{{:path:}}': srv_path,
        '{{:pathsep:}}': os.path.sep,
        '{{:user:}}': srv_user,
        '{{:group:}}': srv_user,
        '{{:proxy_pass:}}': srv_proxy_pass
    }
    print('Creating deployment files')
    for filename in deploys:
        deploy_src = os.path.join(deploy_dir, filename)
        deploy_dst = os.path.join(cwd, filename)
        print(' Creating {0}'.format(deploy_dst))
        with open(deploy_src) as infile, open(deploy_dst, 'w') as outfile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                outfile.write(line)


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
    deploy_parser = subparsers.add_parser(
        'deploy', help='create DelogX blog deployment files')
    init_parser.add_argument(
        '-f', '--force', help='force creation of the blog',
        action='store_true')
    deploy_parser.add_argument(
        '--mod-wsgi', '--apache2',
        dest='apache', help='deploy on Apache 2 (mod_wsgi)',
        action='store_true')
    deploy_parser.add_argument(
        '--wsgi', '--uwsgi',
        dest='wsgi', help='deploy in a WSGI container',
        action='store_true')
    deploy_parser.add_argument(
        '--nginx', dest='nginx', help='deploy behind Nginx proxy',
        action='store_true')
    init_parser.set_defaults(func=init)
    deploy_parser.set_defaults(func=deploy)
    if len(sys.argv) <= 1:
        parser.print_help()
        parser.exit(0)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
