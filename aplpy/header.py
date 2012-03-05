from __future__ import absolute_import

from aplpy.logger import logger

<<<<<<< HEAD
def check(header, convention=None, userwcs=False):
=======
>>>>>>> 25e718cacf533205bc5829f723fe1cff72dfb8d9

def check(header, convention=None, dimensions=[0, 1]):

    ix = dimensions[0] + 1
    iy = dimensions[1] + 1

    # If header does not contain CTYPE keywords, assume that the WCS is
    # missing or incomplete, and replace it with a 1-to-1 pixel mapping
    if 'CTYPE%i' % ix not in header or 'CTYPE%i' % iy not in header:
        logger.warn("No WCS information found in header - using pixel coordinates")
        header.update('CTYPE%i' % ix, 'PIXEL')
        header.update('CTYPE%i' % iy, 'PIXEL')
        header.update('CRVAL%i' % ix, 0.)
        header.update('CRVAL%i' % iy, 0.)
        header.update('CRPIX%i' % ix, 0.)
        header.update('CRPIX%i' % iy, 0.)
        header.update('CDELT%i' % ix, 1.)
        header.update('CDELT%i' % iy, 1.)

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

<<<<<<< HEAD
    # Check that the two projections are equal
    if xproj<>yproj and not userwcs:
        raise Exception("x and y projections do not agree")

    # Check for CRVAL2<>0 for CAR projection
    if xproj == '-CAR' and crval2 <> 0 and not userwcs:
=======
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
>>>>>>> 25e718cacf533205bc5829f723fe1cff72dfb8d9

            else:
                raise Exception('''WARNING: projection is Plate Caree (-CAR) and
                CRVALy is not zero. This can be intepreted either according to
                Wells (1981) or Calabretta (2002). The former defines the
                projection as rectilinear regardless of the value of CRVALy,
                whereas the latter defines the projection as rectilinear only when
                CRVALy is zero. You will need to specify the convention to assume
                by setting either convention='wells' or convention='calabretta'
                when initializing the FITSFigure instance. ''')

    return header
