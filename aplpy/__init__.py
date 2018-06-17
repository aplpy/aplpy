# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
APLpy : Astronomical Plotting Library in Python
"""

# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *  # noqa
# ----------------------------------------------------------------------------

if not _ASTROPY_SETUP_:  # noqa

    from .core import FITSFigure  # noqa
    from .rgb import make_rgb_image, make_rgb_cube  # noqa

    from .frame import Frame  # noqa
    from .overlays import Scalebar, Beam  # noqa
    from .colorbar import Colorbar  # noqa
    from .grid import Grid  # noqa
    from .ticks import Ticks  # noqa
    from .tick_labels import TickLabels  # noqa
    from .axis_labels import AxisLabels  # noqa
