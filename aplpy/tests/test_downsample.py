import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest

from .. import FITSFigure

# Test simple contour generation with Numpy example


def test_numpy_downsample():
    data = np.arange(256).reshape((16, 16))
    f = FITSFigure(data, downsample=2)
    f.show_grayscale()
    f.close()
