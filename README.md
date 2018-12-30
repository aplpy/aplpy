[![Build Status](https://travis-ci.org/aplpy/aplpy.svg?branch=master)](https://travis-ci.org/aplpy/aplpy)
[![CircleCI](https://circleci.com/gh/aplpy/aplpy/tree/master.svg?style=svg)](https://circleci.com/gh/aplpy/aplpy/tree/master)
[![codecov](https://codecov.io/gh/aplpy/aplpy/branch/master/graph/badge.svg)](https://codecov.io/gh/aplpy/aplpy)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](https://aplpy.readthedocs.io/en/latest/)


About
-----

APLpy (the Astronomical Plotting Library in Python) is a
Python module aimed at producing publication-quality plots
of astronomical imaging data in FITS format.

PyPI: https://pypi.python.org/pypi/APLpy

Website: http://aplpy.github.io

Documentation: http://aplpy.readthedocs.io

APLpy is released under an MIT open-source license.

Installing
----------

The following dependencies are required:

* [Numpy](http://www.numpy.org) 1.11 or later
* [Matplotlib](http://www.matplotlib.org) 2.0 or later
* [Astropy](http://www.astropy.org) 3.1 or later
* [reproject](http://reproject.readthedocs.org) 0.4 or later

and the following are optional:

* [PyAVM](http://astrofrog.github.io/pyavm/) 0.9.4 or later
* [pyregion](http://pyregion.readthedocs.org/) 2.0 or later
* [pillow](https://pypi.org/project/Pillow/) 4.0 or later
* [scikit-image](https://pypi.org/project/scikit-image/) 0.14 or later

You can install APLpy with:

    pip install aplpy

If you want to install all optional dependencies, you can do:

    pip install aplpy[all]
