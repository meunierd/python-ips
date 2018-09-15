#!/usr/bin/env python
from setuptools import setup


setup(
    name="python-ips",
    version='2.1',
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
            "python-ips = ips:main"
        ]
    },
)
