#!/usr/bin/env python
"""Setup `databricks_utils` package"""
from setuptools import setup, find_packages

setup(
    name='databricks-utils',
    version='0.0.2',
    url='https://github.com/e2fyi/databricks-utils',
    license='Apache License 2.0',
    author='William Teo',
    author_email='eterna2@hotmail.com',
    description='Ease-of-use utility tools for databricks notebooks.',
    packages=find_packages(include=['databricks_utils*'],
                           exclude=["notebooks*", "docs*", "*.sh"]),
    include_package_data=False,
    install_requires=[
        "pandas~=0.19.0",
        "pyspark~=2.3.0",
        "ipython~=6.0.0"
    ]
)
