from __future__ import absolute_import, print_function, division

import pytest
import numpy as np

from .. import FITSFigure

# Test simple contour generation with Numpy example


@pytest.mark.parametrize(('filled'), [True, False])
def test_numpy_contour(filled):
    data = np.arange(256).reshape((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.show_contour(data, levels=np.linspace(1., 254., 10), filled=filled)
    f.close()
