Quick reference Guide
---------------------

.. toctree::
  :maxdepth: 1


.. note:: Rather than showing the generic call signature for the methods on
          this page, these are given in the form of example values. In
          addition, not all of the optional keywords are mentioned here.
          For more information on a specific command and all the options
          available, type ``help`` followed by the method name, e.g. ``help
          fig.show_grayscale``. When multiple optional arguments are given,
          this does not mean that all of them have to be specified, but
          just shows all the options available.

Introduction
^^^^^^^^^^^^

To import APLpy::

    import aplpy

To create a figure of a FITS file::

    fig = aplpy.FITSFigure('myimage.fits')

Here and in the remainder of this reference guide, we use the variable name
``fig`` for the figure object, but any name can be used.

A grayscale or colorscale representation of the FITS image can be shown and
hidden using the following methods::

    fig.show_grayscale()
    fig.hide_grayscale()
    fig.show_colorscale()
    fig.hide_colorscale()

To show a three-color image, use the following method, specifying the
filename of the color image::

    fig.show_rgb('m17.jpeg')

The figure can be interactively explored by zooming and panning. To
recenter on a specific region programmatically, use the following method,
specifying either a radius::

    fig.recenter(33.23, 55.33, radius=0.3)  # degrees

or a separate width and height::

    fig.recenter(33.23, 55.33, width=0.3, height=0.2)  # degrees

To overlay contours, use::

    fig.show_contour('co_data.fits')

To save the current figure, use::

    fig.save('myplot.eps')

Other formats such as PDF, PNG, etc. can be used.

Labels
^^^^^^

Labels can be added either in world coordinates::

    fig.add_label(34.455, 54.112, 'My favorite star')

or relative to the axes::

    fig.add_label(0.1, 0.9, '(a)', relative=True)

Shapes
^^^^^^

To overlay different shapes, the following methods are available::

    fig.show_markers(x_world, y_world)
    fig.show_circles(x_world, y_world, radius)
    fig.show_ellipses(x_world, y_world, width, height)
    fig.show_rectangles(x_world, y_world, width, height)
    fig.show_arrows(x_world, y_world, dx, dy)

where ``x_world``, ``y_world``, ``radius``, ``width``, ``height``, ``dx``,
and ``dy`` should be 1D arrays specified in degrees.

It is also possible to plot lines and polygons using::

    fig.show_lines(line_list)
    fig.show_polygons(polygon_list)

For these methods, ``line_list`` and ``polygon_list`` should be lists of
2xN Numpy arrays describing the coordinates of the vertices in degrees.

DS9 Regions
^^^^^^^^^^^

DS9 region files can be overlaid with::

    fig.show_regions('myregions.reg')

Layers
^^^^^^

Markers, shapes, regions and text labels are stored in layers. These layers can be listed using::

    fig.list_layers()

Layers can be hidden and shown with the following methods::

    fig.hide_layer('regions')
    fig.show_layer('regions')

Any layer can be retrieved using::

    layer = fig.get_layer('circles')

Finally, layers can be removed using::

    fig.remove_layer('rectangles')

Coordinates
^^^^^^^^^^^

Two methods are provided to help transform coordinates between world and pixel coordinates. These accept either scalars or arrays in degrees::

    x_pix, y_pix = fig.world2pixel(45.3332, 22.1932)
    x_world, y_world = fig.pixel2world(np.array([1., 2., 3]), np.array([1., 3., 5.]))

Frame
^^^^^

To set the look of the frame around the figure, use::

    fig.frame.set_linewidth(1)  # points
    fig.frame.set_color('black')

Colorbar
^^^^^^^^

A grid can be added and removed using the following commands::

    fig.add_colorbar()
    fig.remove_colorbar()

Once :meth:`~aplpy.aplpy.FITSFigure.add_colorbar` has been called, the ``fig.colorbar`` object is created and the following methods are then available:

* Show and hide the colorbar::

    fig.colorbar.show()
    fig.colorbar.hide()

* Set where to place the colorbar::

    fig.colorbar.set_location('right')

  This can be one of ``left``, ``right``, ``bottom`` or ``top``.

* Set the width of the colorbar::

    fig.colorbar.set_width(0.1)  # arbitrary units, default is 0.2

* Set the amount of padding between the colorbar and the parent axes::

    fig.colorbar.set_pad(0.03)  # arbitrary units, default is 0.05

* Set the font properties of the labels::

    fig.colorbar.set_font(size='medium', weight='medium', \
                          stretch='normal', family='sans-serif', \
                          style='normal', variant='normal')

