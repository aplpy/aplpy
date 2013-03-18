import matplotlib
matplotlib.use('Agg')

import numpy as np

from .. import FITSFigure


def test_beam_addremove():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.remove_beam()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.remove_beam()
    f.close()


def test_beam_showhide():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.hide()
    f.beam.show(major=0.1, minor=0.04, angle=10.)
    f.close()


def test_beam_major():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_major(0.5)
    f.beam.set_major(1.0)
    f.close()


def test_beam_minor():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_minor(0.05)
    f.beam.set_minor(0.08)
    f.close()


def test_beam_angle():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_angle(0.)
    f.beam.set_angle(55.)
    f.close()


def test_beam_corner():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    for corner in ['top', 'bottom', 'left', 'right', 'top left', 'top right',
                   'bottom left', 'bottom right']:
        f.beam.set_corner(corner)
    f.close()


def test_beam_frame():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_frame(True)
    f.beam.set_frame(False)
    f.close()


def test_beam_borderpad():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_borderpad(0.1)
    f.beam.set_borderpad(0.3)
    f.close()


def test_beam_pad():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_pad(0.1)
    f.beam.set_pad(0.3)
    f.close()


def test_beam_alpha():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_alpha(0.1)
    f.beam.set_alpha(0.2)
    f.beam.set_alpha(0.5)
    f.close()


def test_beam_color():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_color('black')
    f.beam.set_color('#003344')
    f.beam.set_color((1.0, 0.4, 0.3))
    f.close()


def test_beam_facecolor():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_facecolor('black')
    f.beam.set_facecolor('#003344')
    f.beam.set_facecolor((1.0, 0.4, 0.3))
    f.close()


def test_beam_edgecolor():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_edgecolor('black')
    f.beam.set_edgecolor('#003344')
    f.beam.set_edgecolor((1.0, 0.4, 0.3))
    f.close()


def test_beam_linestyle():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_linestyle('solid')
    f.beam.set_linestyle('dotted')
    f.beam.set_linestyle('dashed')
    f.close()


def test_beam_linewidth():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_linewidth(0)
    f.beam.set_linewidth(1)
    f.beam.set_linewidth(5)
    f.close()


def test_beam_hatch():
    data = np.zeros((16, 16))
    f = FITSFigure(data)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    for hatch in ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']:
        f.beam.set_hatch(hatch)
    f.close()
