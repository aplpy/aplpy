Complete API
-------------

.. toctree::
  :maxdepth: 1

Initialization
^^^^^^^^^^^^^^

.. automodule:: aplpy
.. autoclass:: FITSFigure
   :members: __init__
   
General routines
^^^^^^^^^^^^^^^^

.. automethod:: FITSFigure.show_grayscale
.. automethod:: FITSFigure.hide_grayscale
.. automethod:: FITSFigure.show_colorscale
.. automethod:: FITSFigure.hide_colorscale
.. automethod:: FITSFigure.show_rgb
.. automethod:: FITSFigure.recenter
.. automethod:: FITSFigure.show_contour
.. automethod:: FITSFigure.save

Labels
^^^^^^

.. automethod:: FITSFigure.add_label
   
Shapes
^^^^^^^

.. automethod:: FITSFigure.show_markers
.. automethod:: FITSFigure.show_circles
.. automethod:: FITSFigure.show_ellipses
.. automethod:: FITSFigure.show_rectangles
.. automethod:: FITSFigure.show_lines
.. automethod:: FITSFigure.show_polygons
.. automethod:: FITSFigure.show_arrows
   
Layers
^^^^^^

.. automethod:: FITSFigure.list_layers
.. automethod:: FITSFigure.remove_layer
.. automethod:: FITSFigure.hide_layer
.. automethod:: FITSFigure.show_layer
.. automethod:: FITSFigure.get_layer

Coordinates
^^^^^^^^^^^

.. automethod:: FITSFigure.world2pixel
.. automethod:: FITSFigure.pixel2world
   
.. automodule:: aplpy.frame

Frame
^^^^^

.. autoclass:: Frame
    :members:

.. automodule:: aplpy

Colorbar
^^^^^^^^

.. automethod:: FITSFigure.add_colorbar
.. automethod:: FITSFigure.remove_colorbar

.. automodule:: aplpy.colorbar
.. autoclass:: Colorbar
    :members:

.. automodule:: aplpy

Coordinate Grid
^^^^^^^^^^^^^^^

.. automethod:: FITSFigure.add_grid
.. automethod:: FITSFigure.remove_grid

.. automodule:: aplpy.grid
.. autoclass:: Grid
    :members:

.. automodule:: aplpy

Scalebar
^^^^^^^^

.. automethod:: FITSFigure.add_scalebar
.. automethod:: FITSFigure.remove_scalebar

.. automodule:: aplpy.overlays
.. autoclass:: ScaleBar
    :members:

.. automodule:: aplpy

Beam
^^^^

.. automethod:: FITSFigure.add_beam
.. automethod:: FITSFigure.remove_beam

.. automodule:: aplpy.overlays
.. autoclass:: Beam
    :members:
    
.. automodule:: aplpy.axis_labels

Axis labels
^^^^^^^^^^^^^^^^

.. autoclass:: AxisLabels
    :members:


.. automodule:: aplpy.labels

Tick labels
^^^^^^^^^^^^^^^^

.. autoclass:: TickLabels
    :members:

.. automodule:: aplpy.ticks

Ticks
^^^^^^^^^^^^^^^^

.. autoclass:: Ticks
    :members:

.. automodule:: aplpy

Advanced
^^^^^^^^

.. automethod:: FITSFigure.set_auto_refresh
.. automethod:: FITSFigure.refresh
.. automethod:: FITSFigure.set_system_latex

.. automodule:: aplpy

RGB Images
^^^^^^^^^^

.. autofunction:: aplpy.make_rgb_cube
.. autofunction:: aplpy.make_rgb_image



