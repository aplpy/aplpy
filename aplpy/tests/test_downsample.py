from __future__ import absolute_import, print_function, division

import pytest
import numpy as np

try:
    import skimage  # noqa
except ImportError:
    SKIMAGE_INSTALLED = False
else:
    SKIMAGE_INSTALLED = True

from .. import FITSFigure


@pytest.mark.skipif("not SKIMAGE_INSTALLED")
def test_numpy_downsample():
    data = np.arange(256).reshape((16, 16))
    f = FITSFigure(data, downsample=2)
    f.show_grayscale()
    f.close()
