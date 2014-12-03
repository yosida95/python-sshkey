# -*- coding: utf-8 -*-

import os

from setuptools import (
    find_packages,
    setup,
)

here = os.path.dirname(__file__)
requires = []
tests_require = []

try:
    import enum
except ImportError:
    requires.append('enum34')
else:
    del enum


def _read(name):
    try:
        return open(os.path.join(here, name)).read()
    except:
        return ""
readme = _read("README.rst")
license = _read("LICENSE")

setup(
    name='sshkey',
    version='0.0.1',
    test_suite='sshkey',
    author='Kohei YOSHIDA',
    author_email='license@yosida95.com',
    description='SSH key management utility',
    long_description=readme,
    license=license,
    url='https://github.com/yosida95/python-sshkey',
    packages=find_packages(),
    install_requires=requires,
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
