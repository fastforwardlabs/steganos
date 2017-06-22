#!/usr/bin/env python

from setuptools import setup
from steganos import __version__


setup(
    name='steganos',
    version=__version__,
    description='Hide messages inside text',
    author='Noam Finkelstein, Micha Gorelick',
    url='http://github.com/fastforwardlabs/steganos',
    download_url='https://github.com/fastforwardlabs/steganos/tarball/master',
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",

    packages=['steganos'],
)
