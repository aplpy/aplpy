from __future__ import absolute_import, print_function, division

import numpy as np


def isnumeric(value):
    return type(value) in [float, int, np.int8, np.int16, np.int32, \
        np.float32, np.float64]


def smart_range(array):

    array.sort()

    minval = 360.
    i1 = 0
    i2 = 0

    for i in range(0, np.size(array) - 1):
        if 360. - abs(array[i + 1] - array[i]) < minval:
            minval = 360. - abs(array[i + 1] - array[i])
            i1 = i + 1
            i2 = i

    if(max(array) - min(array) < minval):
        i1 = 0
        i2 = np.size(array) - 1

    x_min = array[i1]
    x_max = array[i2]

    if(x_min > x_max):
        x_min = x_min - 360.

    return x_min, x_max


def complete_range(xmin, xmax, spacing):
    if(xmax - xmin < 1):
        spacing = 10
    xstep = (xmax - xmin) / float(spacing)
    r = np.arange(xmin, xmax, xstep)
    if(np.any(r >= xmax)):
        return r
    else:
        return np.hstack([r, xmax])


def closest(array, a):
    ipos = np.argmin(np.abs(a - array))
    return array[ipos]


def divisors(n, dup=False):
    divisors = []
    i = 0
    if n == 1:
        return {1: 1}
    while 1:
        i += 1
        if dup:
            break
        if i == n + 1:
            break
        if n % i == 0:
            divisors[i:i + 1] = [i]
    return np.array(divisors)
