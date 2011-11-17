from __future__ import absolute_import


def check(header, convention=None, dimensions=[0, 1]):

    ix = dimensions[0] + 1
    iy = dimensions[1] + 1

    ctypex = header['CTYPE%i' % ix]
    crvaly = header['CRVAL%i' % iy]

    # Check for CRVAL2!=0 for CAR projection
    if ctypex[4:] == '-CAR' and crvaly != 0:

        if convention in ['wells', 'calabretta']:
            if convention == 'wells':
                try:
                    crpixy = header['CRPIX%i' % iy]
                    cdelty = header['CDELT%i' % iy]
                except:
                    raise Exception("Need CDELT to be present for wells convention")
                crpixy = crpixy - crvaly / cdelty
                header.update('CRPIX%i' % iy, crpixy)
                header.update('CRVAL%i' % iy, 0.0)
            else:
                pass
        else:
            raise Exception('''WARNING: projection is Plate Caree (-CAR) and
            CRVAL2 is not zero. This can be intepreted either according to
            Wells (1981) or Calabretta (2002). The former defines the
            projection as rectilinear regardless of the value of CRVAL2,
            whereas the latter defines the projection as rectilinear only when
            CRVAL2 is zero. You will need to specify the convention to assume
            by setting either convention='wells' or convention='calabretta'
            when initializing the FITSFigure instance. ''')

    return header
