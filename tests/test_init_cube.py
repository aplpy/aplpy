import matplotlib
matplotlib.use('Agg')

import pyfits
import aplpy
import pytest

from helpers import generate_file, generate_hdu, generate_wcs

# The tests in this file check that the initialization and basic plotting do
# not crash for FITS files with 3+ dimensions. No reference images are
# required here.

HEADERS = ['data/3d_fits/cube.hdr']


VALID_DIMENSIONS = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
INVALID_DIMENSIONS = [None, (1,), (0, 3), (-4, 2), (1, 1), (2, 2), (3, 3),
                      (1, 2, 3), (3, 5, 3, 2)]

# For valid dimensions, test the plotting of all files
valid_parameters = []
for h in HEADERS:
    for d in VALID_DIMENSIONS:
        valid_parameters.append((h, d))

# For invalid dimensions, no need to test for all headers, only do the first
invalid_parameters = []
for d in INVALID_DIMENSIONS:
    invalid_parameters.append((HEADERS[0], d))


@pytest.mark.parametrize(('header', 'dimensions'), valid_parameters)
def test_file_init_valid(tmpdir, header, dimensions):
    filename = generate_file(header, str(tmpdir))
    f = aplpy.FITSFigure(filename, dimensions=dimensions, slices=[5])
    f.show_grayscale()
    f.close()


@pytest.mark.parametrize(('header', 'dimensions'), invalid_parameters)
def test_file_init_invalid(tmpdir, header, dimensions):
    filename = generate_file(header, str(tmpdir))
    with pytest.raises(Exception):
        aplpy.FITSFigure(filename, dimensions=dimensions, slices=[5])


@pytest.mark.parametrize(('header', 'dimensions'), valid_parameters)
def test_hdu_init_valid(header, dimensions):
    hdu = generate_hdu(header)
    f = aplpy.FITSFigure(hdu, dimensions=dimensions, slices=[5])
    f.show_grayscale()
    f.close()


@pytest.mark.parametrize(('header', 'dimensions'), invalid_parameters)
def test_hdu_init_invalid(header, dimensions):
    hdu = generate_hdu(header)
    with pytest.raises(Exception):
        aplpy.FITSFigure(hdu, dimensions=dimensions, slices=[5])


@pytest.mark.parametrize(('header', 'dimensions'), valid_parameters)
def test_wcs_init_valid(header, dimensions):
    wcs = generate_wcs(header)
    f = aplpy.FITSFigure(wcs, dimensions=dimensions, slices=[5])
    f.show_grayscale()
    f.close()


@pytest.mark.parametrize(('header', 'dimensions'), invalid_parameters)
def test_wcs_init_invalid(header, dimensions):
    wcs = generate_wcs(header)
    with pytest.raises(Exception):
        aplpy.FITSFigure(wcs, dimensions=dimensions, slices=[5])
