import pytest
import numpy as np

from ..core import FITSFigure

from .test_images import BaseImageTests
from . import baseline_dir
from .figures import figure_test

x = np.linspace(-1., 1., 10)
y = np.linspace(-1., 1., 10)
X, Y = np.meshgrid(x, y)

np.random.seed(12345)
IMAGE = np.random.random((10, 10))
PDATA = np.arange(100).reshape((10, 10)) / 50. + 0.5
ADATA = np.degrees(np.arctan2(Y, X))


class TestVectors(BaseImageTests):

    @figure_test
    def test_default(self):
        f = FITSFigure(IMAGE, figsize=(4, 4))
        f.show_grayscale()
        f.show_vectors(PDATA, ADATA, color='orange')
        return f

    @figure_test
    def test_step_scale(self):
        f = FITSFigure(IMAGE, figsize=(4, 4))
        f.show_grayscale()
        f.show_vectors(PDATA, ADATA, step=2, scale=0.8, color='orange')
        return f
