import os
import tempfile

import numpy as np

from astropy.tests.helper import pytest, remote_data

from .. import FITSFigure
from .helpers import generate_file
from . import baseline_dir


class BaseImageTests(object):

    @classmethod
    def setup_class(cls):

        cls._moduledir = os.path.dirname(__file__)
        cls._data_dir = os.path.abspath(os.path.join(cls._moduledir, 'data'))
        cls._baseline_images_dir = os.path.abspath(os.path.join(cls._moduledir, 'baseline_images'))

        header_1 = os.path.join(cls._data_dir, '2d_fits/1904-66_AIR.hdr')
        cls.filename_1 = generate_file(header_1, str(tempfile.mkdtemp()))

        header_2 = os.path.join(cls._data_dir, '2d_fits/2MASS_k.hdr')
        cls.filename_2 = generate_file(header_2, str(tempfile.mkdtemp()))

        header_3 = os.path.join(cls._data_dir, '3d_fits/cube.hdr')
        cls.filename_3 = generate_file(header_3, str(tempfile.mkdtemp()))


class TestBasic(BaseImageTests):

    # Test for showing grayscale
    @remote_data
    @pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=1.5)
    def test_basic_image(self, generate):
        f = FITSFigure(self.filename_2)
        f.show_grayscale()
        return f

    @remote_data
    @pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=1.5)
    def test_ticks_labels_options(self, generate):
        f = FITSFigure(self.filename_2)
        f.ticks.set_color('black')
        f.axis_labels.set_xposition('top')
        f.axis_labels.set_yposition('right')
        f.axis_labels.set_font(size='medium', weight='medium',
                               stretch='normal', style='normal')
        f.tick_labels.set_xformat('dd:mm:ss.ss')
        f.tick_labels.set_yformat('hh:mm:ss.ss')
        f.tick_labels.set_style('colons')
        f.ticks.set_xspacing(0.2)
        f.ticks.set_yspacing(0.2)
        f.ticks.set_minor_frequency(10)
        return f

    # Test for showing colorscale
    @remote_data
    @pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=1.5)
    def test_show_colorbar_scalebar_beam(self, generate):
        f = FITSFigure(self.filename_1)
        f.ticks.set_color('black')
        f.show_colorscale(vmin=-0.1, vmax=0.1)
        f.add_colorbar()
        f.add_scalebar(7.5)
        f.add_beam(major=0.5, minor=0.2, angle=10.)
        f.tick_labels.hide()
        return f

    # Test for overlaying shapes
    @remote_data
    @pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=1.5)
    def test_overlay_shapes(self, generate):
        f = FITSFigure(self.filename_1)
        f.ticks.set_color('black')
        f.show_markers([360., 350., 340.], [-61., -62., -63])
        f.show_ellipses(330., -66., 0.15, 2., 10.)
        f.show_rectangles([355., 350.], [-71, -72], [0.5, 1], [2, 1])
        f.show_arrows([340., 360], [-72, -68], [2, -2], [2, 2])
        f.add_label(350., -66., 'text')
        f.add_label(0.4, 0.25, 'text', relative=True)
        f.frame.set_linewidth(1)  # points
        f.frame.set_color('black')
        f.axis_labels.hide()
        return f

    # Test for grid
    @remote_data
    @pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=1.5)
    def test_grid(self, generate):
        f = FITSFigure(self.filename_1)
        f.ticks.set_color('black')
        f.add_grid()
        f.grid.set_color('red')
        f.grid.set_alpha(0.8)
        f.grid.set_linestyle('solid')
        f.grid.set_xspacing('tick')
        f.grid.set_yspacing(3)
        return f

    # Test recenter
    @remote_data
    @pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=1.5)
    def test_recenter(self, generate):
        f = FITSFigure(self.filename_2)
        f.ticks.set_color('black')
        f.recenter(266.5, -29.0, width=0.1, height=0.1)
        f.axis_labels.set_xpad(20)
        f.axis_labels.set_ypad(20)
        return f

    # Test overlaying contours
    @remote_data
    @pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=1.5)
    def test_contours(self, generate):
        data = np.arange(256).reshape((16, 16))
        f = FITSFigure(data)
        f.ticks.set_color('black')
        f.show_contour(data, levels=np.linspace(1., 254., 10), filled=False)
        return f

    # Test cube slice
    @remote_data
    @pytest.mark.mpl_image_compare(baseline_dir=baseline_dir, tolerance=1.5)
    def test_cube_slice(self, generate):
        f = FITSFigure(self.filename_3, dimensions=[2, 0], slices=[10])
        f.ticks.set_color('black')
        f.add_grid()
        f.grid.set_color('black')
        f.grid.set_linestyle('solid')
        f.grid.set_xspacing(250)
        f.grid.set_yspacing(0.01)
        f.tick_labels.set_xformat('%g')
        f.tick_labels.set_yformat('dd:mm:ss.ss')
        return f
