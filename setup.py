#!/usr/bin/env python
from setuptools import setup


setup(
    name="python-ips",
    version='1.7',
    description="Python IPS patcher.",
    author="Devon Meunier",
    license="MIT License",
    author_email="devon.meunier@utoronto.ca",
    py_modules=['ips'],
    install_requires=[
        'docopt',
    ],
    entry_points={
        "console_scripts": [
            "ips = ips:main"
        ]
    },
)
