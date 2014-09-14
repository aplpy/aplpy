import os

import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest
from astropy import units as u
from astropy.io import fits

from .. import FITSFigure


header_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/2d_fits')

HEADER = fits.Header.fromtextfile(os.path.join(header_dir, '1904-66_TAN.hdr'))
HDU = fits.PrimaryHDU(np.zeros((16, 16)), HEADER)


def test_scalebar_add_invalid():
    f = FITSFigure(HDU)
    with pytest.raises(TypeError):
        f.add_scalebar()


def test_scalebar_addremove():
    f = FITSFigure(HDU)
    f.add_scalebar(0.1)
    f.remove_scalebar()
    f.add_scalebar(0.1)
    f.close()


def test_scalebar_showhide():
    f = FITSFigure(HDU)
    f.add_scalebar(0.1)
    f.scalebar.hide()
    f.scalebar.show(0.1)
    f.close()


def test_scalebar_length():
    f = FITSFigure(HDU)
    f.add_scalebar(0.1)
    f.scalebar.set_length(0.01)
    f.scalebar.set_length(0.1)
    f.close()


@pytest.mark.parametrize('quantity', [1*u.arcsec, u.arcsec, 2*u.degree, 5*u.radian])
def test_scalebar_length_quantity(quantity):
    f = FITSFigure(HDU)
    f.add_scalebar(quantity)
    f.scalebar.set_length(quantity)
    f.close()


def test_scalebar_label():
    f = FITSFigure(HDU)
    f.add_scalebar(0.1)
    f.scalebar.set_label('1 pc')
    f.scalebar.set_label('5 AU')
    f.scalebar.set_label('2"')
    f.close()


def test_scalebar_corner():
    f = FITSFigure(HDU)
    f.add_scalebar(0.1)
    for corner in ['top', 'bottom', 'left', 'right', 'top left', 'top right',
                   'bottom left', 'bottom right']:
        f.scalebar.set_corner(corner)
    f.close()


def test_scalebar_frame():
    f = FITSFigure(HDU)
    f.add_scalebar(0.1)
    f.scalebar.set_frame(True)
    f.scalebar.set_frame(False)
    f.close()


def test_scalebar_color():
    f = FITSFigure(HDU)
    f.add_scalebar(0.1)
    f.scalebar.set_color('black')
    f.scalebar.set_color('#003344')
    f.scalebar.set_color((1.0, 0.4, 0.3))
    f.close()


def test_scalebar_alpha():
    f = FITSFigure(HDU)
    f.add_scalebar(0.1)
    f.scalebar.set_alpha(0.1)
    f.scalebar.set_alpha(0.2)
    f.scalebar.set_alpha(0.5)
    f.close()


def test_scalebar_font():
    f = FITSFigure(HDU)
    f.add_scalebar(0.1)
    f.scalebar.set_font(size='small', weight='bold', stretch='normal',
                        family='serif', style='normal', variant='normal')
    f.close()
