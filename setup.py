# python ltree setup module

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="ltree",
    version="0.0.1",
    author="Daniele Varrazzo",
    author_email="daniele.varrazzo@gmail.com",
    description="Python wrapper for the PostgreSQL ltree data type",
    license="BSD",
    keywords="ltree tree database",
    url="https://github.com/dvarrazzo/py-ltree",
    packages=['ltree'],
    long_description=read('README.rst'),
    classifiers=[l.strip() for l in """
        Development Status :: 3 - Alpha
        Programming Language :: Python :: 2.7
        Topic :: Utilities
        License :: OSI Approved :: BSD License
        """.splitlines() if l],
)
