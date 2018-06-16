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
`Backward-compatibility notes`_

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
scripts that used APLpy 1.0 and earlier.

However, in some cases, the new :class:`~aplpy.FITSFigure` may not be
backward-compatible, in particular if you have made adjustments to figures in
the past using private attributes (e.g. ``fig._ax1``). For these cases, we have
provided a frozen copy of the APLpy 1.x FITSFigure class in the ``aplpy.legacy``
package - you can use this using::

    from aplpy.legacy import FITSFigure

Note that no new features will be added to this class. Critical bugs may be
fixed in that legacy class if reported, but otherwise for any non-critical
issues, we recommend migrating to the new :class:`aplpy.FITSFigure` class or
`WCSAxes`_ directly.

.. _api:

Reference/API
=============

.. automodapi:: aplpy
   :no-main-docstr:
   :no-heading:
   :no-inheritance-diagram:
