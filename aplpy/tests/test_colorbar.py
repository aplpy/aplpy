from __future__ import absolute_import, print_function, division

import numpy as np
from astropy.tests.helper import pytest

from .. import FITSFigure

ARRAY = np.arange(256).reshape((16, 16))


def test_colorbar_invalid():
    f = FITSFigure(ARRAY)
    with pytest.raises(Exception):
        f.add_colorbar()  # no grayscale/colorscale was shown


def test_colorbar_addremove():
    f = FITSFigure(ARRAY)
    f.show_grayscale()
    f.add_colorbar()
    f.remove_colorbar()
    f.add_colorbar()
    f.close()


def test_colorbar_showhide():
    f = FITSFigure(ARRAY)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.hide()
    f.colorbar.show()
    f.close()


def test_colorbar_location():
    f = FITSFigure(ARRAY)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_location('top')
    with pytest.warns(UserWarning, match='Bottom colorbar not fully implemented'):
        f.colorbar.set_location('bottom')
    with pytest.warns(UserWarning, match='Left colorbar not fully implemented'):
        f.colorbar.set_location('left')
    f.colorbar.set_location('right')
    f.close()


def test_colorbar_width():
    f = FITSFigure(ARRAY)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_width(0.1)
    f.colorbar.set_width(0.2)
    f.colorbar.set_width(0.5)
    f.close()


def test_colorbar_pad():
    f = FITSFigure(ARRAY)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_pad(0.1)
    f.colorbar.set_pad(0.2)
    f.colorbar.set_pad(0.5)
    f.close()


def test_colorbar_font():
    f = FITSFigure(ARRAY)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_font(size='small', weight='bold', stretch='normal',
                        family='serif', style='normal', variant='normal')
    f.close()


def test_colorbar_axis_label():
    f = FITSFigure(ARRAY)
    f.show_grayscale()
    f.add_colorbar()
    f.colorbar.set_axis_label_text('Surface Brightness (MJy/sr)')
    f.colorbar.set_axis_label_rotation(45.)
    f.colorbar.set_axis_label_font(size='small', weight='bold', stretch='normal',
                                   family='serif', style='normal', variant='normal')
    f.colorbar.set_axis_label_pad(5.)
    f.close()