* Add a colorbar label::

    f.colorbar.set_axis_label_text('Surface Brightness (Jy/beam)')

* Set some of the colorbar label properties::

    f.colorbar.set_axis_label_font(size=12, weight='bold')

* Set the padding between the colorbar and the label in points::

    f.colorbar.set_axis_label_pad(10)

* Change the rotation of the colorbar label, in degrees::

    f.colorbar.set_axis_label_rotation(270)

Coordinate Grid
^^^^^^^^^^^^^^^

A coordinate grid can be added and removed using the following commands::

    fig.add_grid()
    fig.remove_grid()

Once :meth:`~aplpy.aplpy.FITSFigure.add_grid` has been called, the ``fig.grid`` object is created and the following methods are then available:

* Show and hide the grid::

    fig.grid.show()
    fig.grid.hide()

* Set the x and y spacing for the grid::

    fig.grid.set_xspacing(0.2)  # degrees
    fig.grid.set_yspacing(0.2)  # degrees

* Set the color of the grid lines::

    fig.grid.set_color('white')

* Set the transparency level of the grid lines::

    fig.grid.set_alpha(0.8)

* Set the line style and width for the grid lines::

    fig.grid.set_linestyle('solid')
    fig.grid.set_linewidth(1)  # points

Scalebar
^^^^^^^^

A scalebar can be added and removed using the following commands::

    fig.add_scalebar()
    fig.remove_scalebar()

Once :meth:`~aplpy.aplpy.FITSFigure.add_scalebar` has been called, the ``fig.scalebar`` object is created and the following methods are then available:

* Show and hide the scalebar::

    fig.scalebar.show(0.2)  # length in degrees
    fig.scalebar.hide()

* Change the length of the scalebar::

    fig.scalebar.set_length(0.02)  # degrees

* Specify the length of the scalebar in different units::

    from astropy import units as u
    fig.scalebar.set_length(72 * u.arcsecond)

* Change the label of the scalebar::

    fig.scalebar.set_label('5 pc')

* Change the corner that the beam is shown in::

    fig.scalebar.set_corner('top right')

  This can be one of ``top right``, ``top left``, ``bottom right``,
  ``bottom left``, ``left``, ``right``, ``bottom`` or ``top``.

* Set whether or not to show a frame around the beam::

    fig.scalebar.set_frame(False)

* Set the transparency level of the scalebar and label::

    fig.scalebar.set_alpha(0.7)

* Set the color of the scalebar and label::

    fig.scalebar.set_color('white')

* Set the font properties of the label::

    fig.scalebar.set_font(size='medium', weight='medium', \
                          stretch='normal', family='sans-serif', \
                          style='normal', variant='normal')

* Set the line style and width for the scalebar::

    fig.scalebar.set_linestyle('solid')
    fig.scalebar.set_linewidth(3)  # points

* Set multiple properties at once::

    fig.scalebar.set(linestyle='solid', color='red', ...)

Beam
^^^^

A beam can be added and removed using the following commands::

    fig.add_beam()
    fig.remove_beam()

Once :meth:`~aplpy.aplpy.FITSFigure.add_beam` has been called, the ``fig.beam`` object is created and the following methods are then available:

* Show and hide the beam::

    fig.beam.show()
    fig.beam.hide()

* Change the major and minor axes, and the position angle::

    fig.beam.set_major(0.03)  # degrees
    fig.beam.set_minor(0.02)  # degrees
    fig.beam.set_angle(45.)  # degrees

* Specify the major and minor axes, and the position angle, in explicit units::

    from astropy import units as u
    fig.beam.set_major(108 * u.arcsecond)
    fig.beam.set_minor(349 * u.microradian)
    fig.beam.set_angle(45 * u.degree)

* Change the corner that the beam is shown in::

    fig.beam.set_corner('top left')

  This can be one of ``top right``, ``top left``, ``bottom right``,
  ``bottom left``, ``left``, ``right``, ``bottom`` or ``top``.

* Set whether or not to show a frame around the beam::

    fig.beam.set_frame(False)

* Set the transparency level of the beam::

    fig.beam.set_alpha(0.5)

* Set the color of the whole beam, or the edge and face color individually::

    fig.beam.set_color('white')
    fig.beam.set_edgecolor('white')
    fig.beam.set_facecolor('green')

* Set the line style and width for the edge of the beam::

    fig.beam.set_linestyle('dashed')
    fig.beam.set_linewidth(2)  # points

* Set the hatch style of the beam::

    fig.beam.set_hatch('/')

* Set multiple properties at once::

    fig.beam.set(facecolor='red', linestyle='dashed', ...)

