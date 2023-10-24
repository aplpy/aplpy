__all__ = ['_slice_wcs']


def _slice_wcs(wcs, wcsaxes_slices):
    """
    Given a WCS and a WCSAxes-compatible slices tuple, return a sliced
    version of the WCS
    """

    if wcsaxes_slices == ('x', 'y'):
        return wcs

    ix = wcsaxes_slices.index('x')
    iy = wcsaxes_slices.index('y')

    # We start off by swapping the dimensions if needed. At this point we can assume we
    # are using a FITS WCS so that we can use sub()
    if ix > iy:
        axes = [x + 1 for x in range(frame.pixel_n_dim)]
        axes[ix] = iy + 1
        axes[iy] = ix + 1
        frame = frame.sub(list(axes))

    # Next, we convert the slices to something we can use to slice the contour WCS
    wcs_slices = list(wcsaxes_slices)
    wcs_slices[ix] = slice(None)
    wcs_slices[iy] = slice(None)

    # Invert this so that we are in Numpy axis order
    wcs_slices = wcs_slices[::-1]

    # Apply the slices to the WCS to get a 2-d WCS out
    return wcs[wcs_slices]
