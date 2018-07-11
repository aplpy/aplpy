from __future__ import absolute_import, print_function, division

import numpy as np
from astropy.tests.helper import pytest
from itertools import product

from .. import FITSFigure

# Test simple contour generation with Numpy example


@pytest.mark.parametrize(('filled', 'rasterize'),
                         product([True, False], [True, False]))
def test_numpy_contour(filled, rasterize):
    data = np.arange(256).reshape((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.show_contour(data, levels=np.linspace(1., 254., 10), filled=filled,
                   rasterize=rasterize)
    f.close()
