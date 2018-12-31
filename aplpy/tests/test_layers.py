from __future__ import absolute_import, print_function, division

import pytest
import numpy as np

from .. import FITSFigure


def test_layers(capsys):

    f = FITSFigure(np.arange(256).reshape((16, 16)))

    capsys.readouterr()

    # No layers

    f.list_layers()

    captured = capsys.readouterr()
    assert captured.out.strip() == ('There are no layers in this figure')

    # Two layers

    f.show_markers([360., 350., 340.], [-61., -62., -63], color='cyan', layer='markers')
    f.show_markers([360., 350., 340.], [-61., -62., -63], color='cyan', layer='extra_markers')

    capsys.readouterr()

    f.list_layers()

    captured = capsys.readouterr()
    assert captured.out.strip() == ('There are 2 layers in this figure:\n\n'
                                    '   -> markers\n'
                                    '   -> extra_markers')

    # Check removing layers

    f.remove_layer('extra_markers')

    f.list_layers()

    captured = capsys.readouterr()
    assert captured.out.strip() == ('There is one layer in this figure:\n\n'
                                    '   -> markers')

    # Check all layer types and overwriting layers

    f.show_markers([30, 40], [50, 70], layer='markers')

    f.show_circles([360., 350., 340.], [-61., -62., -63], [0.5, 0.4, 0.3], layer='circles')
    f.show_circles([30, 40], [50, 70], [10, 20], layer='circles')

    f.show_ellipses(340., -66., 1.5, 2., 10., layer='ellipses')
    f.show_ellipses(120, 60, 20, 40, 20., layer='ellipses')

    f.show_rectangles([355., 350.], [-71, -72], [0.5, 1], [2, 1], angle=[20, 30], layer='rectangles')
    f.show_rectangles([66, 80], [20, 30], [10, 14], [20, 22], angle=[20, 30], layer='rectangles')

    f.show_arrows([340., 360], [-72, -68], [2, -2], [2, 2], layer='arrows')
    f.show_arrows([340., 360], [-72, -68], [2, -2], [2, 2], layer='arrows')

    poly = np.array([[330, 340, 360], [-65, -61, -63]])
    f.show_polygons([poly], layer='polygons')
    f.show_polygons([poly], layer='polygons')

    f.show_lines([poly], layer='lines')
    f.show_lines([poly], layer='lines')

    f.add_label(350., -66., 'text', layer='label')
    f.add_label(0.4, 0.25, 'text', relative=True, layer='label')

    # FIXME: Uncomment the following once
    # https://github.com/astropy/astropy/pull/8321 is merged into Astropy and in
    # a bug fix release.
    # f.show_contour(layer='contours')

    f.list_layers()

    captured = capsys.readouterr()
    assert captured.out.strip() == ('There are 8 layers in this figure:\n\n'
                                    '   -> markers\n'
                                    '   -> circles\n'
                                    '   -> ellipses\n'
                                    '   -> rectangles\n'
                                    '   -> arrows\n'
                                    '   -> polygons\n'
                                    '   -> lines\n'
                                    '   -> label')

    # Hiding/showing layers

    f.hide_layer('ellipses')
    f.hide_layer('polygons')

    f.list_layers()

    captured = capsys.readouterr()
    assert captured.out.strip() == ('There are 8 layers in this figure:\n\n'
                                    '   -> markers\n'
                                    '   -> circles\n'
                                    '   -> ellipses (hidden)\n'
                                    '   -> rectangles\n'
                                    '   -> arrows\n'
                                    '   -> polygons (hidden)\n'
                                    '   -> lines\n'
                                    '   -> label')

    layer = f.get_layer('circles')
    assert layer.get_visible()

    layer = f.get_layer('ellipses')
    assert not layer.get_visible()

    f.show_layer('ellipses')

    f.list_layers()

    captured = capsys.readouterr()
    assert captured.out.strip() == ('There are 8 layers in this figure:\n\n'
                                    '   -> markers\n'
                                    '   -> circles\n'
                                    '   -> ellipses\n'
                                    '   -> rectangles\n'
                                    '   -> arrows\n'
                                    '   -> polygons (hidden)\n'
                                    '   -> lines\n'
                                    '   -> label')

    layer = f.get_layer('ellipses')
    assert layer.get_visible()


def test_non_existent_layers():

    # Handling non-existent layers

    f = FITSFigure(np.arange(256).reshape((16, 16)))

    with pytest.raises(Exception) as exc:
        f.get_layer('banana')
    assert exc.value.args[0] == 'Layer banana does not exist'

    assert f.get_layer('banana', raise_exception=False) is None

    with pytest.raises(Exception) as exc:
        f.show_layer('banana')
    assert exc.value.args[0] == 'Layer banana does not exist'

    f.show_layer('banana', raise_exception=False)

    with pytest.raises(Exception) as exc:
        f.hide_layer('banana')
    assert exc.value.args[0] == 'Layer banana does not exist'

    f.hide_layer('banana', raise_exception=False)

    with pytest.raises(Exception) as exc:
        f.remove_layer('banana')
    assert exc.value.args[0] == 'Layer banana does not exist'

    f.remove_layer('banana', raise_exception=False)
