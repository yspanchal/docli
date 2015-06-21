# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='docli',
    version='1.0',

    description='Digital Ocean command line interface',
    long_description=long_description,

    author='Yogesh Panchal',
    author_email='yspanchal@gmail.com',

    url='https://github.com/yspanchal/docli',
    download_url='https://github.com/yspanchal/docli/tarball/master',

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'tabulate',
    ],
    entry_points='''
        [console_scripts]
        docli=docli.main:docli
    ''',
#    classifiers=[
#        'License :: OSI Approved :: Apache Software License',
#        'Programming Language :: Python',
#    ],
)
