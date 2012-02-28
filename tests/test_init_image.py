import matplotlib
matplotlib.use('Agg')

import aplpy
import pytest

from helpers import generate_file, generate_hdu, generate_wcs

# The tests in this file check that the initialization and basic plotting do
# not crash for FITS files with 2 dimensions. No reference images are
# required here.

HEADERS = ['data/2d_fits/1904-66_AIR.hdr',
           'data/2d_fits/1904-66_AIT.hdr',
           'data/2d_fits/1904-66_ARC.hdr',
           'data/2d_fits/1904-66_AZP.hdr',
           'data/2d_fits/1904-66_BON.hdr',
           'data/2d_fits/1904-66_CAR.hdr',
           'data/2d_fits/1904-66_CEA.hdr',
           'data/2d_fits/1904-66_COD.hdr',
           'data/2d_fits/1904-66_COE.hdr',
           'data/2d_fits/1904-66_COO.hdr',
           'data/2d_fits/1904-66_COP.hdr',
           'data/2d_fits/1904-66_CSC.hdr',
           'data/2d_fits/1904-66_CYP.hdr',
           'data/2d_fits/1904-66_HPX.hdr',
           'data/2d_fits/1904-66_MER.hdr',
           'data/2d_fits/1904-66_MOL.hdr',
           'data/2d_fits/1904-66_NCP.hdr',
           'data/2d_fits/1904-66_PAR.hdr',
           'data/2d_fits/1904-66_PCO.hdr',
           'data/2d_fits/1904-66_QSC.hdr',
           'data/2d_fits/1904-66_SFL.hdr',
           'data/2d_fits/1904-66_SIN.hdr',
           'data/2d_fits/1904-66_STG.hdr',
           'data/2d_fits/1904-66_SZP.hdr',
           'data/2d_fits/1904-66_TAN.hdr',
           'data/2d_fits/1904-66_TSC.hdr',
           'data/2d_fits/1904-66_ZEA.hdr',
           'data/2d_fits/1904-66_ZPN.hdr']

REFERENCE = 'data/2d_fits/1904-66_TAN.hdr'

CAR_REFERENCE = 'data/2d_fits/1904-66_CAR.hdr'

VALID_DIMENSIONS = [(0, 1), (1, 0)]
INVALID_DIMENSIONS = [None, (1,), (0, 2), (-4, 2), (1, 1), (2, 2), (1, 2, 3)]


# Test initialization through a filename
def test_file_init(tmpdir):
    filename = generate_file(REFERENCE, str(tmpdir))
    f = aplpy.FITSFigure(filename)
    f.show_grayscale()
    f.close()


# Test initialization through an HDU object
def test_hdu_init_valid():
    hdu = generate_hdu(REFERENCE)
    f = aplpy.FITSFigure(hdu)
    f.show_grayscale()
    f.close()


# Test initialization through a WCS object
def test_wcs_init_valid():
    wcs = generate_wcs(REFERENCE)
    f = aplpy.FITSFigure(wcs)
    f.show_grayscale()
    f.close()

# Now check initialization with valid and invalid dimensions. We just need to
# tes with HDU objects since we already tested that reading from files is ok.

# Test initialization with valid dimensions
@pytest.mark.parametrize(('dimensions'), VALID_DIMENSIONS)
def test_init_dimensions_valid(dimensions):
    hdu = generate_hdu(REFERENCE)
    f = aplpy.FITSFigure(hdu, dimensions=dimensions)
    f.show_grayscale()
    f.close()

# Test initialization with invalid dimensions
@pytest.mark.parametrize(('dimensions'), INVALID_DIMENSIONS)
def test_init_dimensions_invalid(dimensions):
    hdu = generate_hdu(REFERENCE)
    with pytest.raises(Exception):
        aplpy.FITSFigure(hdu, dimensions=dimensions)

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
        f = aplpy.FITSFigure(hdu, dimensions=dimensions, convention='calabretta')
    else:
        f = aplpy.FITSFigure(hdu, dimensions=dimensions)
    f.show_grayscale()
    f.add_grid()
    f.close()

# Check that for CAR projections, an exception is raised if no convention is specified
@pytest.mark.parametrize(('dimensions'), VALID_DIMENSIONS)
def test_init_car_invalid(dimensions):
    hdu = generate_hdu(CAR_REFERENCE)
    with pytest.raises(Exception):
        f = aplpy.FITSFigure(hdu, dimensions=dimensions)
