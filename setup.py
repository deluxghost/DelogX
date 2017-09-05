# -*- coding: utf-8 -*-
'''Setup script of DelogX.'''
import os

from setuptools import setup, find_packages


def find_package_data():
    '''Get data files of DelogX.'''
    cwd = os.getcwd()
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'DelogX')
    data_list = list()
    os.chdir(path)
    data_list.append('DESCRIPTION.rst')
    data_list.append('VERSION')
    for root, dirs, files in os.walk('defaults'):
        for filename in files:
            data_list.append(os.path.join(root, filename))
    for root, dirs, files in os.walk('locale'):
        for filename in files:
            data_list.append(os.path.join(root, filename))
    os.chdir(cwd)
    return data_list


desc = open(os.path.join('DelogX', 'DESCRIPTION.rst'))
DESCRIPTION = desc.read()
desc.close()
ver = open(os.path.join('DelogX', 'VERSION'))
VERSION = ver.read().strip()
ver.close()

setup(
    name='DelogX',
    version=VERSION,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ],
    install_requires=[
        'Flask>=0.11',
        'watchdog',
        'markdown'
    ],
    package_data={
        'DelogX': find_package_data()
    },
    entry_points={
        'console_scripts': [
            'delogx = DelogX.__main__:main'
        ]
    },
    author='deluxghost',
    author_email='deluxghost@gmail.com',
    description='Yet another Markdown based blog',
    long_description=DESCRIPTION,
    license='Apache License 2.0',
    keywords='flask markdown blog framework',
    url='http://delogx.deluxghost.me/'
)
