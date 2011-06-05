import numpy as np


def convert_coords(x, y, input, output):

    system_in, equinox_in = input
    system_out, equinox_out = output

    if input == output:
        return x, y

    if system_in == 'galactic' and system_out == 'equatorial':

        if equinox_out == 'j2000':
            x, y = gal2fk5(x, y)
        elif equinox_out == 'b1950':
            x, y = gal2fk5(x, y)
            x, y = j2000tob1950(x, y)
        else:
            raise Exception("Cannot convert from galactic to equatorial coordinates for equinox=%s" % equinox_out)

    elif system_in == 'equatorial' and system_out == 'galactic':

        if equinox_in == 'j2000':
            x, y = fk52gal(x, y)
        elif equinox_in == 'b1950':
            x, y = b1950toj2000(x, y)
            x, y = fk52gal(x, y)
        else:
            raise Exception("Cannot convert from equatorial to equatorial coordinates for equinox=%s" % equinox_in)

    elif system_in == 'equatorial' and system_out == 'equatorial':

        if equinox_in == 'b1950' and equinox_out == 'j2000':
            x, y = b1950toj2000(x, y)
        elif equinox_in == 'j2000' and equinox_out == 'b1950':
            x, y = j2000tob1950(x, y)
        else:
            raise Exception("Cannot convert between equatorial coordinates for equinoxes %s and %s" % (equinox_in, equinox_out))

    else:
        raise Exception("Cannot (yet) convert between %s, %s and %s, %s" % (system_in, equinox_in, system_out, equinox_out))

    return x, y


def precession_matrix(equinox1, equinox2, fk4=False):
    "Adapted from the IDL astronomy library"

    deg_to_rad = np.pi / 180.
    sec_to_rad = deg_to_rad / 3600.

    t = 0.001 * (equinox2 - equinox1)

    if not fk4:

        st = 0.001 * (equinox1 - 2000.)

        # Compute 3 rotation angles
        a = sec_to_rad * t * (23062.181 + st * (139.656 + 0.0139 * st) + t * (30.188 - 0.344 * st + 17.998 * t))
        b = sec_to_rad * t * t * (79.280 + 0.410 * st + 0.205 * t) + a
        c = sec_to_rad * t * (20043.109 - st * (85.33 + 0.217 * st) + t * (- 42.665 - 0.217 * st - 41.833 * t))

    else:

        st = 0.001 * (equinox1 - 1900.)

        # Compute 3 rotation angles
        a = sec_to_rad * t * (23042.53 + st * (139.75 + 0.06 * st) + t * (30.23 - 0.27 * st + 18.0 * t))
        b = sec_to_rad * t * t * (79.27 + 0.66 * st + 0.32 * t) + a
        c = sec_to_rad * t * (20046.85 - st * (85.33 + 0.37 * st) + t * (- 42.67 - 0.37 * st - 41.8 * t))

    sina = np.sin(a)
    sinb = np.sin(b)
    sinc = np.sin(c)
    cosa = np.cos(a)
    cosb = np.cos(b)
    cosc = np.cos(c)

    r = np.matrix([[cosa * cosb * cosc - sina * sinb, sina * cosb + cosa * sinb * cosc,  cosa * sinc],
                   [- cosa * sinb - sina * cosb * cosc, cosa * cosb - sina * sinb * cosc, - sina * sinc],
                   [- cosb * sinc, - sinb * sinc, cosc]])

    return r

P1 = precession_matrix(1950., 2000.)
P2 = precession_matrix(2000., 1950.)


def b1950toj2000(ra, dec):
    '''
    Convert B1950 to J2000 coordinates.

    This routine is based on the technique described at
    http://www.stargazing.net/kepler/b1950.html
    '''

    # Convert to radians
    ra = np.radians(ra)
    dec = np.radians(dec)

    # Convert RA, Dec to rectangular coordinates
    x = np.cos(ra) * np.cos(dec)
    y = np.sin(ra) * np.cos(dec)
    z = np.sin(dec)

    # Apply the precession matrix
    x2 = P1[0, 0] * x + P1[1, 0] * y + P1[2, 0] * z
    y2 = P1[0, 1] * x + P1[1, 1] * y + P1[2, 1] * z
    z2 = P1[0, 2] * x + P1[1, 2] * y + P1[2, 2] * z

    # Convert the new rectangular coordinates back to RA, Dec
    ra = np.arctan2(y2, x2)
    dec = np.arcsin(z2)

    # Convert to degrees
    ra = np.degrees(ra)
    dec = np.degrees(dec)

    # Make sure ra is between 0. and 360.
    ra = np.mod(ra, 360.)
    dec = np.mod(dec + 90., 180.) - 90.

    return ra, dec


def j2000tob1950(ra, dec):
    '''
    Convert J2000 to B1950 coordinates.

    This routine was derived by taking the inverse of the b1950toj2000 routine
    '''

    # Convert to radians
    ra = np.radians(ra)
    dec = np.radians(dec)

    # Convert RA, Dec to rectangular coordinates
    x = np.cos(ra) * np.cos(dec)
    y = np.sin(ra) * np.cos(dec)
    z = np.sin(dec)

    # Apply the precession matrix
    x2 = P2[0, 0] * x + P2[1, 0] * y + P2[2, 0] * z
    y2 = P2[0, 1] * x + P2[1, 1] * y + P2[2, 1] * z
    z2 = P2[0, 2] * x + P2[1, 2] * y + P2[2, 2] * z

    # Convert the new rectangular coordinates back to RA, Dec
    ra = np.arctan2(y2, x2)
    dec = np.arcsin(z2)

    # Convert to degrees
    ra = np.degrees(ra)
    dec = np.degrees(dec)

    # Make sure ra is between 0. and 360.
    ra = np.mod(ra, 360.)
    dec = np.mod(dec + 90., 180.) - 90.

    return ra, dec

