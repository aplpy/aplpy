*******************
APLpy documentation
*******************

`APLpy <http://aplpy.github.io>`_ (the Astronomical Plotting Library in Python -
pronounced *apple pie*) is a Python package module aimed at producing
publication-quality plots of astronomical imaging data, and has been around
since 2009.

Since APLpy 2.0, APLpy relies on Astropy's `WCSAxes
<http://docs.astropy.org/en/stable/visualization/wcsaxes/index.html>`_ package
to draw the coordinate axes and grids, which in turn uses `Matplotlib
<http://matplotlib.org>`_ to do the rendering. This is a big change compared to
previous versions of APLpy, which handled the drawing of the coordinate axes and
grids directly. For information about backward-compatibility, see the
`Backward-compatibility notes`_.

Note that APLpy 2.x is only compatible with Python 3.5 and later.

Should you use APLpy?
=====================

The `WCSAxes`_ package in Astropy can be used without APLpy to produce plots of
astronomical images. It provides a programmatic interface that is conceptually
very close to Matplotlib, and can be used to make plots that are more complex
than what APLpy has historically been able to do. If you want to be able to
control the appearance of your plots in detail, including for example adding
overlay coordinate systems, or if you simply want a programmatic interface that
is consistent with Matplotlib, then we recommend you use `WCSAxes`_ directly. If
you have a FITS file and just want to make it into a plot in a couple of lines,
then APLpy is the package for you.

Installing APLpy
================

You can install APLpy with pip using::

    pip install aplpy

To include all optional dependencies, you can do::

    pip install aplpy[all]

Using APLpy
===========

APLpy includes a :class:`~aplpy.FITSFigure` class that provides a simple
interface to make plots and provides easy methods for overlaying shapes, beams,
adding colorbars, and overplotting regions.

.. toctree::
  :maxdepth: 1

  fitsfigure/quickstart.rst
  fitsfigure/quick_reference.rst
  fitsfigure/arbitrary_coordinate_systems.rst
  fitsfigure/slicing.rst
  fitsfigure/howto_noninteractive.rst
  fitsfigure/howto_avm.rst
  fitsfigure/howto_subplot.rst
  rgb

.. _backcompat:

Backward-compatibility notes
============================

APLpy continues to include a :class:`~aplpy.FITSFigure` class that provides a
simpler interface and deals with the reading of FITS files and constructing WCS
objects. This class uses `WCSAxes`_ behind the scenes, but provides easy methods
for overlaying shapes, beams, adding colorbars, and overplotting regions. The
interface of this class is intended to be backward-compatible with existing
scripts that used APLpy 1.0 and earlier. If you run into issues with old
scripts, please report the issues in the `issue tracker
<https://github.com/aplpy/aplpy/issues>`_.

Note however that if you have made adjustments to figures in the past using private
attributes (e.g. ``fig._ax1``), these will no longer work and this cannot be
fixed in APLpy 2.x.

In any case, if you have issues with APLpy 2.x and want to continue using APLpy
1.x, you can always restrict the version of APLpy when installing it using
e.g.::

    pip install "aplpy<2"

or::

    conda install "aplpy<2"

If critical bugs are found in the 1.x releases and can easily be fixed, we may
release new 1.x versions.

.. _api:

Reference/API
=============

.. automodapi:: aplpy
   :no-main-docstr:
   :no-heading:
   :no-inheritance-diagram:
