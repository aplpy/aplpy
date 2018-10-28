from __future__ import absolute_import, print_function, division

import os

import pytest
import numpy as np

from astropy.table import Table
from astropy.io import fits
from .helpers import generate_wcs
from .. import FITSFigure

HEADER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/2d_fits', '1904-66_TAN.hdr')

tab = Table({'RA': [347., 349.], 'DEC': [-68., -68]})

GOOD_INPUT = [[1, 2],
              [[1, 2], [3, 4]],
              [np.arange(2), np.arange(2)],
              [tab['RA'], tab['DEC']]
              ]

BAD_INPUT = [[1, ['s', 'e']],
             [np.arange(2), np.sum],
             [tab['RA'], 'ewr']
             ]


@pytest.mark.parametrize(('inputval'), GOOD_INPUT)
def test_pixel_coords(inputval):
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_markers(inputval[0], inputval[1])
    f.close()


@pytest.mark.parametrize(('inputval'), GOOD_INPUT)
def test_wcs_coords(inputval):
    wcs = generate_wcs(HEADER)
    header = fits.Header.fromtextfile(HEADER)
    wcs.naxis1 = header['NAXIS1']
    wcs.naxis2 = header['NAXIS2']
    f = FITSFigure(wcs)
    f.show_markers(inputval[0], inputval[1])
    f.close()


@pytest.mark.parametrize(('inputval'), BAD_INPUT)
def test_pixel_coords_bad(inputval):
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    with pytest.raises(Exception) as exc:
        f.show_markers(inputval[0], inputval[1])
    assert exc.value.args[0] == "x and y must be the same size"
    f.close()


@pytest.mark.parametrize(('inputval'), BAD_INPUT)
def test_wcs_coords_bad(inputval):
    wcs = generate_wcs(HEADER)
    header = fits.Header.fromtextfile(HEADER)
    wcs.naxis1 = header['NAXIS1']
    wcs.naxis2 = header['NAXIS2']
    f = FITSFigure(wcs)
    with pytest.raises(Exception) as exc:
        f.show_markers(inputval[0], inputval[1])
    f.close()
    assert exc.value.args[0] == "x and y must be the same size"
