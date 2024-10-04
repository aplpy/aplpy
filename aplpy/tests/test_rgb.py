import os
import warnings

import pytest
import numpy as np
from astropy.io import fits
from astropy.coordinates import Galactic

from .. import FITSFigure
from ..rgb import make_rgb_image, make_rgb_cube

from .test_images import BaseImageTests
from . import baseline_dir
from .helpers import generate_header
from .figures import figure_test

ROOT = os.path.dirname(os.path.abspath(__file__))
HEADER = os.path.join(ROOT, 'data/2d_fits', '1904-66_TAN.hdr')


class TestRGB(BaseImageTests):

    @pytest.mark.parametrize('embed_avm_tags', (False, True))
    @figure_test
    def test_rgb(self, tmpdir, embed_avm_tags):

        # Regression test to check that RGB recenter works properly

        r_file = tmpdir.join('r.fits').strpath
        g_file = tmpdir.join('g.fits').strpath
        b_file = tmpdir.join('b.fits').strpath
        rgb_file = tmpdir.join('rgb.png').strpath

        np.random.seed(12345)

        header = fits.Header.fromtextfile(HEADER)

        r = fits.PrimaryHDU(np.random.random((12, 12)), header)
        r.writeto(r_file)

        g = fits.PrimaryHDU(np.random.random((12, 12)), header)
        g.writeto(g_file)

        b = fits.PrimaryHDU(np.random.random((12, 12)), header)
        b.writeto(b_file)

        make_rgb_image([r_file, g_file, b_file], rgb_file, embed_avm_tags=embed_avm_tags)

        if embed_avm_tags:
            f = FITSFigure(rgb_file, figsize=(7, 5))
        else:
            f = FITSFigure(r_file, figsize=(7, 5))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f.show_rgb(rgb_file)

        f.tick_labels.set_xformat('dd.d')
        f.tick_labels.set_yformat('dd.d')

        f.recenter(359.3, -72.1, radius=0.05)

        return f

    @pytest.mark.parametrize('north', ['default', 'galactic', 'false'])
    @figure_test
    def test_make_rgb_cube(self, tmpdir, north):

        # Regression test to check that RGB recenter works properly

        header = generate_header(os.path.join(ROOT, 'data', '2d_fits', '2MASS_k_rot.hdr'))

        header['CRPIX1'] = 6.5
        header['CRPIX2'] = 6.5

        header_r = header.copy()
        header_r['CROTA2'] = 5
        header_g = header.copy()
        header_g['CROTA2'] = 35
        header_b = header.copy()
        header_b['CROTA2'] = 70

        r_file = tmpdir.join('r.fits').strpath
        g_file = tmpdir.join('g.fits').strpath
        b_file = tmpdir.join('b.fits').strpath
        rgb_cube = tmpdir.join('rgb.fits').strpath
        rgb_file = tmpdir.join('rgb.png').strpath

        header = fits.Header.fromtextfile(HEADER)

        r = fits.PrimaryHDU(np.ones((128, 128)), header_r)
        r.writeto(r_file)

        g = fits.PrimaryHDU(np.ones((128, 128)), header_g)
        g.writeto(g_file)

        b = fits.PrimaryHDU(np.ones((128, 128)), header_b)
        b.writeto(b_file)

        if north == 'default':
            kwargs = {}
        elif north == 'galactic':
            kwargs = {'north': Galactic()}
        elif north == 'false':
            kwargs = {'north': False}

        make_rgb_cube([r_file, g_file, b_file], rgb_cube, **kwargs)

        make_rgb_image(rgb_cube, rgb_file, embed_avm_tags=True,
                       vmin_r=0, vmax_r=1, vmin_g=0, vmax_g=1, vmin_b=0, vmax_b=1)

        f = FITSFigure(rgb_file, figsize=(3, 3))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f.show_rgb(rgb_file)

        f.tick_labels.hide()
        f.axis_labels.hide()
        f.add_grid()

        return f
