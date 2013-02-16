#!/usr/bin/env python
from setuptools import setup


setup(
    name="python-ips",
    version='2.0',
    description="Python IPS patcher.",
    author="Devon Meunier",
    license="MIT License",
    author_email="devon@ajah.ca",
    py_modules=['ips'],
    install_requires=[
        'docopt',
    ],
    entry_points={
        "console_scripts": [
            "ips = python-ips:main"
        ]
    },
)
