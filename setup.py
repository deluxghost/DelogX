# -*- coding: utf-8 -*-
'''Setup script of DelogX.'''
import os

from setuptools import setup, find_packages

VERSION = '1.0.7'


def find_package_data():
    '''Get data files of DelogX.'''
    cwd = os.getcwd()
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'DelogX')
    data_list = list()
    os.chdir(path)
    data_list.append('DESCRIPTION.rst')
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
setup(
    name='DelogX',
    version=VERSION,
    packages=find_packages(),
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
    license='Apache 2',
    keywords='flask markdown blog framework',
    url='http://delogx.deluxghost.me/'
)
