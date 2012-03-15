#!/usr/bin/env python

import os
import sys
import subprocess

from distutils.core import setup, Command

try:  # Python 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:  # Python 2.x
    from distutils.command.build_py import build_py


class PyTest(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, 'runtests.py', '-q'])
        raise SystemExit(errno)

setup(name='APLpy',
      version='0.9.8',
      description='The Astronomical Plotting Library in Python',
      author='Thomas Robitaille and Eli Bressert',
      author_email='thomas.robitaille@gmail.com, elibre@users.sourceforge.net',
      license='MIT',
      url='http://aplpy.github.com/',
      packages=['aplpy'],
      provides=['aplpy'],
      requires=['pywcs', 'pyfits', 'numpy', 'matplotlib'],
      cmdclass={'build_py': build_py, 'test': PyTest},
      keywords=['Scientific/Engineering'],
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: MIT License",
                  ],
     )
