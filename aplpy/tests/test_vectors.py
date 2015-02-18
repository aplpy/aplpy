import numpy as np

from ..core import FITSFigure

from .test_images import BaseImageTests

x = np.linspace(-1., 1., 10)
y = np.linspace(-1., 1., 10)
X, Y = np.meshgrid(x, y)

np.random.seed(12345)
IMAGE = np.random.random((10,10))
PDATA = np.arange(100).reshape((10,10)) / 50. + 0.5
ADATA = np.degrees(np.arctan2(Y, X))

class TestVectors(BaseImageTests):

    def test_default(self, generate):
        f = FITSFigure(IMAGE, figsize=(4,4))
        f.show_grayscale()
        f.show_vectors(PDATA, ADATA, color='orange')
        self.generate_or_test(generate, f, 'vectors_default.png', tolerance=2.5)
        f.close()

    def test_step_scale(self, generate):
        f = FITSFigure(IMAGE, figsize=(4,4))
        f.show_grayscale()
        f.show_vectors(PDATA, ADATA, step=2, scale=0.8, color='orange')
        self.generate_or_test(generate, f, 'vectors_step_scale.png', tolerance=2.5)
        f.close()

