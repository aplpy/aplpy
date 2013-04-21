AVM tagging
===========

The latest developer version of APLpy has support for reading/writing AVM tags
from/to RGB images (via `PyAVM <http://astrofrog.github.io/pyavm/>`_). To make
a plot with an AVM-tagged RGB image, say 'example.jpg', you can use::

    import aplpy
    f = aplpy.FITSFigure('example.jpg')
    f.show_rgb()

Note that no filename is required for :meth:`~aplpy.aplpy.FITSFigure.show_rgb`
in this case.

If PyAVM is installed, :func:`~aplpy.rgb.make_rgb_image` can embed AVM
meta-data into RGB images it creates, although only JPEG and PNG files support
this::

    import aplpy
    aplpy.make_rgb_image('2mass_cube.fits', '2mass_rgb.jpg')

If PyAVM 0.9.1 or later is installed, the above file ``2mass_rgb.jpg`` will
include AVM meta-data and can then be plotted with::

    import aplpy
    f = aplpy.FITSFigure('2mass_rgb.jpg')
    f.show_rgb()

In other words, this means that when creating an RGB image with APLpy, it is
no longer necessary to initialize :class:`~aplpy.aplpy.FITSFigure` with a FITS
file and then use :meth:`~aplpy.aplpy.FITSFigure.show_rgb` with the RGB image
filename - instead, :class:`~aplpy.aplpy.FITSFigure` can be directly
initialized with the AVM-tagged image.

To disable the embedding of AVM tags, you can use the ``embed_avm_tags=False``
option for :func:`~aplpy.rgb.make_rgb_image`.

These features require `PyAVM 0.9.1 <http://astrofrog.github.io/pyavm/>`_
or later. Please report any issues you encounter `here
<https://github.com/aplpy/aplpy/issues>`_.