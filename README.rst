|Build Status| |CircleCI| |codecov| |Documentation Status|

About
-----

APLpy (the Astronomical Plotting Library in Python) is a Python module
aimed at producing publication-quality plots of astronomical imaging
data in FITS format.

PyPI: https://pypi.python.org/pypi/APLpy

Website: http://aplpy.github.io

Documentation: http://aplpy.readthedocs.io

APLpy is released under an MIT open-source license.

Installing
----------

The following dependencies are required:

-  `Numpy <http://www.numpy.org>`__ 1.11 or later
-  `Matplotlib <http://www.matplotlib.org>`__ 2.0 or later
-  `Astropy <http://www.astropy.org>`__ 3.1 or later
-  `reproject <http://reproject.readthedocs.org>`__ 0.4 or later

and the following are optional:

-  `PyAVM <http://astrofrog.github.io/pyavm/>`__ 0.9.4 or later
-  `pyregion <http://pyregion.readthedocs.org/>`__ 2.0 or later
-  `pillow <https://pypi.org/project/Pillow/>`__ 4.0 or later
-  `scikit-image <https://pypi.org/project/scikit-image/>`__ 0.14 or
   later

You can install APLpy with:

::

   pip install aplpy

If you want to install all optional dependencies, you can do:

::

   pip install aplpy[all]

.. |Build Status| image:: https://travis-ci.org/aplpy/aplpy.svg?branch=master
   :target: https://travis-ci.org/aplpy/aplpy
.. |CircleCI| image:: https://circleci.com/gh/aplpy/aplpy/tree/master.svg?style=svg
   :target: https://circleci.com/gh/aplpy/aplpy/tree/master
.. |codecov| image:: https://codecov.io/gh/aplpy/aplpy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/aplpy/aplpy
.. |Documentation Status| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
   :target: https://aplpy.readthedocs.io/en/latest/
