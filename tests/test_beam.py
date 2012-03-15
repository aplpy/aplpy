import matplotlib
matplotlib.use('Agg')

import numpy as np
import pytest

from aplpy import FITSFigure

# Test simple contour generation with Numpy example


def test_numpy_beam():
    data = np.arange(256).reshape((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.close()
