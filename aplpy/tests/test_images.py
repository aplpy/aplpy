from __future__ import absolute_import, print_function, division

import os
import tempfile

import pytest
import numpy as np

try:
    import pyregion  # noqa
except ImportError:
    PYREGION_INSTALLED = False
else:
    PYREGION_INSTALLED = True

try:
    import reproject  # noqa
except ImportError:
    REPROJECT_INSTALLED = False
else:
    REPROJECT_INSTALLED = True

from .. import FITSFigure
from .helpers import generate_file
from . import baseline_dir

MODULEDIR = os.path.dirname(__file__)
DATADIR = os.path.abspath(os.path.join(MODULEDIR, 'data'))


class BaseImageTests(object):

    @classmethod
    def setup_class(cls):

        cls._baseline_images_dir = os.path.abspath(os.path.join(MODULEDIR, 'baseline_images'))

        header_1 = os.path.join(DATADIR, '2d_fits/1904-66_AIR.hdr')
        cls.filename_1 = generate_file(header_1, str(tempfile.mkdtemp()))

        header_2 = os.path.join(DATADIR, '2d_fits/2MASS_k.hdr')
        cls.filename_2 = generate_file(header_2, str(tempfile.mkdtemp()))

        header_3 = os.path.join(DATADIR, '3d_fits/cube.hdr')
        cls.filename_3 = generate_file(header_3, str(tempfile.mkdtemp()))

        header_4 = os.path.join(DATADIR, '2d_fits/2MASS_k_rot.hdr')
        cls.filename_4 = generate_file(header_4, str(tempfile.mkdtemp()))


