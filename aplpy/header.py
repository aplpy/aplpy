from __future__ import absolute_import, print_function, division

from astropy import log


def check(header, convention=None, dimensions=[0, 1]):

    ix = dimensions[0] + 1
    iy = dimensions[1] + 1

    # If header does not contain CTYPE keywords, assume that the WCS is
    # missing or incomplete, and replace it with a 1-to-1 pixel mapping
    if 'CTYPE%i' % ix not in header or 'CTYPE%i' % iy not in header:
        log.warning("No WCS information found in header - using pixel coordinates")
        header['CTYPE%i' % ix] = 'PIXEL'
        header['CTYPE%i' % iy] = 'PIXEL'
        header['CRVAL%i' % ix] = 0.
        header['CRVAL%i' % iy] = 0.
        header['CRPIX%i' % ix] = 0.
        header['CRPIX%i' % iy] = 0.
        header['CDELT%i' % ix] = 1.
        header['CDELT%i' % iy] = 1.

    if header['CTYPE%i' % ix][4:] == '-CAR' and header['CTYPE%i' % iy][4:] == '-CAR':

        if header['CTYPE%i' % ix][:4] == 'DEC-' or header['CTYPE%i' % ix][1:4] == 'LAT':
            ilon = iy
            ilat = ix
        elif header['CTYPE%i' % iy][:4] == 'DEC-' or header['CTYPE%i' % iy][1:4] == 'LAT':
            ilon = ix
            ilat = iy
        else:
            ilon = None
            ilat = None

        if ilat is not None and header['CRVAL%i' % ilat] != 0:

            if convention == 'calabretta':
                pass  # we don't need to do anything
            elif convention == 'wells':
                if 'CDELT%i' % ilat not in header:
                    raise Exception("Need CDELT%i to be present for wells convention" % ilat)
                crpix = header['CRPIX%i' % ilat]
                crval = header['CRVAL%i' % ilat]
                cdelt = header['CDELT%i' % ilat]
                crpix = crpix - crval / cdelt
                try:
                    header['CRPIX%i' % ilat] = crpix
                    header['CRVAL%i' % ilat] = 0.
                except:  # older versions of PyFITS
                    header.update('CRPIX%i' % ilat, crpix)
                    header.update('CRVAL%i' % ilon, 0.)

            else:
                raise Exception('''WARNING: projection is Plate Caree (-CAR) and
                CRVALy is not zero. This can be interpreted either according to
                Wells (1981) or Calabretta (2002). The former defines the
                projection as rectilinear regardless of the value of CRVALy,
                whereas the latter defines the projection as rectilinear only when
                CRVALy is zero. You will need to specify the convention to assume
                by setting either convention='wells' or convention='calabretta'
                when initializing the FITSFigure instance. ''')

    return header
