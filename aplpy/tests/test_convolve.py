import os

import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest
from astropy.io import fits
from astropy.wcs import WCS as AstropyWCS

from .helpers import generate_file, generate_hdu, generate_wcs
from .. import FITSFigure


def test_convolve_default():
    data = np.random.random((16, 16))
    hdu = fits.PrimaryHDU(data)
    f = FITSFigure(hdu)
    f.show_grayscale(smooth=3)
    f.close()


def test_convolve_gauss():
    data = np.random.random((16, 16))
    hdu = fits.PrimaryHDU(data)
    f = FITSFigure(hdu)
    f.show_grayscale(kernel='gauss', smooth=3)
    f.close()


def test_convolve_box():
    data = np.random.random((16, 16))
    hdu = fits.PrimaryHDU(data)
    f = FITSFigure(hdu)
    f.show_grayscale(kernel='box', smooth=3)
    f.close()


def test_convolve_custom():
    data = np.random.random((16, 16))
    hdu = fits.PrimaryHDU(data)
    f = FITSFigure(hdu)
    f.show_grayscale(kernel=np.ones((3,3)))
    f.close()


def test_convolve_default():
    # Regression test for aplpy/aplpy#165
    data = np.ones((16, 16), dtype=int)
    hdu = fits.PrimaryHDU(data)
    f = FITSFigure(hdu)
    f.show_grayscale(smooth=3)
    f.close()
