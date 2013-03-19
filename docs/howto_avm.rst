AVM tagging
===========

The latest developer version of APLpy has experimental support for
reading/writing AVM tags from/to RGB images. To make a plot with an AVM-tagged RGB image, say 'example.jpg', you can use::

    import aplpy
    f = aplpy.FITSFigure('example.jpg')
    f.show_rgb()
    
Note that no filename is required for `show_rgb()` in this case.

Optionally, ``aplpy.make_rgb_image`` can embed AVM meta-data into RGB
images it creates, using the ``embed_avm_tags=True`` option::

    import aplpy
    aplpy.make_rgb_image('2mass_cube.fits',\
                         '2mass_rgb.jpg', \
                         embed_avm_tags=True)

This means that when creating an RGB image with APLpy, it is no longer
necessary to initialize ``FITSFigure`` with a FITS file and then use
``show_rgb`` with the RGB image filename - instead, ``FITSFigure`` can be
directly initialized with the AVM-tagged image.

These features require `PyAVM 0.1.2 <https://github.com/astrofrog/pyavm>`_
or later. Please report any issues you encounter `here
<https://github.com/aplpy/aplpy/issues>`_.