import matplotlib
matplotlib.use('Agg')

import numpy as np
from astropy.tests.helper import pytest

from .. import FITSFigure


def test_axis_labels_show_hide():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.axis_labels.hide()
    f.axis_labels.show()
    f.axis_labels.hide_x()
    f.axis_labels.show_x()
    f.axis_labels.hide_y()
    f.axis_labels.show_y()
    f.close()


def test_axis_labels_text():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.axis_labels.set_xtext('x')
    f.axis_labels.set_ytext('y')
    f.close()


def test_axis_labels_pad():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.axis_labels.set_xpad(-1.)
    f.axis_labels.set_ypad(0.5)
    f.close()


def test_axis_labels_position():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.axis_labels.set_xposition('top')
    f.axis_labels.set_xposition('bottom')
    f.axis_labels.set_yposition('right')
    f.axis_labels.set_yposition('left')
    f.close()


def test_axis_labels_position_invalid():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    with pytest.raises(ValueError):
        f.axis_labels.set_xposition('right')
    with pytest.raises(ValueError):
        f.axis_labels.set_xposition('left')
    with pytest.raises(ValueError):
        f.axis_labels.set_yposition('top')
    with pytest.raises(ValueError):
        f.axis_labels.set_yposition('bottom')
    f.close()


def test_axis_labels_font():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.axis_labels.set_font(size='small', weight='bold', stretch='normal',
                           family='serif', style='normal', variant='normal')
    f.close()
