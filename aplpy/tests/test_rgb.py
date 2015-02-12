import os
import warnings

import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.io import fits

from .. import FITSFigure
from ..rgb import make_rgb_image

from .test_images import BaseImageTests

HEADER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/2d_fits', '1904-66_TAN.hdr')


class TestRGB(BaseImageTests):

    def test_rgb(self, generate, tmpdir):

        # Regression test to check that RGB recenter works properly

        r_file = tmpdir.join('r.fits').strpath
        g_file = tmpdir.join('g.fits').strpath
        b_file = tmpdir.join('b.fits').strpath
        rgb_file = tmpdir.join('rgb.png').strpath

        np.random.seed(12345)

        header = fits.Header.fromtextfile(HEADER)

        r = fits.PrimaryHDU(np.random.random((12,12)), header)
        r.writeto(r_file)

        g = fits.PrimaryHDU(np.random.random((12,12)), header)
        g.writeto(g_file)

        b = fits.PrimaryHDU(np.random.random((12,12)), header)
        b.writeto(b_file)

        make_rgb_image([r_file, g_file, b_file], rgb_file, embed_avm_tags=False)

        f = FITSFigure(r_file, figsize=(3,3))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f.show_rgb(rgb_file)

        f.tick_labels.set_xformat('dd.d')
        f.tick_labels.set_yformat('dd.d')

        f.recenter(359.3, -72.1, radius=0.05)

        self.generate_or_test(generate, f, 'test_rgb.png', tolerance=2)
        f.close()
