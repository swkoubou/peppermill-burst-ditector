#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup
setup(name='burstditector',
      version='0.1.0',
      py_modules=['burstditector'],
      install_requires=[
          "numpy",
          "scipy",
      ]
      )
