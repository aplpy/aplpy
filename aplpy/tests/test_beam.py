import os

import pytest
import numpy as np
from astropy import units as u
from astropy.io import fits

from .. import FITSFigure
from ..overlays import Beam


header_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/2d_fits')

HEADER = fits.Header.fromtextfile(os.path.join(header_dir, '1904-66_TAN.hdr'))
HDU = fits.PrimaryHDU(np.zeros((16, 16)), HEADER)


def test_beam_add_remove():
    f = FITSFigure(HDU)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.remove_beam()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.remove_beam()
    f.close()


def test_beam_show_hide():
    f = FITSFigure(HDU)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.hide()
    f.beam.show(major=0.1, minor=0.04, angle=10.)
    f.close()


def test_beam_major():
    f = FITSFigure(HDU)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_major(0.5)
    f.beam.set_major(1.0)
    f.close()


@pytest.mark.parametrize('quantity', [u.arcsec, 5 * u.arcsec, 1 * u.degree, 1 * u.radian])
def test_beam_major_quantity(quantity):
    f = FITSFigure(HDU)
    f.show_grayscale()
    f.add_beam(major=quantity, minor=0.04, angle=10.)
    f.beam.set_major(quantity)
    f.close()


def test_beam_minor():
    f = FITSFigure(HDU)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_minor(0.05)
    f.beam.set_minor(0.08)
    f.close()


@pytest.mark.parametrize('quantity', [u.arcsec, 5 * u.arcsec, 1 * u.degree, 1 * u.radian])
def test_beam_minor_quantity(quantity):
    f = FITSFigure(HDU)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=quantity, angle=10.)
    assert type(f.beam) is not list
    f.beam.set_minor(quantity)
    f.close()


def test_beam_angle():
    f = FITSFigure(HDU)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_angle(0.)
    f.beam.set_angle(55.)
    f.close()


@pytest.mark.parametrize('quantity', [u.arcsec, 5 * u.arcsec, 1 * u.degree, 1 * u.radian])
def test_beam_angle_quantity(quantity):
    f = FITSFigure(HDU)
    f.show_grayscale()
    f.add_beam(major=0.1, minor=0.04, angle=quantity)
    f.beam.set_angle(quantity)
    f.close()


def test_beam_corner():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    for corner in ['top', 'bottom', 'left', 'right', 'top left', 'top right',
                   'bottom left', 'bottom right']:
        f.beam.set_corner(corner)
    f.close()


def test_beam_frame():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_frame(True)
    f.beam.set_frame(False)
    f.close()


def test_beam_borderpad():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_borderpad(0.1)
    f.beam.set_borderpad(0.3)
    f.close()


def test_beam_pad():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_pad(0.1)
    f.beam.set_pad(0.3)
    f.close()


def test_beam_alpha():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_alpha(0.1)
    f.beam.set_alpha(0.2)
    f.beam.set_alpha(0.5)
    f.close()


def test_beam_color():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_color('black')
    f.beam.set_color('#003344')
    f.beam.set_color((1.0, 0.4, 0.3))
    f.close()


def test_beam_facecolor():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_facecolor('black')
    f.beam.set_facecolor('#003344')
    f.beam.set_facecolor((1.0, 0.4, 0.3))
    f.close()


def test_beam_edgecolor():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_edgecolor('black')
    f.beam.set_edgecolor('#003344')
    f.beam.set_edgecolor((1.0, 0.4, 0.3))
    f.close()


def test_beam_linestyle():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_linestyle('solid')
    f.beam.set_linestyle('dotted')
    f.beam.set_linestyle('dashed')
    f.close()


def test_beam_linewidth():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.beam.set_linewidth(0)
    f.beam.set_linewidth(1)
    f.beam.set_linewidth(5)
    f.close()


def test_beam_hatch():
    f = FITSFigure(HDU)
    f.add_beam(major=0.1, minor=0.04, angle=10.)
    for hatch in ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']:
        f.beam.set_hatch(hatch)
    f.close()


def test_beam_multiple():

    f = FITSFigure(HDU)
    f.show_grayscale()

    f.add_beam(major=0.1, minor=0.04, angle=10.)
    f.add_beam(major=0.2, minor=0.08, angle=10.)
    f.add_beam(major=0.15, minor=0.08, angle=10.)

    assert len(f.beam) == 3

    with pytest.raises(Exception) as exc:
        f.remove_beam()
    assert exc.value.args[0] == ('More than one beam present - use beam_index= '
                                 'to specify which one to remove')
    f.remove_beam(beam_index=2)

    assert len(f.beam) == 2

    f.remove_beam(beam_index=1)

    assert isinstance(f.beam, Beam)

    f.remove_beam()

    assert not hasattr(f, 'beam')

    f.close()
