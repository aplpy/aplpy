from __future__ import absolute_import, print_function, division

import numpy as np
from astropy.io import fits

from .. import FITSFigure

ARRAY = np.arange(256).reshape((16, 16))


def test_convolve_default():
    hdu = fits.PrimaryHDU(ARRAY)
    f = FITSFigure(hdu)
    f.show_grayscale(smooth=3)
    f.close()


def test_convolve_gauss():
    hdu = fits.PrimaryHDU(ARRAY)
    f = FITSFigure(hdu)
    f.show_grayscale(kernel='gauss', smooth=3)
    f.close()


def test_convolve_box():
    hdu = fits.PrimaryHDU(ARRAY)
    f = FITSFigure(hdu)
    f.show_grayscale(kernel='box', smooth=3)
    f.close()


def test_convolve_custom():
    hdu = fits.PrimaryHDU(ARRAY)
    f = FITSFigure(hdu)
    f.show_grayscale(kernel=np.ones((3, 3)))
    f.close()


def test_convolve_int():
    # Regression test for aplpy/aplpy#165
    hdu = fits.PrimaryHDU(ARRAY)
    f = FITSFigure(hdu)
    f.show_grayscale(smooth=3)
    f.close()
