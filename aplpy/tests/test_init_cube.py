import os

import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest
from astropy.io import fits
import astropy.utils.exceptions as aue

from .helpers import generate_file, generate_hdu, generate_wcs
from .. import FITSFigure

# The tests in this file check that the initialization and basic plotting do
# not crash for FITS files with 3+ dimensions. No reference images are
# required here.

header_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/3d_fits')

HEADERS = [os.path.join(header_dir, 'cube.hdr')]

REFERENCE = os.path.join(header_dir, 'cube.hdr')

VALID_DIMENSIONS = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
INVALID_DIMENSIONS = [None, (1,), (0, 3), (-4, 2), (1, 1), (2, 2), (3, 3),
                      (1, 2, 3), (3, 5, 3, 2)]


# Test initialization through a filename
def test_file_init(tmpdir):
    filename = generate_file(REFERENCE, str(tmpdir))
    f = FITSFigure(filename, slices=[5])
    f.show_grayscale()
    f.close()


# Test initialization through an HDU object
def test_hdu_init():
    hdu = generate_hdu(REFERENCE)
    f = FITSFigure(hdu, slices=[5])
    f.show_grayscale()
    f.close()


# Test initialization through a WCS object (should not work)
def test_wcs_init():
    wcs = generate_wcs(REFERENCE)
    exc = ValueError if hasattr(wcs,'naxis1') else aue.AstropyDeprecationWarning
    with pytest.raises(exc):
        FITSFigure(wcs, slices=[5])


# Test initialization through an HDU object (no WCS)
def test_hdu_nowcs_init():
    data = np.zeros((16, 16, 16))
    hdu = fits.PrimaryHDU(data)
    f = FITSFigure(hdu, slices=[5])
    f.show_grayscale()
    f.close()


# Test initalization through a Numpy array (no WCS)
def test_numpy_nowcs_init():
    data = np.zeros((16, 16, 16))
    f = FITSFigure(data, slices=[5])
    f.show_grayscale()
    f.close()


# Test that initialization without specifying slices raises an exception for a
# true 3D cube
def test_hdu_noslices():
    hdu = generate_hdu(REFERENCE)
    with pytest.raises(Exception):
        FITSFigure(hdu)

# Test that initialization without specifying slices does *not* raise an
# exception if the remaining dimensions have size 1.
def test_hdu_noslices_2d():
    data = np.zeros((1, 16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.close()

# Now check initialization with valid and invalid dimensions. We just need to
# tes with HDU objects since we already tested that reading from files is ok.


# Test initialization with valid dimensions
@pytest.mark.parametrize(('dimensions'), VALID_DIMENSIONS)
def test_init_dimensions_valid(dimensions):
    hdu = generate_hdu(REFERENCE)
    f = FITSFigure(hdu, dimensions=dimensions, slices=[5])
    f.show_grayscale()
    f.close()


# Test initialization with invalid dimensions
@pytest.mark.parametrize(('dimensions'), INVALID_DIMENSIONS)
def test_init_dimensions_invalid(dimensions):
    hdu = generate_hdu(REFERENCE)
    with pytest.raises(ValueError):
        FITSFigure(hdu, dimensions=dimensions, slices=[5])


# Now check initialization of different WCS projections, and we check only
# valid dimensions

valid_parameters = []
for h in HEADERS:
    for d in VALID_DIMENSIONS:
        valid_parameters.append((h, d))


@pytest.mark.parametrize(('header', 'dimensions'), valid_parameters)
def test_init_extensive_wcs(tmpdir, header, dimensions):
    filename = generate_file(header, str(tmpdir))
    f = FITSFigure(filename, dimensions=dimensions, slices=[5])
    f.show_grayscale()
    f.close()

# Test that recenter works for cube slices
def test_hdu_nowcs_init():
    data = np.zeros((16, 16, 16))
    hdu = fits.PrimaryHDU(data)
    f = FITSFigure(hdu, slices=[5])
    f.show_grayscale()
    f.recenter(5., 5., width=3., height=3.)
    f.close()
