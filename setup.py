# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="so-green-it",
    version="0.1",
    scripts=['app.py'],
    install_requires=[
        'Flask>=0.12.2'
    ],
    author='Romain Failla',
    author_email='rigbuntu@gmail.com',
    license='MIT',
    keywords='green it best practises',
    url='https://github.com/so-green-team/so-green-it'
)

