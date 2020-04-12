# -*- coding: utf-8 -*-

import os

from setuptools import (
    find_packages,
    setup,
)

here = os.path.dirname(__file__)


def _read(name):
    try:
        return open(os.path.join(here, name)).read()
    except BaseException:
        return ""


readme = _read("README.rst")

setup(
    name='sshkey',
    version='0.1.0',
    description='SSH key management utility',
    long_description=readme,
    license='BSD-3-Clause',
    url='https://github.com/yosida95/python-sshkey',

    author='Kohei YOSHIDA',
    author_email='kohei@yosida95.com',

    packages=find_packages(),
    test_suite='tests',
    install_requires=[],
    tests_require=[],
    python_requires='>= 3.6',

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
