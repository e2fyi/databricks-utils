#!/usr/bin/env python
"""Setup `databricks_utils` package"""
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    README = fh.read()

setup(
    name='databricks-utils',
    version='0.0.7',
    url='https://github.com/e2fyi/databricks-utils',
    license='Apache License 2.0',
    author='William Teo',
    author_email='eterna2@hotmail.com',
    description='Ease-of-use utility tools for databricks notebooks.',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['databricks_utils*'],
                           exclude=["notebooks*", "docs*", "*.sh"]),
    include_package_data=False,
    install_requires=[]
)
