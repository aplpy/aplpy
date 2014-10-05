from __future__ import absolute_import, print_function, division

import numpy as np
try:
    from astropy.convolution import convolve as astropy_convolve, Gaussian2DKernel, Box2DKernel
    make_kernel = None
except ImportError:
    from astropy.nddata import convolve as astropy_convolve, make_kernel


def convolve(image, smooth=3, kernel='gauss'):

    if smooth is None and kernel in ['box', 'gauss']:
        return image

    if smooth is not None and not np.isscalar(smooth):
        raise ValueError("smooth= should be an integer - for more complex "
                         "kernels, pass an array containing the kernel "
                         "to the kernel= option")

    # The Astropy convolution doesn't treat +/-Inf values correctly yet, so we
    # convert to NaN here.

    image_fixed = np.array(image, dtype=float, copy=True)
    image_fixed[np.isinf(image)] = np.nan

    if kernel == 'gauss':
        if make_kernel is None:
            kernel = Gaussian2DKernel(smooth, x_size=smooth * 5, y_size=smooth * 5)
        else:
            kernel = make_kernel((smooth * 5, smooth * 5), smooth, 'gaussian')
    elif kernel == 'box':
        if make_kernel is None:
            kernel = Box2DKernel(smooth, x_size=smooth * 5, y_size=smooth * 5)
        else:
            kernel = make_kernel((smooth * 5, smooth * 5), smooth, 'boxcar')
    else:
        kernel = kernel

    return astropy_convolve(image, kernel, boundary='extend')