Coordinate types
^^^^^^^^^^^^^^^^

APLpy supports three types of coordinates: longitudes (in the range 0 to 360 with wrap-around), latitudes (in the range -90 to 90), and scalars (any arbitrary value). APLpy tries to guess the correct type of coordinate for each axis, but it is possible to override this::

    fig.set_xaxis_coord_type('scalar')
    fig.set_yaxis_coord_type('longitude')

Valid options are ``longitude``, ``latitude``, and ``scalar``.

Axis labels
^^^^^^^^^^^

The methods to control the x- and y- axis labels are the following

* Show/hide both axis labels::

    fig.axis_labels.show()
    fig.axis_labels.hide()

* Show/hide the x-axis label::

    fig.axis_labels.show_x()
    fig.axis_labels.hide_x()

* Show/hide the y-axis label::

    fig.axis_labels.show_y()
    fig.axis_labels.hide_y()

* Set the text for the x- and y-axis labels::

    fig.axis_labels.set_xtext('Right Ascension (J2000)')
    fig.axis_labels.set_ytext('Declination (J2000)')

* Set the displacement of the x- and y-axis labels from the x- and y-axis respectively::

    fig.axis_labels.set_xpad(...)
    fig.axis_labels.set_ypad(...)

* Set where to place the x-axis label::

    fig.axis_labels.set_xposition('bottom')

* Set where to place the y-axis label::

    fig.axis_labels.set_yposition('right')

* Set the font properties of the labels::

    fig.axis_labels.set_font(size='medium', weight='medium', \
                             stretch='normal', family='sans-serif', \
                             style='normal', variant='normal')

Tick labels
^^^^^^^^^^^

The methods to control the numerical labels below each tick are the following

* Show/hide all tick labels::

    fig.tick_labels.show()
    fig.tick_labels.hide()

* Show/hide the x-axis labels::

    fig.tick_labels.show_x()
    fig.tick_labels.hide_x()

* Show/hide the y-axis labels::

    fig.tick_labels.show_y()
    fig.tick_labels.hide_y()

* Set the format for the x-axis labels (e.g hh:mm, hh:mm:ss.s, etc.)::

    fig.tick_labels.set_xformat('hh:mm:ss.ss')

* Set the format for the y-axis labels (e.g dd:mm, dd:mm:ss.s, etc.)::

    fig.tick_labels.set_yformat('dd:mm:ss.s')

* Set where to place the x-axis tick labels::

    fig.tick_labels.set_xposition('top')

* Set where to place the y-axis tick labels::

    fig.tick_labels.set_yposition('left')

* Set the style of the labels ('colons' or 'plain')::

    fig.tick_labels.set_style('colons')

* Set the font properties of the labels::

    fig.tick_labels.set_font(size='medium', weight='medium', \
                             stretch='normal', family='sans-serif', \
                             style='normal', variant='normal')

Ticks
^^^^^

The methods to control properties relating to the tick marks are the following:

* Show/hide all ticks::

    fig.ticks.show()
    fig.ticks.hide()

* Show/hide the x-axis ticks::

    fig.ticks.show_x()
    fig.ticks.hide_x()

* Show/hide the y-axis ticks::

    fig.ticks.show_y()
    fig.ticks.hide_y()

* Change the tick spacing for the x- and y-axis::

    fig.ticks.set_xspacing(0.04)  # degrees
    fig.ticks.set_yspacing(0.03)  # degrees

* Change the length of the ticks::

    fig.ticks.set_length(10)  # points

* Change the color of the ticks::

    fig.ticks.set_color('black')

* Set the line width for the ticks::

    fig.ticks.set_linewidth(2)  # points

* Set the number of minor ticks per major tick::

    fig.ticks.set_minor_frequency(5)

  Set this to ``1`` to get rid of minor ticks

Advanced
^^^^^^^^

To control whether to refresh the display after each command, use the following method::

    fig.set_auto_refresh(False)

To force a refresh, use::

    fig.refresh()

To use the system LaTeX instead of the matplotlib LaTeX, use::

    fig.set_system_latex(True)

The color for NaN values can be controlled using the following method::

    fig.set_nan_color('black')

The order of figure elements (eg lines, shapes, imagemap) can be controlled using the zorder parameter using for example::

    fig.show_ellipses(x_world, y_world, width, height, zorder=1)

Increasing integers from 0 will place elements towards the front.  Setting zorder=0 places layer at the bottom.

Finally, to change the look of the plot using pre-set themes, use::

    fig.set_theme('publication')
