# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="so-green-it",
    version="0.5",
    packages=['sogreenit'],
    include_package_data=True,
    install_requires=[
        'flask>=0.12.2',
        'selenium',
        'browsermob-proxy>=0.8.0',
        'psutil>=5.4.1',
        'jsonschema>=2.6.0',
        'psycopg2>=2.7',
        'mysqlclient>=1.3'
    ],
    author='Romain Failla',
    author_email='rigbuntu@gmail.com',
    license='MIT',
    keywords='green it best practises',
    url='https://github.com/so-green-team/so-green-it'
)
