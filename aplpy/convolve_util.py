from __future__ import absolute_import, print_function, division

from astropy.nddata import convolve as nddata_convolve, make_kernel


def convolve(image, smooth=3, kernel='gauss'):

    if smooth is None:
        return image

    if kernel == 'gauss':
        kernel = make_kernel((smooth * 5, smooth * 5), smooth, 'gaussian')
    elif kernel == 'box':
        kernel = make_kernel((smooth * 5, smooth * 5), smooth, 'boxcar')
    else:
        kernel = kernel

    return nddata_convolve(image, kernel)
