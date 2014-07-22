import os

import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest
from astropy.io import fits
from astropy.wcs import WCS as AstropyWCS
import astropy.utils.exceptions as aue

from .helpers import generate_file, generate_hdu, generate_wcs
from .. import FITSFigure

# The tests in this file check that the initialization and basic plotting do
# not crash for FITS files with 2 dimensions. No reference images are
# required here.

header_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/2d_fits')

HEADERS = [os.path.join(header_dir, '1904-66_AIR.hdr'),
           os.path.join(header_dir, '1904-66_AIT.hdr'),
           os.path.join(header_dir, '1904-66_ARC.hdr'),
           os.path.join(header_dir, '1904-66_AZP.hdr'),
           os.path.join(header_dir, '1904-66_BON.hdr'),
           os.path.join(header_dir, '1904-66_CAR.hdr'),
           os.path.join(header_dir, '1904-66_CEA.hdr'),
           os.path.join(header_dir, '1904-66_COD.hdr'),
           os.path.join(header_dir, '1904-66_COE.hdr'),
           os.path.join(header_dir, '1904-66_COO.hdr'),
           os.path.join(header_dir, '1904-66_COP.hdr'),
           os.path.join(header_dir, '1904-66_CSC.hdr'),
           os.path.join(header_dir, '1904-66_CYP.hdr'),
           os.path.join(header_dir, '1904-66_HPX.hdr'),
           os.path.join(header_dir, '1904-66_MER.hdr'),
           os.path.join(header_dir, '1904-66_MOL.hdr'),
           os.path.join(header_dir, '1904-66_NCP.hdr'),
           os.path.join(header_dir, '1904-66_PAR.hdr'),
           os.path.join(header_dir, '1904-66_PCO.hdr'),
           os.path.join(header_dir, '1904-66_QSC.hdr'),
           os.path.join(header_dir, '1904-66_SFL.hdr'),
           os.path.join(header_dir, '1904-66_SIN.hdr'),
           os.path.join(header_dir, '1904-66_STG.hdr'),
           os.path.join(header_dir, '1904-66_SZP.hdr'),
           os.path.join(header_dir, '1904-66_TAN.hdr'),
           os.path.join(header_dir, '1904-66_TSC.hdr'),
           os.path.join(header_dir, '1904-66_ZEA.hdr'),
           os.path.join(header_dir, '1904-66_ZPN.hdr')]

REFERENCE = os.path.join(header_dir, '1904-66_TAN.hdr')

CAR_REFERENCE = os.path.join(header_dir, '1904-66_CAR.hdr')

VALID_DIMENSIONS = [(0, 1), (1, 0)]
INVALID_DIMENSIONS = [None, (1,), (0, 2), (-4, 2), (1, 1), (2, 2), (1, 2, 3)]


# Test initialization through a filename
def test_file_init(tmpdir):
    filename = generate_file(REFERENCE, str(tmpdir))
    f = FITSFigure(filename)
    f.show_grayscale()
    f.close()


# Test initialization through an HDU object
def test_hdu_init():
    hdu = generate_hdu(REFERENCE)
    f = FITSFigure(hdu)
    f.show_grayscale()
    f.close()


# Test initialization through a WCS object
def test_wcs_init():
    wcs = generate_wcs(REFERENCE)
    if hasattr(wcs,'naxis1'):
        f = FITSFigure(wcs)
        f.show_grayscale()
        f.close()
    else:
        with pytest.raises(aue.AstropyDeprecationWarning):
            f = FITSFigure(wcs)


# Test initialization through a WCS object with wcs.to_header() as a go-between
# specifically for testing the cd -> pc -> cd hack, and has particular importance
# for AVM-generated headers
def test_wcs_toheader_init():
    wcs = generate_wcs(REFERENCE)
    header_ = fits.Header.fromtextfile(REFERENCE)
    header = wcs.to_header()
    wcs2 = AstropyWCS(header)
    wcs2.naxis1 = wcs.naxis1 = header_['NAXIS1']
    wcs2.naxis2 = wcs.naxis2 = header_['NAXIS2']
    f = FITSFigure(wcs2)
    f.show_grayscale()
    f.add_grid()
    f.close()


# Test initialization through an HDU object (no WCS)
def test_hdu_nowcs_init():
    data = np.zeros((16, 16))
    hdu = fits.PrimaryHDU(data)
    f = FITSFigure(hdu)
    f.show_grayscale()
    f.close()


# Test initalization through a Numpy array (no WCS)
def test_numpy_nowcs_init():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.close()


# Now check initialization with valid and invalid dimensions. We just need to
# tes with HDU objects since we already tested that reading from files is ok.

# Test initialization with valid dimensions
@pytest.mark.parametrize(('dimensions'), VALID_DIMENSIONS)
def test_init_dimensions_valid(dimensions):
    hdu = generate_hdu(REFERENCE)
    f = FITSFigure(hdu, dimensions=dimensions)
    f.show_grayscale()
    f.close()

# Test initialization with invalid dimensions


@pytest.mark.parametrize(('dimensions'), INVALID_DIMENSIONS)
def test_init_dimensions_invalid(dimensions):
    hdu = generate_hdu(REFERENCE)
    with pytest.raises(ValueError):
        FITSFigure(hdu, dimensions=dimensions)

# Now check initialization of different WCS projections, and we check only
# valid dimensions

valid_parameters = []
for h in HEADERS:
    for d in VALID_DIMENSIONS:
        valid_parameters.append((h, d))


@pytest.mark.parametrize(('header', 'dimensions'), valid_parameters)
def test_init_extensive_wcs(header, dimensions):
    hdu = generate_hdu(header)
    if 'CAR' in header:
        f = FITSFigure(hdu, dimensions=dimensions, convention='calabretta')
    else:
        f = FITSFigure(hdu, dimensions=dimensions)
    f.show_grayscale()
    f.add_grid()
    f.close()

# Check that for CAR projections, an exception is raised if no convention is specified


@pytest.mark.parametrize(('dimensions'), VALID_DIMENSIONS)
def test_init_car_invalid(dimensions):
    hdu = generate_hdu(CAR_REFERENCE)
    with pytest.raises(Exception):
        FITSFigure(hdu, dimensions=dimensions)

# Check that images containing only NaN or Inf values don't crash FITSFigure
def test_init_only_naninf():
    data = np.ones((10,10)) * np.nan
    data[::2,::2] = np.inf
    f = FITSFigure(data)
    f.show_grayscale()
    f.show_colorscale()


def test_init_single_pixel():
    data = np.zeros((4,4))
    data[...] = np.nan
    data[2,2] = 1
    f = FITSFigure(data)
    f.show_grayscale()
