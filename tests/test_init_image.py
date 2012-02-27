import matplotlib
matplotlib.use('Agg')

import pyfits
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


VALID_DIMENSIONS = [(0, 1), (1, 0)]
INVALID_DIMENSIONS = [None, (1,), (0, 2), (-4, 2), (1, 1), (2, 2), (1, 2, 3)]

valid_parameters = []
for h in HEADERS:
    for d in VALID_DIMENSIONS:
        valid_parameters.append((h, d))

invalid_parameters = []
for h in HEADERS:
    for d in INVALID_DIMENSIONS:
        invalid_parameters.append((h, d))


@pytest.mark.parametrize(('header', 'dimensions'), valid_parameters)
def test_file_init_valid(tmpdir, header, dimensions):
    filename = generate_file(header, str(tmpdir))
    f = aplpy.FITSFigure(filename, dimensions=dimensions,
                         convention='calabretta')
    f.show_grayscale()
    f.close()


@pytest.mark.parametrize(('header', 'dimensions'), invalid_parameters)
def test_file_init_invalid(tmpdir, header, dimensions):
    filename = generate_file(header, str(tmpdir))
    with pytest.raises(Exception):
        aplpy.FITSFigure(filename, dimensions=dimensions,
                         convention='calabretta')


@pytest.mark.parametrize(('header', 'dimensions'), valid_parameters)
def test_hdu_init_valid(header, dimensions):
    hdu = generate_hdu(header)
    f = aplpy.FITSFigure(hdu, dimensions=dimensions, convention='calabretta')
    f.show_grayscale()
    f.close()


@pytest.mark.parametrize(('header', 'dimensions'), invalid_parameters)
def test_hdu_init_invalid(header, dimensions):
    hdu = generate_hdu(header)
    with pytest.raises(Exception):
        aplpy.FITSFigure(hdu, dimensions=dimension, convention='calabretta')


@pytest.mark.parametrize(('header', 'dimensions'), valid_parameters)
def test_wcs_init_valid(header, dimensions):
    wcs = generate_wcs(header)
    f = aplpy.FITSFigure(wcs, dimensions=dimensions, convention='calabretta')
    f.show_grayscale()
    f.close()


@pytest.mark.parametrize(('header', 'dimensions'), invalid_parameters)
def test_wcs_init_invalid(header, dimensions):
    wcs = generate_wcs(header)
    with pytest.raises(Exception):
        aplpy.FITSFigure(wcs, dimensions=dimensions, convention='calabretta')
