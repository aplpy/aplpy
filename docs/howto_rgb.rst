Making RGB images
-----------------

While the APLpy :meth:`~aplpy.aplpy.FITSFigure.show_rgb` can be used to
display an RGB image with the same projection as a given FITS file, it is also
possible to use the :func:`~aplpy.rgb.make_rgb_cube` and
:func:`~aplpy.rgb.make_rgb_image` to generate RGB images from scratch, even
for files with initially different projections/resolutions.

Reprojecting three images to the same projection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are starting from three images with different projections/resolutions,
the first step is to reproject these to a common projection/resolution. The
following code shows how this can be done using the
:func:`~aplpy.rgb.make_rgb_cube` function::

    import aplpy
    aplpy.make_rgb_cube(['2mass_k.fits','2mass_h.fits', \
                         '2mass_j.fits'],'2mass_cube.fits')

This method makes use of Montage to reproject the images to a common
projection. For more information on installing Montage, see here. The above
example produces a FITS cube named ``2mass_cube.fits`` which contains the
three channels in the same projection. This can be used to then produce an RGB
image (see next section)

Producing an RGB image from images in a common projection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :func:`~aplpy.rgb.make_rgb_image` function can be used to produce an RGB
image from either three FITS files in the exact same projection, or a FITS
cube containing the three channels (such as that output by
:func:`~aplpy.rgb.make_rgb_cube`). The following example illustrates how to do this::

    import aplpy
    aplpy.make_rgb_image('2mass_cube.fits','2mass_rgb.tif')

In the above example, APLpy will automatically adjust the stretch of the
different channels to try and produce a reasonable image, but it is of course
possible to specify one or more of the lower/upper limits of the scale to use
for each channel. For each lower/upper scale limit, this can be done in two
ways. The first is to use the vmin_r/g/b or vmax_r/g/b argument which specifies the
pixel value to use for the lower or upper end of the scale respectively. The
alternative is to use the pmin_r/g/b or pmax_r/g/b arguments, which specify the
percentile value to use instead of an absolute value. The two can of course be
mixed, such as in the following example::

    import aplpy
    aplpy.make_rgb_image('2mass_cube.fits','2mass_rgb.tif', \
                          vmin_r=0.,pmax_g=90.)

