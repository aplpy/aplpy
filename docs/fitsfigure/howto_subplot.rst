Creating subplots
-----------------

By default, :class:`~aplpy.aplpy.FITSFigure` creates a figure with a single
subplot that occupies the entire figure. However, APLpy can be used to place a
subplot in an existing matplotlib figure instance. To do this,
:class:`~aplpy.aplpy.FITSFigure` should be called with the ``figure=``
argument as follows::

    import aplpy
    import matplotlib.pyplot as mpl
    
     fig = mpl.figure()
     f = aplpy.FITSFigure('some_image.fits', figure=fig)
    
The above will place a subplot inside the ``fig`` figure instance. The ``f``
object can be used as normal to control the FITS figure inside the
subplot. The above however is not very interesting compared to just
creating a FITSFigure instance from scratch. What this is useful for is
only using sub-regions of the figure to display the FITS data, to leave
place for other subplots, whether histograms, scatter, or other matplotlib
plots, or another FITS Figure. This can be done using the ``subplot``
argument. From the docstring for FITSFigure::
    
    *subplot*: [ list of four floats ]
        If specified, a subplot will be added at this position. The list
        should contain [xmin, ymin, dx, dy] where xmin and ymin are the
        position of the bottom left corner of the subplot, and dx and dy are
        the width and height of the subplot respectively. These should all be
        given in units of the figure width and height. For example, [0.1, 0.1,
        0.8, 0.8] will almost fill the entire figure, leaving a 10 percent
        margin on all sides.
    
The following code outline illustrates how to create a rectangular figure with
two FITS images::

    import aplpy
    import matplotlib.pyplot as mpl

    fig = mpl.figure(figsize=(15, 7))

    f1 = aplpy.FITSFigure('image_1.fits', figure=fig, subplot=[0.1,0.1,0.35,0.8])
    f1.set_tick_labels_font(size='x-small')
    f1.set_axis_labels_font(size='small')
    f1.show_grayscale()

    f2 = aplpy.FITSFigure('image_2.fits', figure=fig, subplot=[0.5,0.1,0.35,0.8])
    f2.set_tick_labels_font(size='x-small')
    f2.set_axis_labels_font(size='small')
    f2.show_grayscale()

    f2.hide_yaxis_label()
    f2.hide_ytick_labels()

    fig.canvas.draw()
    
The ``hide`` methods shown above are especially useful when working with
subplots, as in some cases there is no need to repeat the tick labels. Alternatively figures can be constructed from both APLpy figures and normal matplotlib axes::

    import aplpy
    import matplotlib.pyplot as mpl

    fig = mpl.figure(figsize=(15, 7))

    f1 = aplpy.FITSFigure('image_1.fits', figure=fig, subplot=[0.1,0.1,0.35,0.8])
    f1.set_tick_labels_font(size='x-small')
    f1.set_axis_labels_font(size='small')
    f1.show_grayscale()

    ax2 = fig.add_axes([0.5,0.1,0.35,0.8])
    
    # some code here with ax2

    fig.canvas.draw()
