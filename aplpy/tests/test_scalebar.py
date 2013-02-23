import matplotlib
matplotlib.use('Agg')

import numpy as np
import pytest

from aplpy import FITSFigure


def test_scalebar_add_invalid():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    with pytest.raises(TypeError):
        f.add_scalebar()


def test_scalebar_addremove():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_scalebar(0.1)
    f.remove_scalebar()
    f.add_scalebar(0.1)
    f.close()


def test_scalebar_showhide():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_scalebar(0.1)
    f.scalebar.hide()
    f.scalebar.show(0.1)
    f.close()


def test_scalebar_length():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_scalebar(0.1)
    f.scalebar.set_length(0.01)
    f.scalebar.set_length(0.1)
    f.close()


def test_scalebar_label():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_scalebar(0.1)
    f.scalebar.set_label('1 pc')
    f.scalebar.set_label('5 AU')
    f.scalebar.set_label('2"')
    f.close()


def test_scalebar_corner():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_scalebar(0.1)
    for corner in ['top', 'bottom', 'left', 'right', 'top left', 'top right',
                   'bottom left', 'bottom right']:
        f.scalebar.set_corner(corner)
    f.close()


def test_scalebar_frame():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_scalebar(0.1)
    f.scalebar.set_frame(True)
    f.scalebar.set_frame(False)
    f.close()


def test_scalebar_color():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_scalebar(0.1)
    f.scalebar.set_color('black')
    f.scalebar.set_color('#003344')
    f.scalebar.set_color((1.0, 0.4, 0.3))
    f.close()


def test_scalebar_alpha():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_scalebar(0.1)
    f.scalebar.set_alpha(0.1)
    f.scalebar.set_alpha(0.2)
    f.scalebar.set_alpha(0.5)
    f.close()


def test_scalebar_font():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_scalebar(0.1)
    f.scalebar.set_font(size='small', weight='bold', stretch='normal',
                        family='serif', style='normal', variant='normal')
    f.close()
