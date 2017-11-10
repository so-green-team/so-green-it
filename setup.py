# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="so-green-it",
    version="0.1",
    packages=['sogreenit'],
    include_package_data=True,
    install_requires=[
        'flask>=0.12.2',
        'selenium>=3.7.0'
    ],
    author='Romain Failla',
    author_email='rigbuntu@gmail.com',
    license='MIT',
    keywords='green it best practises',
    url='https://github.com/so-green-team/so-green-it'
)
