from __future__ import absolute_import, print_function, division

import os

import pytest
import numpy as np
from astropy import units as u
from astropy.io import fits

from .. import FITSFigure


ROOT = os.path.dirname(os.path.abspath(__file__))
HEADER_DIR = os.path.join(ROOT, 'data/2d_fits')
HEADER = fits.Header.fromtextfile(os.path.join(HEADER_DIR, '1904-66_TAN.hdr'))
HDU = fits.PrimaryHDU(np.zeros((16, 16)), HEADER)


def test_compass_addremove():
    f = FITSFigure(HDU)
    f.add_compass()
    f.remove_compass()
    f.add_compass()
    f.close()


def test_compass_showhide():
    f = FITSFigure(HDU)
    f.add_compass()
    f.compass.hide()
    f.compass.show()
    f.close()


def test_compass_length():
    f = FITSFigure(HDU)
    f.add_compass(length=0.15)
    f.compass.set_length(0.01)
    f.compass.set_length(0.15)
    f.close()


@pytest.mark.parametrize('quantity', [1 * u.arcsec, u.arcsec, 2 * u.degree, 5 * u.radian])
def test_compass_length_quantity(quantity):
    f = FITSFigure(HDU)
    f.add_compass(length=quantity)
    f.compass.set_length(quantity)
    f.close()


def test_compass_corner():
    f = FITSFigure(HDU)
    f.add_compass()
    for corner in ['top', 'bottom', 'left', 'right', 'top left', 'top right',
                   'bottom left', 'bottom right']:
        f.compass.set_corner(corner)
    f.close()


def test_compass_frame():
    f = FITSFigure(HDU)
    f.add_compass()
    f.compass.set_frame(True)
    f.compass.set_frame(False)
    f.close()


def test_compass_color():
    f = FITSFigure(HDU)
    f.add_compass()
    f.compass.set_color('black')
    f.compass.set_color('#003344')
    f.compass.set_color((1.0, 0.4, 0.3))
    f.close()


def test_compass_alpha():
    f = FITSFigure(HDU)
    f.add_compass()
    f.compass.set_alpha(0.1)
    f.compass.set_alpha(0.2)
    f.compass.set_alpha(0.5)
    f.close()


def test_compass_linestyle():
    f = FITSFigure(HDU)
    f.add_compass()
    f.compass.set_linestyle('solid')
    f.compass.set_linestyle('dotted')
    f.compass.set_linestyle('dashed')
    f.close()


def test_compass_linewidth():
    f = FITSFigure(HDU)
    f.add_compass()
    f.compass.set_linewidth(0)
    f.compass.set_linewidth(1)
    f.compass.set_linewidth(5)
    f.close()


def test_compass_font():
    f = FITSFigure(HDU)
    f.add_compass()
    f.compass.set_font(size='small', weight='bold', stretch='normal',
                       family='serif', style='normal', variant='normal')
    f.close()
