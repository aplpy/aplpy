import pytest
import numpy as np

from .. import FITSFigure


def test_subplot_grid():
    f = FITSFigure(np.zeros((10, 10)), subplot=(2, 2, 1))
    f.show_grayscale()
    f.close()


def test_subplot_box():
    f = FITSFigure(np.zeros((10, 10)), subplot=[0.1, 0.1, 0.8, 0.8])
    f.show_grayscale()
    f.close()


@pytest.mark.parametrize('subplot', [(1, 2, 3, 4), [1, 2, 3], '111', 1.2])
def test_subplot_invalid(subplot):
    with pytest.raises(ValueError) as exc:
        FITSFigure(np.zeros((10, 10)), subplot=subplot)
    assert exc.value.args[0] == "subplot= should be either a tuple of three values, or a list of four values"
