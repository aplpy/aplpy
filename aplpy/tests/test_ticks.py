import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest

from .. import FITSFigure


def test_ticks_show_hide():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.ticks.hide()
    f.ticks.show()
    f.ticks.hide_x()
    f.ticks.show_x()
    f.ticks.hide_y()
    f.ticks.show_y()
    f.close()


def test_ticks_spacing():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.ticks.set_xspacing(0.5)
    f.ticks.set_xspacing(1.)
    f.ticks.set_yspacing(0.5)
    f.ticks.set_yspacing(1.)
    f.close()


def test_ticks_length():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.ticks.set_length(0)
    f.ticks.set_length(1)
    f.ticks.set_length(10)
    f.close()


def test_ticks_color():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.ticks.set_color('black')
    f.ticks.set_color('#003344')
    f.ticks.set_color((1.0, 0.4, 0.3))
    f.close()


def test_ticks_linewidth():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.ticks.set_linewidth(1)
    f.ticks.set_linewidth(3)
    f.ticks.set_linewidth(10)
    f.close()


def test_ticks_minor_frequency():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.ticks.set_minor_frequency(1)
    f.ticks.set_minor_frequency(5)
    f.ticks.set_minor_frequency(10)
    f.close()
