from __future__ import absolute_import, print_function, division

import numpy as np

from . import math_util


def smart_round_angle_decimal(x, latitude=False):

    x = np.log10(x)
    e = np.floor(x)
    x -= e
    x = 10. ** x
    divisors_10 = math_util.divisors(10)
    x = math_util.closest(divisors_10, x)
    x = x * 10. ** e

    return x


def _get_label_precision(format):

    if format[0] == "%":
        if "i" in format:
            return 1
        elif "f" in format:
            return 10. ** (-len((format % 1).split('.')[1]))
        elif "e" in format:
            return None  # need to figure this out
        else:
            return None  # need to figure this out
    elif "." in format:
        return 10 ** (-len(format.split('.')[1]))
    else:
        return 1


class InconsistentSpacing(Exception):
    pass


def _check_format_spacing_consistency(format, spacing):
    '''
    Check whether the format can correctly show labels with the specified
    spacing.

    For example, if the tick spacing is set to 1 arcsecond, but the format is
    set to dd:mm, then the labels cannot be correctly shown. Similarly, if the
    spacing is set to 1/1000 of a degree, or 3.6", then a format of dd:mm:ss
    will cause rounding errors, because the spacing includes fractional
    arcseconds.

    This function will raise a warning if the format and spacing are
    inconsistent.
    '''

    label_spacing = _get_label_precision(format)

    if label_spacing is None:
        return  # can't determine minimum spacing, so can't check

    if spacing % label_spacing != 0.:
        raise InconsistentSpacing('Label format and tick spacing are inconsistent. Make sure that the tick spacing is a multiple of the smallest angle that can be represented by the specified format (currently %s). For example, if the format is dd:mm:ss.s, then the tick spacing has to be a multiple of 0.1". Similarly, if the format is hh:mm:ss, then the tick spacing has to be a multiple of 15". If you got this error as a result of interactively zooming in to a small region, this means that the default display format for the labels is not accurate enough, so you will need to increase the format precision.' % format)
