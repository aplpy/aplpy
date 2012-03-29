import numpy as np

from . import math_util as m


class interp1d(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = np.zeros(y.shape, dtype=y.dtype)
        self.dy[:-1] = (self.y[1:] - self.y[:-1]) / (self.x[1:] - self.x[:-1])
        self.dy[-1] = self.dy[-2]

    def __call__(self, x_new):

        ipos = np.searchsorted(self.x, x_new)

        if m.isnumeric(x_new):
            if ipos == 0:
                ipos = 1
            if ipos == len(self.x):
                ipos = len(self.x) - 1
        else:
            ipos[ipos == 0] = 1
            ipos[ipos == len(self.x)] = len(self.x) - 1

        ipos = ipos - 1

        return (x_new - self.x[ipos]) * self.dy[ipos] + self.y[ipos]


def resample(array, factor):

    nx, ny = np.shape(array)

    nx_new = nx / factor
    ny_new = ny / factor

    array2 = np.zeros((nx_new, ny))
    for i in range(nx_new):
        array2[i, :] = np.mean(array[i * factor:(i + 1) * factor, :], axis=0)

    array3 = np.zeros((nx_new, ny_new))
    for j in range(ny_new):
        array3[:, j] = np.mean(array2[:, j * factor:(j + 1) * factor], axis=1)

    return array3


def percentile_function(array):

    array = array.ravel()
    array = array[np.where(np.isnan(array) == False)]
    array = array[np.where(np.isinf(array) == False)]

    n_total = np.shape(array)[0]
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
        if not m.isnumeric(midpoint):
            midpoint = 0.05
        return np.log10(array / midpoint + 1.) / np.log10(1. / midpoint + 1.)
    elif function == 'sqrt':
        return np.sqrt(array)
    elif function == 'arcsinh':
        if not m.isnumeric(midpoint):
            midpoint = -0.033
        return np.arcsinh(array / midpoint) / np.arcsinh(1. / midpoint)
    elif function == 'power':
        return np.power(array, exponent)
    else:
        raise Exception("Unknown function : " + function)
