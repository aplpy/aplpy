import numpy as np

ra_ngp=np.radians(192.859508333333)
dec_ngp=np.radians(27.1283361111111)
l_cp=np.radians(122.932)
l_0=l_cp-np.pi/2.
ra_0=ra_ngp+np.pi/2.
dec_0=np.pi/2.-dec_ngp


def convert_coords(x, y, input, output):

    system_in, equinox_in = input
    system_out, equinox_out = output

    if input == output:
        return x, y

    if system_in == 'galactic' and (system_out == 'celestial' and equinox_out == 'j2000'):
        x, y = gal2fk5(x, y)

    elif (system_in == 'celestial' and  equinox_in == 'j2000') and system_out == 'galactic':
        x, y = fk52gal(x, y)

    else:
        raise Exception("Cannot (yet) convert between "+system_in+", "+equinox_in+" and "+system_out+", "+equinox_out)

    return x, y


def gal2fk5(l, b):

    l = np.radians(l)
    b = np.radians(b)

    sind = np.sin(b) * np.sin(dec_ngp) + np.cos(b) * np.cos(dec_ngp) * np.sin(l-l_0)

    dec = np.arcsin(sind)

    cosa = np.cos(l-l_0) * np.cos(b) / np.cos(dec)
    sina = (np.cos(b) * np.sin(dec_ngp) * np.sin(l-l_0) - np.sin(b) * np.cos(dec_ngp)) / np.cos(dec)

    dec = np.degrees(dec)

    ra = np.arccos(cosa)
    ra[np.where(sina < 0.)] = -ra[np.where(sina < 0.)]

    ra = np.degrees(ra + ra_0)

    ra = np.mod(ra, 360.)
    dec = np.mod(dec+90., 180.)-90.

    return ra, dec


def fk52gal(ra, dec):

    ra, dec = np.radians(ra), np.radians(dec)

    np.sinb = np.sin(dec) * np.cos(dec_0) - np.cos(dec) * np.sin(ra-ra_0) * np.sin(dec_0)

    b = np.arcsin(np.sinb)

    cosl = np.cos(dec) * np.cos(ra-ra_0) / np.cos(b)
    sinl = (np.sin(dec) * np.sin(dec_0) + np.cos(dec) * np.sin(ra-ra_0) * np.cos(dec_0)) / np.cos(b)

    b = np.degrees(b)

    l = np.arccos(cosl)
    l[np.where(sinl < 0.)] = - l[np.where(sinl < 0.)]

    l = np.degrees(l+l_0)

    l = np.mod(l, 360.)
    b = np.mod(b+90., 180.)-90.

    return l, b


def system(wcs):

    xcoord = wcs.wcs.ctype[0][0:4]
    ycoord = wcs.wcs.ctype[1][0:4]
    equinox = wcs.wcs.equinox

    if xcoord=='RA--' and ycoord=='DEC-':
        system = 'celestial'
    elif xcoord=='GLON' and ycoord=='GLAT':
        system = 'galactic'
    elif xcoord=='ELON' and ycoord=='ELAT':
        system = 'ecliptic'
    else:
        print "Warning: cannot determine coordinate system for "+xcoord+"/"+ycoord+". Assuming celestial."
        system = 'celestial'

    if system == 'celestial':
        if equinox == '' or np.isnan(equinox):
            print "Warning: cannot determine equinox. Assuming J2000."
            equinox = 'j2000'
        elif equinox == 1950.:
            equinox = 'b1950'
        elif equinox == 2000.:
            equinox = 'j2000'
        else:
            raise Exception("Cannot use equinox "+str(equinox))
    else:
        equinox = 'none'

    units = 'degrees'

    return system, equinox, units


def arcperpix(wcs):
    return degperpix(wcs) * 3600.


def degperpix(wcs):
    try:
        pscale = np.sqrt(wcs.wcs.cd[0, 0]**2 + wcs.wcs.cd[1, 0]**2)
    except AttributeError:
        pscale = np.abs(wcs.wcs.cdelt[0])
    return pscale


def world2pix(wcs, x_world, y_world):
    if type(x_world) == float or type(x_world) == np.float32 or type(x_world) == np.float64:
        x_pix, y_pix = wcs.wcs_sky2pix(np.array([x_world]), np.array([y_world]), 1)
        return x_pix[0], y_pix[0]
    elif type(x_world) == list:
        x_pix, y_pix = wcs.wcs_sky2pix(np.array(x_world), np.array(y_world), 1)
        return x_pix.tolist(), y_pix.tolist()
    elif type(x_world) in [np.ndarray, np.core.records.recarray]:
        return wcs.wcs_sky2pix(x_world, y_world, 1)
    else:
        raise Exception("world2pix should be provided either with two floats, two lists, or two numpy arrays")


def pix2world(wcs, x_pix, y_pix):
    if type(x_pix) == float or type(x_pix) == np.float32 or type(x_pix) == np.float64:
        x_world, y_world = wcs.wcs_pix2sky(np.array([x_pix]), np.array([y_pix]), 1)
        return x_world[0], y_world[0]
    elif type(x_pix) == list:
        x_world, y_world = wcs.wcs_pix2sky(np.array(x_pix), np.array(y_pix), 1)
        return x_world.tolist(), y_world.tolist()
    elif type(x_pix) in [np.ndarray, np.core.records.recarray]:
        return wcs.wcs_pix2sky(x_pix, y_pix, 1)
    else:
        raise Exception("pix2world should be provided either with two floats, two lists, or two numpy arrays")
