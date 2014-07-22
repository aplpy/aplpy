# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
APLpy : Astronomical Plotting Library in Python
"""

# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *
# ----------------------------------------------------------------------------

if not _ASTROPY_SETUP_:

    from .core import FITSFigure
    from .rgb import make_rgb_image, make_rgb_cube

    from .frame import Frame
    from .overlays import Scalebar, Beam
    from .colorbar import Colorbar
    from .grid import Grid
    from .ticks import Ticks
    from .labels import TickLabels
    from .axis_labels import AxisLabels
