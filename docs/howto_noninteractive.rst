APLpy in non-interactive mode
-----------------------------

While APLpy can be easily used to interactively make plots, it is also
possible to make plots without opening up a display. This can be
useful to run APLpy remotely, or to write non-interactive scripts to
plot one or many FITS files.

Running APLpy in non-interactive mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run APLpy in non-interactive mode, you will need to change the
'backend' used by matplotlib from an interactive (e.g. WxAgg, TkAgg,
MacOS X) to a non-interactive (e.g. Agg, Cairo, PS, PDF) backend. The
default backend is typically set in your ``.matplotlibrc``
file (or if you do not have such a file, an interactive backend is
usually chosen by default). The easiest way to change the backend
temporarily is to use the ``matplotlib.use()`` function::

    import matplotlib
    matplotlib.use('Agg')

It is important to change the backend via ``matplotlib.use``
before the ``aplpy`` module is imported. Once the backend has
been changed, any call to ``FITSFigure()`` will no longer make a figure
window appear. The following script can be used to make a PNG plot::

    import matplotlib
    matplotlib.use('Agg')

    import aplpy

    f = aplpy.FITSFigure('mips_24micron.fits')
    f.show_grayscale()
    f.save('mips_24.png')

Pan/Zoom in non-interactive mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the advantages of using APLpy in interactive mode is the
ability to zoom in on a given region of interest. To replicate this
functionality in non-interactive mode, the
``FITSFigure.recenter()`` method can be used. This method
takes a central position, and either a radius (to make a square plot)
or a width/height (to make a rectangular plot). This is illustrated in
the following example::

    import matplotlib
    matplotlib.use('Agg')

    import aplpy

    f = aplpy.FITSFigure('mips_24micron.fits')
    f.show_grayscale()
    f.recenter(266.2142,-29.1832,width=0.5,height=0.3)
    f.save('mips_24_zoomin.png')

Batch scripting
^^^^^^^^^^^^^^^

Using APLpy non-interactively can be useful for making plots of many
FITS files. Given a directory ``fits/`` containing FITS
files, the following code will generate on plot for each
``.fits`` file::

    import matplotlib
    matplotlib.use('Agg')

    import aplpy

    import glob
    import os

    for fits_file in glob.glob(os.path.join('fits/','*.fits')):

        f = aplpy.FITSFigure(fits_file)
        f.show_grayscale()
        f.save(fits_file.replace('.fits','.png'))
        f.close()


