# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='lirc_cli_py',
    version='0.0.1',
    description='LIRC client package for python',
    long_description=readme,
    author='Takuma Tanaka',
    author_email='takuborn1980@gmail.com',
    url='https://github.com/takuborn/lirc-cli-py',
    license='Apache License 2.0',
    packages=find_packages(exclude=('tests', 'docs'))
)

