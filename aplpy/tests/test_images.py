import os
import shutil
import tempfile
from distutils.version import LooseVersion

import numpy as np

import matplotlib
from matplotlib.testing.compare import compare_images
from astropy.tests.helper import pytest

from .. import FITSFigure
from .helpers import generate_file

MATPLOTLIB_GE_12 = LooseVersion(matplotlib.__version__) >= LooseVersion("1.2")


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

    # method to create baseline or test images
    def generate_or_test(self, generate, figure, image, adjust_bbox=True, tolerance=1):
        if generate is None:
            result_dir = tempfile.mkdtemp()
            test_image = os.path.abspath(os.path.join(result_dir, image))

            # distutils will put the baseline images in non-accessible places,
            # copy to our tmpdir to be sure to keep them in case of failure
            orig_baseline_image = os.path.abspath(os.path.join(self._baseline_images_dir, image))
            baseline_image = os.path.abspath(os.path.join(result_dir, 'baseline-'+image))
            shutil.copyfile(orig_baseline_image, baseline_image)

            figure.save(test_image)

            if not os.path.exists(baseline_image):
                raise Exception("""Image file not found for comparision test
                                Generated Image:
                                \t{test}
                                This is expected for new tests.""".format(
                                    test=test_image))

            msg = compare_images(baseline_image, test_image, tol=tolerance)

            if msg is None:
                shutil.rmtree(result_dir)
            else:
                raise Exception(msg)
        else:
            figure.save(os.path.abspath(os.path.join(generate, image)), adjust_bbox=adjust_bbox)
            pytest.skip("Skipping test, since generating data")


class TestBasic(BaseImageTests):

    # Test for showing grayscale
    def test_basic_image(self, generate):
        f = FITSFigure(self.filename_2)
        f.show_grayscale()
        self.generate_or_test(generate, f, 'basic_image.png')
        f.close()

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
        self.generate_or_test(generate, f, 'tick_labels_options.png')
        f.close()

    # Test for showing colorscale
    @pytest.mark.skipif("not MATPLOTLIB_GE_12")
    def test_show_colorbar_scalebar_beam(self, generate):
        f = FITSFigure(self.filename_1)
        f.ticks.set_color('black')
        f.show_colorscale(vmin=-0.1, vmax=0.1)
        f.add_colorbar()
        f.add_scalebar(7.5)
        f.add_beam(major=0.5, minor=0.2, angle=10.)
        f.tick_labels.hide()
        self.generate_or_test(generate, f, 'colorbar_scalebar_beam.png')
        f.close()

    # Test for overlaying shapes
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
        self.generate_or_test(generate, f, 'overlay_shapes.png')
        f.close()

    # Test for grid
    def test_grid(self, generate):
        f = FITSFigure(self.filename_1)
        f.ticks.set_color('black')
        f.add_grid()
        f.grid.set_color('red')
        f.grid.set_alpha(0.8)
        f.grid.set_linestyle('solid')
        f.grid.set_xspacing('tick')
        f.grid.set_yspacing(3)
        self.generate_or_test(generate, f, 'grid.png')
        f.close()

    # Test recenter
    def test_recenter(self, generate):
        f = FITSFigure(self.filename_2)
        f.ticks.set_color('black')
        f.recenter(266.5, -29.0, width=0.1, height=0.1)
        f.axis_labels.set_xpad(20)
        f.axis_labels.set_ypad(20)
        self.generate_or_test(generate, f, 'recenter.png')
        f.close()

    # Test overlaying contours
    def test_contours(self, generate):
        data = np.arange(256).reshape((16, 16))
        f = FITSFigure(data)
        f.ticks.set_color('black')
        f.show_contour(data, levels=np.linspace(1., 254., 10), filled=False)
        self.generate_or_test(generate, f, 'contours.png')
        f.close()

    # Test cube slice
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
        self.generate_or_test(generate, f, 'cube_slice.png')
        f.close()
