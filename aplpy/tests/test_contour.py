import os
import pytest
import numpy as np
from astropy.wcs import WCS
from astropy.io import fits

from .. import FITSFigure

ROOT = os.path.dirname(os.path.abspath(__file__))
HEADER_3D = os.path.join(ROOT, 'data', '3d_fits', 'cube.hdr')


# Test simple contour generation with Numpy example


@pytest.mark.parametrize(('filled'), [True, False])
def test_numpy_contour(filled):
    data = np.arange(256).reshape((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.show_contour(data, levels=np.linspace(1., 254., 10), filled=filled)
    f.close()


def test_contour_slices_with_wcs():
    data = np.arange(16**3).reshape((16, 16, 16))
    hdu = fits.PrimaryHDU(data, fits.Header.fromtextfile(HEADER_3D))
    f = FITSFigure(hdu, slices=[0])
    f.show_grayscale()
    f.show_contour(hdu, levels=np.linspace(1., 254., 10),
                   slices=[0], dimensions=[1, 0])
    f.close()
