# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='docli',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'tabulate',
    ],
    entry_points='''
        [console_scripts]
        docli=docli:docli
    ''',
)