# Galactic conversion constants
RA_NGP = np.radians(192.859508333333)
DEC_NGP = np.radians(27.1283361111111)
L_CP = np.radians(122.932)
L_0 = L_CP - np.pi / 2.
RA_0 = RA_NGP + np.pi / 2.
DEC_0 = np.pi / 2. - DEC_NGP


def gal2fk5(l, b):

    l = np.radians(l)
    b = np.radians(b)

    sind = np.sin(b) * np.sin(DEC_NGP) + np.cos(b) * np.cos(DEC_NGP) * np.sin(l - L_0)

    dec = np.arcsin(sind)

    cosa = np.cos(l - L_0) * np.cos(b) / np.cos(dec)
    sina = (np.cos(b) * np.sin(DEC_NGP) * np.sin(l - L_0) - np.sin(b) * np.cos(DEC_NGP)) / np.cos(dec)

    dec = np.degrees(dec)

    ra = np.arccos(cosa)
    ra[np.where(sina < 0.)] = -ra[np.where(sina < 0.)]

    ra = np.degrees(ra + RA_0)

    ra = np.mod(ra, 360.)
    dec = np.mod(dec + 90., 180.) - 90.

    return ra, dec


def fk52gal(ra, dec):

    ra, dec = np.radians(ra), np.radians(dec)

    np.sinb = np.sin(dec) * np.cos(DEC_0) - np.cos(dec) * np.sin(ra - RA_0) * np.sin(DEC_0)

    b = np.arcsin(np.sinb)

    cosl = np.cos(dec) * np.cos(ra - RA_0) / np.cos(b)
    sinl = (np.sin(dec) * np.sin(DEC_0) + np.cos(dec) * np.sin(ra - RA_0) * np.cos(DEC_0)) / np.cos(b)

    b = np.degrees(b)

    l = np.arccos(cosl)
    l[np.where(sinl < 0.)] = - l[np.where(sinl < 0.)]

    l = np.degrees(l + L_0)

    l = np.mod(l, 360.)
    b = np.mod(b + 90., 180.) - 90.

    return l, b


def system(wcs):

    xcoord = wcs.wcs.ctype[0][0:4]
    ycoord = wcs.wcs.ctype[1][0:4]
    equinox = wcs.wcs.equinox

    if xcoord == 'RA--' and ycoord == 'DEC-':
        system = 'equatorial'
    elif xcoord == 'GLON' and ycoord == 'GLAT':
        system = 'galactic'
    elif xcoord == 'ELON' and ycoord == 'ELAT':
        system = 'ecliptic'
    else:
        print "Warning: cannot determine coordinate system for %s/%s. Assuming equatorial." % (xcoord, ycoord)
        system = 'equatorial'

    if system == 'equatorial':
        if equinox == '' or np.isnan(equinox):
            print "Warning: cannot determine equinox. Assuming J2000."
            equinox = 'j2000'
        elif equinox == 1950.:
            equinox = 'b1950'
        elif equinox == 2000.:
            equinox = 'j2000'
        else:
            raise Exception("Cannot use equinox %s" % equinox)
    else:
        equinox = 'none'

    units = 'degrees'

    return system, equinox, units


def arcperpix(wcs):
    return degperpix(wcs) * 3600.


def degperpix(wcs):
    try:
        pscale = np.sqrt(wcs.wcs.cd[0, 0] ** 2 + wcs.wcs.cd[1, 0] ** 2)
    except AttributeError:
        pscale = np.abs(wcs.wcs.cdelt[0])
    return pscale


def world2pix(wcs, x_world, y_world):
    if np.isscalar(x_world):
        x_pix, y_pix = wcs.wcs_sky2pix(np.array([x_world]), np.array([y_world]), 1)
        return x_pix[0], y_pix[0]
    elif type(x_world) == list:
        x_pix, y_pix = wcs.wcs_sky2pix(np.array(x_world), np.array(y_world), 1)
        return x_pix.tolist(), y_pix.tolist()
    elif type(x_world) in [np.ndarray, np.core.records.recarray, np.ma.core.MaskedArray]:
        return wcs.wcs_sky2pix(x_world, y_world, 1)
    else:
        raise Exception("world2pix should be provided either with two scalars, two lists, or two numpy arrays")


def pix2world(wcs, x_pix, y_pix):
    if np.isscalar(x_pix):
        x_world, y_world = wcs.wcs_pix2sky(np.array([x_pix]), np.array([y_pix]), 1)
        return x_world[0], y_world[0]
    elif type(x_pix) == list:
        x_world, y_world = wcs.wcs_pix2sky(np.array(x_pix), np.array(y_pix), 1)
        return x_world.tolist(), y_world.tolist()
    elif type(x_pix) in [np.ndarray, np.core.records.recarray, np.ma.core.MaskedArray]:
        return wcs.wcs_pix2sky(x_pix, y_pix, 1)
    else:
        raise Exception("pix2world should be provided either with two scalars, two lists, or two numpy arrays")
