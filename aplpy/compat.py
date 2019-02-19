# The simple_norm function in astropy is missing a control for the log
# scaling as described in https://github.com/astropy/astropy/issues/8432,
# so for now we include a copy of the fixed function here.


from astropy.visualization.interval import (PercentileInterval,
                                            AsymmetricPercentileInterval,
                                            ManualInterval, MinMaxInterval)

from astropy.visualization.stretch import (LinearStretch, SqrtStretch,
                                           PowerStretch, LogStretch,
                                           AsinhStretch)

from astropy.visualization.mpl_normalize import ImageNormalize

__all__ = ['simple_norm']


def simple_norm(data, stretch='linear', power=1.0, asinh_a=0.1, log_a=1000,
                min_cut=None, max_cut=None, min_percent=None, max_percent=None,
                percent=None, clip=True):

    if percent is not None:
        interval = PercentileInterval(percent)
    elif min_percent is not None or max_percent is not None:
        interval = AsymmetricPercentileInterval(min_percent or 0.,
                                                max_percent or 100.)
    elif min_cut is not None or max_cut is not None:
        interval = ManualInterval(min_cut, max_cut)
    else:
        interval = MinMaxInterval()

    if stretch == 'linear':
        stretch = LinearStretch()
    elif stretch == 'sqrt':
        stretch = SqrtStretch()
    elif stretch == 'power':
        stretch = PowerStretch(power)
    elif stretch == 'log':
        stretch = LogStretch(log_a)
    elif stretch == 'asinh':
        stretch = AsinhStretch(asinh_a)
    else:
        raise ValueError('Unknown stretch: {0}.'.format(stretch))

    vmin, vmax = interval.get_limits(data)

    return ImageNormalize(vmin=vmin, vmax=vmax, stretch=stretch, clip=clip)
