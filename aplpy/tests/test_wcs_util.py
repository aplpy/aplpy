import os

import numpy as np
from astropy.io import fits
from astropy.tests.helper import pytest

from ..wcs_util import WCS, celestial_pixel_scale, non_celestial_pixel_scales

from .helpers import generate_wcs

HEADER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
HEADER_2D = fits.Header.fromtextfile(os.path.join(HEADER_DIR, '2d_fits', '1904-66_TAN.hdr'))
HEADER_3D = fits.Header.fromtextfile(os.path.join(HEADER_DIR, '3d_fits', 'cube.hdr'))


def test_pixel_scale_matrix_1():
    wcs = WCS(HEADER_2D)
    np.testing.assert_allclose(wcs.pixel_scale_matrix, [[-0.06666667, 0.], [0., 0.06666667]])


def test_celestial_scale_1():
    wcs = WCS(HEADER_2D)
    for crota2 in range(0, 360, 20):
        wcs.wcs.crota = [0.,crota2]
        np.testing.assert_allclose(celestial_pixel_scale(wcs), 0.06666667)


def test_non_celestial_scales_1():
    wcs = WCS(HEADER_2D)
    with pytest.raises(ValueError) as exc:
        non_celestial_pixel_scales(wcs)
    assert exc.value.args[0] == "WCS is celestial, use celestial_pixel_scale instead"


def test_pixel_scale_matrix_2():
    wcs = WCS(HEADER_3D, dimensions=[0,2], slices=[0])
    np.testing.assert_allclose(wcs.pixel_scale_matrix, [[-6.38888900e-03, 0.], [0., 6.64236100e+01]])


def test_celestial_scale_2():
    wcs = WCS(HEADER_3D, dimensions=[0,2], slices=[0])
    with pytest.raises(ValueError) as exc:
        celestial_pixel_scale(wcs)
    assert exc.value.args[0] == "WCS is not celestial, cannot determine celestial pixel scale"


def test_non_celestial_scales_2():
    wcs = WCS(HEADER_3D, dimensions=[0,2], slices=[0])
    np.testing.assert_allclose(non_celestial_pixel_scales(wcs), [6.38888900e-03, 6.64236100e+01])
