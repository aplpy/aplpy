import matplotlib
matplotlib.use('Agg')

import numpy as np
import pyfits
import aplpy
import pytest
import pywcs

# The tests in this file check that the initialization and basic plotting do
# not crash for FITS files with 3+ dimensions. No reference images are
# required here.


def setup_module(module):

    # Read in header
    header = pyfits.Header()
    header.fromTxtFile('data/cube.hdr')

    # Find shape of array
    shape = []
    for i in range(header['NAXIS']):
        shape.append(header['NAXIS%i' % (i + 1)])

    # Generate data array
    data = np.zeros(shape[::-1])

    # Generate primary HDU
    hdu = pyfits.PrimaryHDU(data=data, header=header)

    # Make available to all tests
    module.hdu = hdu
    module.data = data
    module.header = header
    module.wcs = pywcs.WCS(header)

VALID_DIMENSIONS = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
INVALID_DIMENSIONS = [None, (1,), (0, 3), (-4, 2), (1, 1), (2, 2), (3, 3),
                      (1, 2, 3), (3, 5, 3, 2)]


@pytest.mark.parametrize(('dimensions'), VALID_DIMENSIONS)
def test_file_init_valid(tmpdir, dimensions):
    filename = str(tmpdir) + '/' + 'valid.fits'
    hdu.writeto(filename)
    f = aplpy.FITSFigure(filename, dimensions=dimensions, slices=[100])
    f.show_grayscale()
    f.add_grid()
    f.close()


@pytest.mark.parametrize(('dimensions'), INVALID_DIMENSIONS)
def test_file_init_invalid(tmpdir, dimensions):
    filename = str(tmpdir) + '/' + 'invalid.fits'
    hdu.writeto(filename)
    with pytest.raises(Exception):
        f = aplpy.FITSFigure(filename, dimensions=dimensions, slices=[100])


@pytest.mark.parametrize(('dimensions'), VALID_DIMENSIONS)
def test_hdu_init_valid(dimensions):
    f = aplpy.FITSFigure(hdu, dimensions=dimensions, slices=[100])
    f.show_grayscale()
    f.add_grid()
    f.close()


@pytest.mark.parametrize(('dimensions'), INVALID_DIMENSIONS)
def test_hdu_init_invalid(dimensions):
    with pytest.raises(Exception):
        f = aplpy.FITSFigure(hdu, dimensions=dimensions, slices=[100])


@pytest.mark.parametrize(('dimensions'), VALID_DIMENSIONS)
def test_wcs_init_valid(dimensions):
    f = aplpy.FITSFigure(wcs, dimensions=dimensions, slices=[100])
    f.show_grayscale()
    f.add_grid()
    f.close()


@pytest.mark.parametrize(('dimensions'), INVALID_DIMENSIONS)
def test_wcs_init_invalid(dimensions):
    with pytest.raises(Exception):
        f = aplpy.FITSFigure(wcs, dimensions=dimensions, slices=[100])
