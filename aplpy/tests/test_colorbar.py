import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest

from .. import FITSFigure


def test_colorbar_invalid():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    with pytest.raises(Exception):
        f.add_colorbar()  # no grayscale/colorscale was shown


def test_colorbar_addremove():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_colorbar()
    f.remove_colorbar()
    f.add_colorbar()
    f.close()


def test_colorbar_showhide():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.hide()
    f.colorbar.show()
    f.close()


def test_colorbar_location():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_location('top')
    f.colorbar.set_location('bottom')
    f.colorbar.set_location('left')
    f.colorbar.set_location('right')
    f.close()


def test_colorbar_width():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_width(0.1)
    f.colorbar.set_width(0.2)
    f.colorbar.set_width(0.5)
    f.close()


def test_colorbar_pad():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_pad(0.1)
    f.colorbar.set_pad(0.2)
    f.colorbar.set_pad(0.5)
    f.close()


def test_colorbar_font():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_font(size='small', weight='bold', stretch='normal',
                        family='serif', style='normal', variant='normal')
    f.close()


def test_colorbar_axis_label():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_axis_label_text('Flux (MJy/sr)')
    f.colorbar.set_axis_label_rotation(45.)
    f.colorbar.set_axis_label_font(size='small', weight='bold', stretch='normal',
                                   family='serif', style='normal', variant='normal')
    f.colorbar.set_axis_label_pad(5.)
    f.close()