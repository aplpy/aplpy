import os

import matplotlib
matplotlib.use('Agg')

import numpy as np

from astropy.table import Table
from astropy.tests.helper import pytest
from .helpers import generate_wcs
from .. import wcs_util


HEADER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/2d_fits', '1904-66_TAN.hdr')

tab = Table({'RA':[347.,349.], 'DEC':[-68.,-68]})

GOOD_INPUT = [ [1.,2.],
               [[1.,2.],[3,4]],
               [np.arange(2), np.arange(2)],
               [tab['RA'], tab['DEC']]
             ]

BAD_INPUT = [ [1,['s','w']],
              [np.arange(2), np.sum],
              [tab['RA'], 'ewr']
            ]

@pytest.mark.parametrize(('inputval'), GOOD_INPUT)
def test_pixworld_input_and_consistency(inputval):
    wcs = generate_wcs(HEADER)
    ra, dec = wcs_util.pix2world(wcs, inputval[0], inputval[1])
    x, y = wcs_util.world2pix(wcs, ra, dec)
    # For some inputs (e.g. list) a-b is not defined
    # so change them all to np.ndarrays here to make sure
    assert np.all(np.abs(np.array(x) - np.array(inputval[0])) < 1e-5)
    assert np.all(np.abs(np.array(y) - np.array(inputval[1])) < 1e-5)

def test_returntypes():
    wcs = generate_wcs(HEADER)
    ra, dec = wcs_util.pix2world(wcs, 1.,2.)
    assert np.isscalar(ra) and np.isscalar(dec)
    ra, dec = wcs_util.pix2world(wcs, [1.],[2.])
    assert (type(ra) == list) and (type(dec) == list)
    # Astropy.table.Column objects get donwconverted np.ndarray
    ra, dec = wcs_util.pix2world(wcs, np.arange(2), tab['DEC'])
    assert isinstance(ra, np.ndarray) and isinstance(dec, np.ndarray)


@pytest.mark.parametrize(('inputval'), BAD_INPUT)
def test_pix2world_fail(inputval):
    wcs = generate_wcs(HEADER)
    with pytest.raises(Exception) as exc:
        wcs_util.pix2world(wcs, inputval[0], inputval[1])
    assert exc.value.args[0] == "pix2world should be provided either with two scalars, two lists, or two numpy arrays"

@pytest.mark.parametrize(('inputval'), BAD_INPUT)
def test_world2pix_fail(inputval):
    wcs = generate_wcs(HEADER)
    with pytest.raises(Exception) as exc:
        wcs_util.world2pix(wcs, inputval[0], inputval[1])
    assert exc.value.args[0] == "world2pix should be provided either with two scalars, two lists, or two numpy arrays"

