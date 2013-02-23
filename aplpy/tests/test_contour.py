import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest

from .. import FITSFigure

# Test simple contour generation with Numpy example


@pytest.mark.parametrize(('filled'), [True, False])
def test_numpy_contour(filled):
    data = np.arange(256).reshape((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.show_contour(data, levels=np.linspace(1., 254., 10), filled=filled)
    f.close()