class TestBasic(BaseImageTests):

    # Test for showing grayscale
    @pytest.mark.remote_data
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=7.5)
    def test_basic_image(self):
        f = FITSFigure(self.filename_2, figsize=(7, 5))
        f.show_grayscale(vmin=0, vmax=1)
        return f._figure

    @pytest.mark.remote_data
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=7.5)
    def test_ticks_labels_options(self):
        f = FITSFigure(self.filename_2, figsize=(7, 5))

        # Force aspect ratio
        f.show_grayscale()
        f.hide_grayscale()

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
        return f._figure

    # Test for showing colorscale
    @pytest.mark.remote_data
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=5)
    def test_show_colorbar_scalebar_beam(self):
        f = FITSFigure(self.filename_1, figsize=(7, 5))
        f.ticks.set_color('black')
        f.show_colorscale(vmin=-0.1, vmax=0.1)
        f.add_colorbar()
        f.add_scalebar(7.5)
        f.add_beam(major=0.5, minor=0.2, angle=10.)
        f.tick_labels.hide()
        return f._figure

    # Test for overlaying shapes
    @pytest.mark.remote_data
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=1.5)
    def test_overlay_shapes(self):
        f = FITSFigure(self.filename_1, figsize=(7, 5))

        # Force aspect ratio
        f.show_grayscale()
        f.hide_grayscale()

        f.ticks.set_color('black')

        # Markers
        f.show_markers([360., 350., 340.], [-61., -62., -63], color='cyan')
        f.show_markers([30, 40], [50, 70], coords_frame='pixel', edgecolor='blue')

        # Circles
        f.show_circles([360., 350., 340.], [-61., -62., -63], [0.5, 0.4, 0.3], edgecolor='purple')
        f.show_circles([30, 40], [50, 70], [10, 20], coords_frame='pixel', edgecolor='orange')

        # Ellipses
        f.show_ellipses(340., -66., 1.5, 2., 10., edgecolor='red')
        f.show_ellipses(120, 60, 20, 40, 20., coords_frame='pixel', edgecolor='green')

        # Rectangles
        f.show_rectangles([355., 350.], [-71, -72], [0.5, 1], [2, 1], angle=[20, 30], edgecolor='magenta')
        f.show_rectangles([66, 80], [20, 30], [10, 14], [20, 22], angle=[20, 30], coords_frame='pixel', edgecolor='yellow')

        # Arrows
        f.show_arrows([340., 360], [-72, -68], [2, -2], [2, 2])

        # Polygons
        poly = np.array([[330, 340, 360], [-65, -61, -63]])
        f.show_polygons([poly], edgecolor='0.3', zorder=10)

        # Lines
        f.show_lines([poly], zorder=9, lw=5, color='red', alpha=0.5)

        # Labels
        f.add_label(350., -66., 'text')
        f.add_label(0.4, 0.25, 'text', relative=True)

        f.frame.set_linewidth(1)  # points
        f.frame.set_color('black')
        f.axis_labels.hide()

        return f._figure

    # Test for grid
    @pytest.mark.remote_data
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=7.5)
    def test_grid(self):
        f = FITSFigure(self.filename_1, figsize=(7, 5))

        # Force aspect ratio
        f.show_grayscale()
        f.hide_grayscale()

        f.ticks.set_color('black')
        f.add_grid()
        f.grid.set_color('red')
        f.grid.set_alpha(0.8)
        f.grid.set_linestyle('solid')
        f.grid.set_xspacing('tick')
        f.grid.set_yspacing(3)
        return f._figure

    # Test recenter
    @pytest.mark.remote_data
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=1.5)
    def test_recenter(self):
        f = FITSFigure(self.filename_2, figsize=(7, 5))

        # Force aspect ratio
        f.show_grayscale()
        f.hide_grayscale()

        f.ticks.set_color('black')
        f.recenter(266.5, -29.0, width=0.1, height=0.1)
        f.axis_labels.set_xpad(20)
        f.axis_labels.set_ypad(20)
        return f._figure

    # Test overlaying contours
    @pytest.mark.remote_data
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=5)
    def test_contours(self):
        data = np.arange(256).reshape((16, 16))
        f = FITSFigure(data, figsize=(7, 5))

        # Force aspect ratio
        f.show_grayscale()
        f.hide_grayscale()

        f.ticks.set_color('black')
        f.show_contour(data, levels=np.linspace(1., 254., 10), filled=False)
        return f._figure

    # Test cube slice
    @pytest.mark.remote_data
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=5)
    def test_cube_slice(self):
        f = FITSFigure(self.filename_3, dimensions=[2, 0], slices=[10], figsize=(7, 5), subplot=[0.25, 0.1, 0.7, 0.8])
        f.ticks.set_color('black')
        f.add_grid()
        f.grid.set_color('black')
        f.grid.set_linestyle('solid')
        f.grid.set_xspacing(250)
        f.grid.set_yspacing(0.01)
        f.tick_labels.set_xformat('%g')
        f.tick_labels.set_yformat('dd:mm:ss.ss')
        return f._figure

    # Test for ds9 regions
    @pytest.mark.remote_data
    @pytest.mark.skipif("not PYREGION_INSTALLED")
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=5)
    def test_regions(self):
        f = FITSFigure(self.filename_2, figsize=(7, 5))

        # Force aspect ratio
        f.show_grayscale()
        f.hide_grayscale()

        f.show_regions(os.path.join(DATADIR, 'shapes.reg'))
        f.axis_labels.hide()
        f.tick_labels.hide()
        f.ticks.hide()
        return f._figure

    @pytest.mark.remote_data
    @pytest.mark.skipif("not REPROJECT_INSTALLED")
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=5)
    def test_north(self):
        f = FITSFigure(self.filename_4, figsize=(3, 3), north=True)
        f.show_grayscale(vmin=-1, vmax=1)
        f.axis_labels.hide()
        f.tick_labels.hide()
        f.ticks.hide()
        return f._figure

    @pytest.mark.remote_data
    @pytest.mark.mpl_image_compare(style={}, savefig_kwargs={'adjust_bbox': False}, baseline_dir=baseline_dir, tolerance=5)
    def test_downsample(self):
        data = np.arange(256).reshape((16, 16))
        f = FITSFigure(data, downsample=2)
        f.show_grayscale()
        return f._figure
