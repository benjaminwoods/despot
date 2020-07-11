"""
Despot setup.

Requires Python >= 3.7.
"""

import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 7):
    raise NotImplementedError('Requires Python >= 3.7.')

setup(
    name="despot",
    version="dev",

    package_dir={'':'src'},
    packages=find_packages(where='src'),
    install_requires=['radon>=4.1.0',
                      'pycodestyle>=2.5.0',
                      'pyyaml>=5.3.1'],
    entry_points={
        'console_scripts': ['despot=despot.__main__:main'],
    },
    
    # Metadata
    author="Benjamin Woods",
    author_email="ben@bjqw.me",
    project_urls={},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ]
)