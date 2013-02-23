import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest

from .. import FITSFigure


def test_grid_addremove():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_grid()
    f.remove_grid()
    f.add_grid()
    f.close()


def test_grid_showhide():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_grid()
    f.grid.hide()
    f.grid.show()
    f.close()


def test_grid_spacing():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_grid()
    f.grid.set_xspacing(1.)
    f.grid.set_xspacing('tick')
    with pytest.raises(ValueError):
        f.grid.set_xspacing('auto')
    f.grid.set_yspacing(2.)
    f.grid.set_yspacing('tick')
    with pytest.raises(ValueError):
        f.grid.set_yspacing('auto')
    f.close()


def test_grid_color():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_grid()
    f.grid.set_color('black')
    f.grid.set_color('#003344')
    f.grid.set_color((1.0, 0.4, 0.3))
    f.close()


def test_grid_alpha():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_grid()
    f.grid.set_alpha(0.0)
    f.grid.set_alpha(0.3)
    f.grid.set_alpha(1.0)
    f.close()


def test_grid_linestyle():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_grid()
    f.grid.set_linestyle('solid')
    f.grid.set_linestyle('dashed')
    f.grid.set_linestyle('dotted')
    f.close()


def test_grid_linewidth():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_grid()
    f.grid.set_linewidth(0)
    f.grid.set_linewidth(2)
    f.grid.set_linewidth(5)
    f.close()
