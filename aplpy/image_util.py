from __future__ import absolute_import, print_function, division

import numpy as np

from astropy import log
from astropy.visualization import (LinearStretch, LogStretch, SqrtStretch,
                                   PowerStretch, AsinhStretch, BaseInterval,
                                   AsymmetricPercentileInterval)


def resample(array, factor):

    nx, ny = np.shape(array)

    nx_new = nx // factor
    ny_new = ny // factor

    array2 = np.zeros((nx_new, ny))
    for i in range(nx_new):
        array2[i, :] = np.mean(array[i * factor:(i + 1) * factor, :], axis=0)

    array3 = np.zeros((nx_new, ny_new))
    for j in range(ny_new):
        array3[:, j] = np.mean(array2[:, j * factor:(j + 1) * factor], axis=1)

    return array3


class PVInterval(BaseInterval):

    def __init__(self, vmin=None, vmax=None, pmin=0., pmax=100.):
        self.vmin = vmin
        self.vmax = vmax
        self.pmin = pmin
        self.pmax = pmax

    def get_limits(self, values):

        if self.vmin is None or self.vmax is None:
            interval = AsymmetricPercentileInterval(self.pmin, self.pmax, n_samples=10000)
            vmin_auto, vmax_auto = interval.get_limits(values)

        if self.vmin is None:
            vmin = vmin_auto
        else:
            vmin = self.vmin

        if self.vmax is None:
            vmax = vmax_auto
        else:
            vmax = self.vmax

        return vmin, vmax


def get_stretch(stretch=None, exponent=None, vmin=None, vmid=None, vmax=None):

    if stretch == 'linear':
        stretch = LinearStretch()
    elif stretch == 'sqrt':
        stretch = SqrtStretch()
    elif stretch == 'power':
        stretch = PowerStretch(exponent)
    elif stretch == 'log':
        if vmid is None:
            if vmin > 0:
                a = vmax / vmin
            else:
                raise Exception("When using a log stretch, if vmin < 0, then vmid has to be specified")
        else:
            a = (vmax - vmid) / (vmin - vmid) - 1
        stretch = LogStretch(a)
    elif stretch == 'arcsinh':
        if vmid is None:
            a = -1. / 30.
        else:
            a = (vmid - vmin) / (vmax - vmin)
        stretch = AsinhStretch(a)
    else:
        raise ValueError('Unknown stretch: {0}'.format(stretch))

    return stretch


def _matplotlib_pil_bug_present():
    """
    Determine whether PIL images should be pre-flipped due to a bug in Matplotlib.

    Prior to Matplotlib 1.2.0, RGB images provided as PIL objects were
    oriented wrongly. This function tests whether the bug is present.
    """

    from matplotlib.image import pil_to_array

    try:
        from PIL import Image
    except:
        import Image

    array1 = np.array([[1,2],[3,4]], dtype=np.uint8)
    image = Image.fromarray(array1)
    array2 = pil_to_array(image)

    if np.all(array1 == array2):
        log.debug("PIL Image flipping bug not present in Matplotlib")
        return False
    elif np.all(array1 == array2[::-1,:]):
        log.debug("PIL Image flipping bug detected in Matplotlib")
        return True
    else:
        log.warning("Could not properly determine Matplotlib behavior for RGB images - image may be flipped incorrectly")
        return False
