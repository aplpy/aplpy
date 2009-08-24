import pywcs


def check(header, convention=None):

    wcs = pywcs.WCS(header)

    xproj = header['CTYPE1']
    yproj = header['CTYPE2']

    xproj = xproj[4:8]
    yproj = yproj[4:8]

    crpix1 = float(header['CRPIX1'])
    crpix2 = float(header['CRPIX2'])

    crval1 = float(header['CRVAL1'])
    crval2 = float(header['CRVAL2'])

    nx = int(header['NAXIS1'])
    ny = int(header['NAXIS1'])

    xcp = float(nx / 2)
    ycp = float(ny / 2)

    # Check that the two projections are equal
    if xproj<>yproj:
        raise Exception("x and y projections do not agree")

    # Check for CRVAL2<>0 for CAR projection
    if xproj == '-CAR' and crval2 <> 0:

        if convention in ['wells', 'calabretta']:
            if convention=='wells':
                cdelt2 = float(header['CDELT2'])
                crpix2 = crpix2 - crval2 / cdelt2
                header.update('CRPIX2', crpix2)
                header.update('CRVAL2', 0.0)
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

    # Remove any extra coordinates
    for key in ['CTYPE', 'CRPIX', 'CRVAL', 'CUNIT', 'CDELT', 'CROTA']:
        for coord in range(3, 6):
            name = key + str(coord)
            if name in header:
                header.__delitem__(name)

    return header
