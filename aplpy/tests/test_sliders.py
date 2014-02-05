import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest

from .. import FITSFigure

def test_add_sliders():
    data = np.random.randn(16, 16)
    F = FITSFigure(data)
    F.show_grayscale()
    F.show_sliders()
    fignum = F.Sliders.toolfig.number
    F.show_sliders()
    # make sure showing sliders twice doesn't make a new instance
    assert F.Sliders.toolfig.number == fignum
    F.hide_sliders()


def test_add_log_sliders():
    data = np.random.randn(16, 16)
    F = FITSFigure(data)
    F.show_grayscale(stretch='log')
    F.show_sliders()
    fignum = F.Sliders.toolfig.number
    F.show_sliders()
    # make sure showing sliders twice doesn't make a new instance
    assert F.Sliders.toolfig.number == fignum
    F.hide_sliders()

