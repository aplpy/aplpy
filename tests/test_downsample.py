import matplotlib
matplotlib.use('Agg')

import numpy as np
import pytest

import aplpy

# Test simple contour generation with Numpy example
def test_numpy_downsample():
    data = np.arange(256).reshape((16, 16))
    f = aplpy.FITSFigure(data, downsample=2)
    f.show_grayscale()
    f.close()
    
