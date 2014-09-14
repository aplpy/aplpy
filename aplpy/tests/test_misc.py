import numpy as np
from astropy.io import fits

from ..core import FITSFigure


def test_nan_color_copy():
    """
    Regression test to ensure that NaN values set in one image don't affect
    global Matplotlib colormap.
    """

    data = np.zeros((16, 16))

    f1 = FITSFigure(data)
    f1.show_grayscale()
    f1.set_nan_color('blue')

    f2 = FITSFigure(data)
    f2.show_grayscale()
    f2.set_nan_color('red')

    assert f1.image.get_cmap()._rgba_bad == (0.0, 0.0, 1.0, 1.0) 
    assert f2.image.get_cmap()._rgba_bad == (1.0, 0.0, 0.0, 1.0) 