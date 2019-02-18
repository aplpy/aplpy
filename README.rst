|Build Status| |CircleCI| |AppVeyor| |codecov| |Documentation Status|

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
-  `reproject <https://reproject.readthedocs.org>`__ 0.4 or later
-  `PyAVM <http://astrofrog.github.io/pyavm/>`__ 0.9.4 or later
-  `pyregion <http://pyregion.readthedocs.org/>`__ 2.0 or later
-  `pillow <https://pypi.org/project/Pillow/>`__ 4.0 or later
-  `scikit-image <https://pypi.org/project/scikit-image/>`__ 0.14 or later
-  `shapely <https://shapely.readthedocs.io/en/stable/project.html>`__ 1.6 or later

You can install APLpy and all its dependencies with::

    pip install aplpy

or if you use conda::

    conda install -c astropy aplpy

.. |Build Status| image:: https://travis-ci.org/aplpy/aplpy.svg?branch=master
   :target: https://travis-ci.org/aplpy/aplpy
.. |CircleCI| image:: https://circleci.com/gh/aplpy/aplpy/tree/master.svg?style=svg
   :target: https://circleci.com/gh/aplpy/aplpy/tree/master
.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/7whcuutukcbowyfn/branch/master?svg=true
   :target: https://ci.appveyor.com/project/Astropy/aplpy
.. |codecov| image:: https://codecov.io/gh/aplpy/aplpy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/aplpy/aplpy
.. |Documentation Status| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
   :target: https://aplpy.readthedocs.io/en/latest/
