import matplotlib
matplotlib.use('Agg')

import numpy as np
import pytest

import aplpy


def test_frame_linewidth():
    data = np.zeros((16, 16))
    f = aplpy.FITSFigure(data)
    f.frame.set_linewidth(0)
    f.frame.set_linewidth(1)
    f.frame.set_linewidth(10)
    f.close()


def test_frame_color():
    data = np.zeros((16, 16))
    f = aplpy.FITSFigure(data)
    f.frame.set_color('black')
    f.frame.set_color('#003344')
    f.frame.set_color((1.0, 0.4, 0.3))
    f.close()

