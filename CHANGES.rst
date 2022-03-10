CHANGES
--------

2.1.0 (2022-03-10)
------------------

- Updated package infrastructure to follow guidelines described in APE 17, namely
  removing astropy-helpers and using tox for setting up testing environments. [#448]

- Fix compatibility with astropy 4.x and 5.0. [#448,#471]

- Fixed default color for ``show_lines`` (was previously transparent, now black). [#441]

- Fixed ``set_tick_direction`` to not error due to incorrect reference to ``ax``. [#450]

- Fixed compatibility with Matplotlib 3.4. [#466]

2.0.3 (2019-02-19)
------------------

- Fix 'arcsinh' stretch and fix definition of vmid to match that in 1.x. [#421]

2.0.2 (2019-02-18)
------------------

- Fixed ``set_nan_color``. [#419]

2.0.1 (2019-02-18)
------------------

- Remove unused arguments in ``make_rgb_cube`` and fix behavior of
  ``north=False``. [#417]

- Fixed bug in image extent for non-square RGB images. [#417]

2.0 (2019-02-17)
----------------

- Refactored APLpy to make use of WCSAxes to draw coordinate frames and
  astropy.visualization to deal with image stretching. [#239, #364, #365]

- Use reproject package instead of montage-wrapper and Montage. [#360]

1.1.1 (2016-10-04)
------------------

- Added missing LICENSE and README to tarball.

- Fix undefined ``HDUList``. [#317]

1.1 (2016-09-23)
----------------

- Fixed compatibility of Scalebar.set with Matplotlib 1.5.x. [#272, #286]

- Fixed compatibility with Python 3.5.

- Astropy is now a required dependency, and PyFITS and PyWCS are no longer
  supported.

1.0 (2015-02-18)
----------------

    New features
    ~~~~~~~~~~~~

    - Added new ``show_vectors`` to show vector maps. [#220]

    Improvements
    ~~~~~~~~~~~~

    - The ``auto_refresh`` option now defaults to ``False`` unless IPython is
      being used and the Matplotlib backend is interactive. [#238]

    Bug fixes
    ~~~~~~~~~

    - Fix a bug that caused RGB images to be incorrectly displayed when zooming
      in. [#235]

0.9.14 (2014-11-05)
-------------------

    Bug fixes
    ~~~~~~~~~

    - Fix a bug that caused smoothing to fail with integer arrays. [#165]

    Improvements
    ~~~~~~~~~~~~

    - Fix deprecation warnings from Astropy. [#173]

0.9.13 (2014-10-04)
-------------------

    New features
    ~~~~~~~~~~~~

    - Added ``FITSFigure.set_title`` method that can be used to set the title
      of a figure. [#175]

    Improvements
    ~~~~~~~~~~~~

    - Beams and scalebars can now optionally be instantiated with Astropy
      angular units and quantities. [#186]

    - APLpy now includes image tests to ensure reliability over time. [#200]

    - The code is now all Python 2 and 3 compatible without requiring 2to3.
      [#198]

    Bug fixes
    ~~~~~~~~~

    - Fix bug that caused a crash when plotting an image with a single valid
      pixel [#197]

    - Fixed a severe bug that caused rotated images to have incorrect pixel
      scales determined. [#211]

    - Fixed a bug that caused set_nan_color to modify Matplotlib colormaps
      globally rather than apply just to the desired FITSFigure. [#214]

0.9.12 (2014-07-17)
-------------------

    This version fixes compatibility with Astropy 0.4

    New features
    ~~~~~~~~~~~~

    - Added the ability to call ``fig.show_contour()`` without arguments and
      used the data used to initialize ``FITSFigure``. [#170]

    - Added the ability to format colorbar ticks in exponential notation using
      the ``log_format`` argument. [#143]

    - Added the ability to make NaNs transparent in RGB image output, using the
      ``make_nans_transparent`` argument. [#138]

    API Changes
    ~~~~~~~~~~~

    - astropy.wcs.WCS no longer contains information about the original image
      size.  Any attempt to instantiate a FITSFigure from a WCS object will raise
      a DeprecationException.  A workaround is to add `naxisn` attributes to your
      WCS object::

         mywcs = wcs.WCS(header)
         mywcs.naxis1 = header['NAXIS1']
         mywcs.naxis2 = header['NAXIS2']

    Bug fixes
    ~~~~~~~~~

    - FITSFigure can now be instantiated using an astropy.io.fits.CompImageHDU
      object. [#188]

    - The coordinate grid is now plotted on the whole axes, not just the subset
      containing the image (noticeable when zooming out). [#118]

0.9.11 (2013-11-29)
-------------------

    Bug fixes
    ~~~~~~~~~

    - Fix a bug that meant that pixel scales were incorrectly extracted for
      some WCS settings. [#156]

0.9.10 (2013-11-25)
-------------------

    This version restores compatibility with Astropy 0.3

    New Features
    ~~~~~~~~~~~~

    - `FITSFigure.recenter` can now be used with sliced data cubes. [#122]

    Bug fixes
    ~~~~~~~~~

    - Fixed issues related to bugs in matplotlib in `match_original` when using
      patch collections. [#124]

    - Fixed a bug that made images containing NaN or Inf values crash APLpy. [#113]

    - Fixed a bug that meant that world2pix and pix2world could not take
      Astropy table columns. [#114]

0.9.9 (2013-04-25)
------------------

    The main change in this version is that APLpy is now an Astropy-affiliated
    package. This means that the Astropy core package is now required, but
    PyFITS and PyWCS are no longer required as dependencies.

    This release is now no longer compatible with python-montage, and users
    should use the montage-wrapper package instead:

       http://www.astropy.org/montage-wrapper/

    Similarly, PyAVM 0.9.1 or later is now required, and APLpy cannot use
    earlier versions:

      http://astrofrog.github.io/pyavm/

    This release is also the first release fully compatible with Python 3.

    New features
    ~~~~~~~~~~~~

    - file-like objects can now be passed to ``FITSFigure.save()``

    - the subplot= argument to ``FITSFigure`` can now take the tuple syntax
      ``(2, 2, 1)`` instead of the full axes box, e.g. ``[0.1, 0.1, 0.9,
      0.9]`` (thanks to Anika Schmiedeke for a patch).

    - a colorbar label can now be set (thanks to Daniel Goering for a patch).

    API changes
    ~~~~~~~~~~~

    - the ``smooth`` argument used for images and contours can no longer take
      a tuple. It takes either a single value for symmetric kernels (``gauss``
      and ``box``), or it can take a Numpy array for any other kernel shape.

    Bug fixes
    ~~~~~~~~~

    - fixed bug that caused regions read from a ds9 region file to be offset
      by one pixel.

    - fixed bug that caused an exception when adding a Beam

    - fixed bug that caused labels in decimal degrees to disappear for images
      near the poles.

    - fixed a bug that caused RGB images to appear vertically flipped with
      certain versions of Matplotlib.

    - added a workaround for a bug in Matplotlib that caused patches to appear
      filled even with ``facecolor='none'``.

    - fixed bug that caused images with NaN or Inf values to not be smoothed
      correctly.

Version 0.9.8

    This version fixes issues that occurred when using APLpy with PyFITS
    3.0.5. This version also contains the first unit/regression tests (which
    we will include many more of in future).

    New features
    ~~~~~~~~~~~~

    - APLpy now includes regression tests that can be run with:

        python setup.py test

    - FITSFigure can now be initialized with files or HDUs with missing WCS
      information.

    - FITSFigure can now be initialized directly with Numpy arrays

    - Added methods to show/hide ticks

    Bug fixes
    ~~~~~~~~~

    - Fixed a major bug that prevented data cube slicing with PyFITS 3.0.5

    - Fixed a few bugs that occurred when plotting a grid for a few specific
      projections.

    - Fixed a bug that cause the error:

        'Figure' object has no attribute '_auto_refresh'


Version 0.9.7

    This version sees the re-write of the WCS support to enable plotting of
    FITS files with arbitrary coordinates rather than just sky coordinates,
    and to allow slicing of multi-dimensional data cubes. It is now very easy
    for example to make position-velocity plots from a 3D FITS cube.

    See http://aplpy.github.com/documentation/slicing.html for details.

    New features
    ~~~~~~~~~~~~

    - added the ability to plot arbitrary coordinate systems rather than just
      sky coordinates.

    - added the ability to slice multi-dimensional data cubes.

    - added minor ticks.

    - pressing 'c' toggles between showing world and pixel coordinates in the
      bottom of the interactive window.

    - added the ability to specify slice indices for 3D FITS cubes in
      make_rgb_image.

    - allow pyregion.ShapeList instance to be passed to show_regions.

    - the 'logging' module is now used for any stdout output.

    - added an overlap= argument to show_contour to force only contours with
      at least one point in the image to be shown. This can result in
      significantly improved performance, and smaller files, when large FITS
      files are used to display contours.

    Changes
    ~~~~~~~

    - the default frame color for the 'pretty' theme (the default) is now
      black


Version 0.9.6

    APLpy is now released under an MIT license

    New Features
    ~~~~~~~~~~~~

    - support for plotting AVM-tagged images (requires PyAVM)

    - make_rgb_image can now optionally embed AVM Spatial.* meta-data into
      images (off by default, requires PyAVM)

    - added support for multiple beams

    - added method to show arrows

    - added method to show lines (thanks to Moritz Guenther)

    - added close() method to FITSFigure to free up memory (useful when
      making many finder charts for example)

    - added B1950 <-> J2000 conversion

    - added axis_labels.set_x/yposition and tick_labels.set_x/yposition to
      control whether labels are on top/bottom or left/right of the axes.

    - now uses python-montage wrapper for reprojection

    - added support for passing a WCS object to FITSFigure instead of a
      file

    - allow a custom box to be specified for the colorbar

    API changes
    ~~~~~~~~~~~

    - vmid has changed meaning for log image scaling. It is now the
      baseline value to subtract from pixel values before taking the log
      (defaults to zero)

    - added interpolation= option to show_grayscale and show_colorscale

    - added support for zorder= in methods to show shapes (controls which
      layers appear on top of which)

    - added north=, system=, and equinox= to make_rgb_cube for more control
      over the final projection

    Bug fixes
    ~~~~~~~~~

    - added a few workaround for matplotlib bugs

    - fixed a major bug with downsampling

    - fixed bug with import of local modules

    - other minor bug fixes

Version 0.9.5

    New Features
    ~~~~~~~~~~~~

    - Support for image and contour smoothing

    - Support for slicing of n-dimensional datacubes

    - Support for beam:
        -> add_beam()
        -> remove_beam()

    - Support for colorbar:
        -> add_colorbar()
        -> remove_colorbar()

    - Support for scalebar:
        -> add_scalebar()
        -> remove_scalebar()

    - Support for plotting ds9 region files:
        -> show_regions()

    - Support for automatic bounding box adjustments when saving

    - New method to set the color to use for NaN values:
        -> set_nan_color()

    - Auto refreshing has been improved. Figures only refresh once per user
      command if refreshing is turned on.

    - Ensure tick spacing / label format consistency

    - New method to overlay polygons

    API changes
    ~~~~~~~~~~~

    - The API has been majorly overhauled. Methods that have been
      deprecated will give instructions on the new methods to use.

    Bug fixes
    ~~~~~~~~~

    - Fixed a bug with filled contours

    - Fixed bug with remove_layer

    - Fixed bug with montage commands

Version 0.9.4

    Important changes
    ~~~~~~~~~~~~~~~~~

    Matplotlib 0.99 is now required for APLpy

    New Features
    ~~~~~~~~~~~~

    - methods such as show_contour, show_markers, etc. now return the
      contour, marker, etc. object

    - added a method to retrieve the object in a specific layer:
        -> get_layer()

    - ability to show the beam for the observations:
        -> show_beam()
        -> hide_beam()
        -> set_beam_properties()

    - added the ability to show/hide only the x or y axis/tick labels:
        -> show_xtick_labels()
        -> hide_xtick_labels()
        -> show_ytick_labels()
        -> hide_ytick_labels()
        -> show_xaxis_labels()
        -> hide_xaxis_labels()
        -> show_yaxis_labels()
        -> hide_yaxis_labels()

    - convenience functions for world to pixel and pixel to world
      conversion:
        -> world2pixel()
        -> pixel2world()

    - added a convention= argument to FITSFigure() and show_contour(). This is
      to be used in cases where the WCS interpretation is ambiguous. For
      example, a -CAR projection with CRVAL2<>0 can be interpreted in two
      different ways. If an ambiguous case pops up, APLpy will raise an
      exception and ask for the convention to be specified.

    API changes
    ~~~~~~~~~~~

    - set_labels_latex() is now set_system_latex()

    Bug fixes
    ~~~~~~~~~

    - the current position of the cursor in world coordinates is now correctly
      shown in interactive mode

    - fixed an issue which caused RGB FITS cubes to be 64-bit

    - fixed a bug which meant that the coordinate grid was not updated
      immediately during pan and zoom

Version 0.9.3

    New Features
    ~~~~~~~~~~~~

    - added aplpy.make_rgb_cube() that allows users to make a FITS RGB cube
      from three FITS files with different projections

    - added aplpy.make_rgb_image() that allows users to make an RGB file in
      standard image formats from a FITS RGB cube

    - added width= and height= arguments to aplpy.FITSFigure.recenter()
      method.

    - added show_circles(), show_ellipses(), and show_rectangles() to
      aplpy.FITSFigure

    - new hide_grayscale() and hide_colorscale() methods

    API changes
    ~~~~~~~~~~~

    - changes to the API for set_tick_labels_* and set_axis_labels_* methods

    - percentiles values are now specified between 0 and 100

    Bug fixes
    ~~~~~~~~~

    - fixed an issue which ocurred when reading in FITS cubes

    - fixed an issue which led to the last tick along an axis being missing
      for coarse images

    - fixed a bug that occured if set_theme was called before showing the
      image

    - fixed a bug that occured when show_contour was called after removing a
      layer

    Acknowledgments
    ~~~~~~~~~~~~~~~

    Thanks to Paul Ray, Adam Ginsburg, Gus Muench, and forum user hatchell for
    bug reports and feature suggestions.


Version 0.9.2

    Improvements
    ~~~~~~~~~~~~

    - Improved compatibility issues with matplotlib 0.98.6svn

    - Improved speed of initialization of FITSFigure


Version 0.9.1.2

    Bug fixes
    ~~~~~~~~~

    - fixed a major bug that occured when reading in Galactic -CAR images


Version 0.9.1

    SciPy Dependency Dropped
    ~~~~~~~~~~~~~~~~~~~~~~~~

    While SciPy is a great python package, it can be troublesome to build and
    install from scratch. Thanks to Tom Aldcroft's suggestion and highlighting
    some of his own code we were able to easily drop the SciPy dependency.

    New Features
    ~~~~~~~~~~~~

    - Users can now pass a pyfits HDU instance instead of filenames for both
      FITSFigure() and show_contour() if desired.

    - Users can now specify an existing figure with the figure= argument.

    - Users with a recent enough version of matplotlib (0.98.6svn) can now use
      the subplot= argument to place multiple plots in a single figure.

    - New hide/show_tick_labels() and hide/show_axis_labels() methods.

    - Show_grayscale and show_colorscale() now accept percentile_lower= and
      percentile_higher= as arguments.

    - Show_grayscale and show_colorscale() now print out vmin and vmax if
      chosen automatically.

    - New recenter() method to pan and zoom non-interactively.

    General Fixes and Optimization
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    - Added HDU keyword for the show_contour() method.

    - More robust reading in FITS file for the show_contour() method.

    - Warning if FITS files do not exist for FITSFigure() or show_contour().


Version 0.9.0

    First public beta release
