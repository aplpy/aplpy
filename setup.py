#!/usr/bin/env python

from distutils.core import setup

try:  # Python 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:  # Python 2.x
    from distutils.command.build_py import build_py

setup(name='APLpy',
      version='0.9.7',
      description='The Astronomical Plotting Library in Python',
      author='Thomas Robitaille and Eli Bressert',
      author_email='thomas.robitaille@gmail.com, elibre@users.sourceforge.net',
      license='MIT',
      url='http://aplpy.github.com/',
      download_url='https://github.com/downloads/aplpy/aplpy/APLpy-0.9.7.tar.gz',
      packages=['aplpy'],
      provides=['aplpy'],
      requires=['pywcs', 'pyfits', 'numpy', 'matplotlib'],
      cmdclass={'build_py': build_py},
      keywords=['Scientific/Engineering'],
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: MIT License",
                  ],
     )
