.. _arbitrary:

Arbitrary coordinate systems
============================

Coordinate type
---------------

In addition to standard longitude/latitude coordinates, APLpy supports any
valid quantities for coordinates (e.g. velocity, frequency, ...) as long as
the WCS header information is valid. To differentiate between longitudes,
latitudes, and arbitrary scalar values, APLpy keeps track of the axis
coordinate 'type' for each axis, and will try and guess these based on the
header. However, it is possible to explicitly specify the coordinate type with
the :meth:`~aplpy.aplpy.FITSFigure.set_xaxis_coord_type` and :meth:`~aplpy.aplpy.FITSFigure.set_yaxis_coord_type` methods in the
:class:`~aplpy.aplpy.FITSFigure` object::

    f = FITSFigure('2MASS_k.fits')
    f.set_xaxis_coord_type('scalar')
    f.set_xaxis_coord_type('latitude')
    
Valid coordinate types are ``longitude``, ``latitude``, and ``scalar``.
Longitudes are forced to be in the 0 to 360 degree range, latitudes are forced
to be in the -90 to 90 degree range, and scalars are not constrained.

Label formatting
----------------

How label formats are specified depends on the coordinate type. If the
coordinate is a longitude or latitude, then the label format is specified
using a special syntax which describes whether the label should be decimal or
sexagesimal, in hours or degrees, and indicates the number of decimal places.
For example:

* ``ddd.ddddd`` means decimal degrees, where the number of decimal places can
  be varied
* ``hh`` or ``dd`` means hours (or degrees)
* ``hh:mm`` or ``dd:mm`` means hours and minutes (or degrees and arcminutes)
* ``hh:mm:ss`` or ``dd:mm:ss`` means hours, minutes, and seconds (or degrees,
  arcminutes, and arcseconds)
* ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` means hours, minutes, and seconds (or
  degrees, arcminutes, and arcseconds), where the number of decimal places can
  be varied.

If the coordinate type is scalar, then the format should be specified as a
valid Python format. For example, ``%g`` is the default Python format,
``%10.3f`` means decimal notation with three decimal places, etc. For more
information, see `String Formatting Operations
<http://docs.python.org/library/stdtypes.html#string-formatting>`_.

In both cases, the default label format can be overridden::

    f.tick_labels.set_xformat('dd.ddddd')
    f.tick_labels.set_yformat('%11.3f')

Aspect ratio
------------

When plotting images in sky coordinates, APLpy makes pixel square by default,
but it is possible to change this, which can be useful for non-sky
coordinates. When calling :meth:`~aplpy.aplpy.FITSFigure.show_grayscale` or
:meth:`~aplpy.aplpy.FITSFigure.show_colorscale`, simply add ``aspect='auto'``
which will override the ``aspect='equal'`` default.