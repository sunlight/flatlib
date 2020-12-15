"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)

"""

from setuptools import setup
from setuptools import find_packages


setup(
    # Project
    name = 'riftlib',
    version = '0.3.1-dev',

    # Sources
    packages = find_packages(),
    package_data = {
        'riftlib': [
            'resources/README.md',
            'resources/swefiles/*'
        ],
    },

    # Dependencies
    install_requires = ['pyswisseph==2.00.00-2'],

    # Metadata
    description = 'Fork of Flatlib, a Python library for Traditional Astrology',
    url = 'https://github.com/theriftlab/riftlib',
    keywords = ['Astrology', 'Traditional Astrology'],
    license = 'MIT',

    # Authoring
    author = 'Robert Davies',
    author_email = 'robert@theriftlab.com',

    # Classifiers
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
