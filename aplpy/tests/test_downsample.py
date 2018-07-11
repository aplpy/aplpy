from __future__ import absolute_import, print_function, division

import numpy as np

from .. import FITSFigure


def test_numpy_downsample():
    data = np.arange(256).reshape((16, 16))
    f = FITSFigure(data, downsample=2)
    f.show_grayscale()
    f.close()
