from __future__ import absolute_import, print_function, division

import numpy as np

from astropy import log


def system(wcs, dimensions=[0, 1]):

    xcoord = wcs.wcs.ctype[dimensions[0]][0:4]
    ycoord = wcs.wcs.ctype[dimensions[1]][0:4]
    equinox = wcs.wcs.equinox

    system = {}

    if xcoord == 'RA--' and ycoord == 'DEC-':
        system['name'] = 'equatorial'
        system['inverted'] = False
    elif ycoord == 'RA--' and xcoord == 'DEC-':
        system['name'] = 'equatorial'
        system['inverted'] = True
    elif xcoord == 'GLON' and ycoord == 'GLAT':
        system['name'] = 'galactic'
        system['inverted'] = False
    elif ycoord == 'GLON' and xcoord == 'GLAT':
        system['name'] = 'galactic'
        system['inverted'] = True
    elif xcoord == 'ELON' and ycoord == 'ELAT':
        system['name'] = 'ecliptic'
        system['inverted'] = False
    elif ycoord == 'ELON' and xcoord == 'ELAT':
        system['name'] = 'ecliptic'
        system['inverted'] = True
    else:
        system['name'] = 'unknown'
        system['inverted'] = False

    if system['name'] == 'equatorial':
        if equinox == '' or np.isnan(equinox) or equinox == 0.:
            log.warning("Cannot determine equinox. Assuming J2000.")
            equinox = 'j2000'
        elif equinox == 1950.:
            equinox = 'b1950'
        elif equinox == 2000.:
            equinox = 'j2000'
        else:
            raise Exception("Cannot use equinox %s" % equinox)
    else:
        equinox = 'none'

    return system, equinox


def world2pix(wcs, x_world, y_world):
    if np.isscalar(x_world) and np.isscalar(y_world):
        x_pix, y_pix = wcs.wcs_world2pix(np.array([x_world]), np.array([y_world]), 0)
        return x_pix[0], y_pix[0]
    elif (type(x_world) == list) and (type(y_world) == list):
        x_pix, y_pix = wcs.wcs_world2pix(np.array(x_world), np.array(y_world), 0)
        return x_pix.tolist(), y_pix.tolist()
    elif isinstance(x_world, np.ndarray) and isinstance(y_world, np.ndarray):
        return wcs.wcs_world2pix(x_world, y_world, 0)
    else:
        raise Exception("world2pix should be provided either with two scalars, two lists, or two numpy arrays")


def pix2world(wcs, x_pix, y_pix):
    if np.isscalar(x_pix) and np.isscalar(y_pix):
        x_world, y_world = wcs.wcs_pix2world(np.array([x_pix]), np.array([y_pix]), 0)
        return x_world[0], y_world[0]
    elif (type(x_pix) == list) and (type(y_pix) == list):
        x_world, y_world = wcs.wcs_pix2world(np.array(x_pix), np.array(y_pix), 0)
        return x_world.tolist(), y_world.tolist()
    elif isinstance(x_pix, np.ndarray) and isinstance(y_pix, np.ndarray):
        return wcs.wcs_pix2world(x_pix, y_pix, 0)
    else:
        raise Exception("pix2world should be provided either with two scalars, two lists, or two numpy arrays")
