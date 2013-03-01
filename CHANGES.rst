CHANGES
--------

Version 0.9.9 (unreleased)

    The main change in this version is that APLpy is now an Astropy-affiliated
    package. This means that the Astropy core package is now required, but
    PyFITS and PyWCS are no longer required as dependencies.

    This release is also the first release fully compatible with Python 3.

    New features
    ~~~~~~~~~~~~

    - file-like objects can now be passed to ``FITSFigure.save()``

    Bug fixes
    ~~~~~~~~~

    - fix bug that caused regions read from a ds9 region file to be offset by
      one pixel.

    - fix bug that caused an exception when adding a Beam

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
