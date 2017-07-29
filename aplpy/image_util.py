# NOT YET CHECKED/SIMPLIFIED

from __future__ import absolute_import, print_function, division

import numbers

import numpy as np
from astropy import log


class interp1d(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = np.zeros(y.shape, dtype=y.dtype)
        self.dy[:-1] = (self.y[1:] - self.y[:-1]) / (self.x[1:] - self.x[:-1])
        self.dy[-1] = self.dy[-2]

    def __call__(self, x_new):

        ipos = np.searchsorted(self.x, x_new)

        if isinstance(x_new, (numbers.Integral, numbers.Real)):
            if ipos == 0:
                ipos = 1
            if ipos == len(self.x):
                ipos = len(self.x) - 1
        else:
            ipos[ipos == 0] = 1
            ipos[ipos == len(self.x)] = len(self.x) - 1

        ipos = ipos - 1

        return (x_new - self.x[ipos]) * self.dy[ipos] + self.y[ipos]


def percentile_function(array):

    if np.all(np.isnan(array) | np.isinf(array)):
        log.warning("Image contains only NaN or Inf values")
        return lambda x: 0

    array = array.ravel()
    array = array[np.where(np.isnan(array) == False)]
    array = array[np.where(np.isinf(array) == False)]

    n_total = np.shape(array)[0]

    if n_total == 0:
        def return_zero(x):
            return 0
        return return_zero
    elif n_total == 1:
        def return_single(x):
            return array[0]
        return return_single

    array = np.sort(array)

    x = np.linspace(0., 100., num=n_total)

    spl = interp1d(x=x, y=array)

    if n_total > 10000:
        x = np.linspace(0., 100., num=10000)
        spl = interp1d(x=x, y=spl(x))

    array = None

    return spl


def stretch(array, function, exponent=2, midpoint=None):

    if function == 'linear':
        return array
    elif function == 'log':
        if isinstance(midpoint, (numbers.Integral, numbers.Real)):
            midpoint = 0.05
        return np.log10(array / midpoint + 1.) / np.log10(1. / midpoint + 1.)
    elif function == 'sqrt':
        return np.sqrt(array)
    elif function == 'arcsinh':
        if isinstance(midpoint, (numbers.Integral, numbers.Real)):
            midpoint = -0.033
        return np.arcsinh(array / midpoint) / np.arcsinh(1. / midpoint)
    elif function == 'power':
        return np.power(array, exponent)
    else:
        raise Exception("Unknown function : " + function)
