from __future__ import absolute_import, print_function, division

import numpy as np


import warnings
from astropy import log
from astropy.wcs import WCS as AstropyWCS
import astropy.wcs


def decode_ascii(string):
    try:
        return string.decode('ascii')
    except AttributeError:
        return string


class WCS(AstropyWCS):

    def __init__(self, *args, **kwargs):

        if 'slices' in kwargs:
            self._slices = kwargs.pop('slices')
        else:
            self._slices = []

        if 'dimensions' in kwargs:
            self._dimensions = kwargs.pop('dimensions')
        else:
            self._dimensions = [0, 1]

        AstropyWCS.__init__(self, *args, **kwargs)

        # Fix common non-standard units
        self.wcs.unitfix()

        # Now find the values of the coordinates in the slices - only needed if
        # data has more than two dimensions
        if len(self._slices) > 0:

            self.nx = args[0]['NAXIS%i' % (self._dimensions[0] + 1)]
            self.ny = args[0]['NAXIS%i' % (self._dimensions[1] + 1)]
            xpix = np.arange(self.nx) + 1.
            ypix = np.arange(self.ny) + 1.
            xpix, ypix = np.meshgrid(xpix, ypix)
            xpix, ypix = xpix.reshape(self.nx * self.ny), ypix.reshape(self.nx * self.ny)
            s = 0
            coords = []
            for dim in range(self.naxis):
                if dim == self._dimensions[0]:
                    coords.append(xpix)
                elif dim == self._dimensions[1]:
                    coords.append(ypix)
                else:
                    coords.append(np.repeat(self._slices[s], xpix.shape))
                    s += 1
            coords = np.vstack(coords).transpose()
            result = AstropyWCS.wcs_pix2world(self, coords, 1)
            self._mean_world = np.mean(result, axis=0)
            # result = result.transpose()
            # result = result.reshape((result.shape[0],) + (self.ny, self.nx))

        # Now guess what 'type' of values are on each axis
        if self.ctype_x[:4] == 'RA--' or \
           self.ctype_x[1:4] == 'LON':
            self.set_xaxis_coord_type('longitude')
            self.set_xaxis_coord_type('longitude')
        elif self.ctype_x[:4] == 'DEC-' or \
           self.ctype_x[1:4] == 'LAT':
            self.set_xaxis_coord_type('latitude')
            self.set_xaxis_coord_type('latitude')
        else:
            self.set_xaxis_coord_type('scalar')
            self.set_xaxis_coord_type('scalar')

        if self.ctype_y[:4] == 'RA--' or \
           self.ctype_y[1:4] == 'LON':
            self.set_yaxis_coord_type('longitude')
            self.set_yaxis_coord_type('longitude')
        elif self.ctype_y[:4] == 'DEC-' or \
           self.ctype_y[1:4] == 'LAT':
            self.set_yaxis_coord_type('latitude')
            self.set_yaxis_coord_type('latitude')
        else:
            self.set_yaxis_coord_type('scalar')
            self.set_yaxis_coord_type('scalar')

    @property
    def is_celestial(self):
        return self.wcs.lng in self._dimensions and self.wcs.lat in self._dimensions

    @property
    def pixel_scale_matrix(self):

        # Only for the subset of dimensions used here

        d0 = self._dimensions[0]
        d1 = self._dimensions[1]

        cdelt = np.matrix([[self.wcs.get_cdelt()[d0],0],
                           [0, self.wcs.get_cdelt()[d1]]])

        pc_full = self.wcs.get_pc()
        pc = np.matrix([[pc_full[d0,d0], pc_full[d0,d1]],
                        [pc_full[d1,d0], pc_full[d1,d1]]])

        m = np.array(cdelt * pc)

        return m

    def set_xaxis_coord_type(self, coord_type):
        if coord_type in ['longitude', 'latitude', 'scalar']:
            self.xaxis_coord_type = coord_type
        else:
            raise Exception("coord_type should be one of longitude/latitude/scalar")

    def set_yaxis_coord_type(self, coord_type):
        if coord_type in ['longitude', 'latitude', 'scalar']:
            self.yaxis_coord_type = coord_type
        else:
            raise Exception("coord_type should be one of longitude/latitude/scalar")

    def __getattr__(self, attribute):

        if attribute[-2:] == '_x':
            axis = self._dimensions[0]
        elif attribute[-2:] == '_y':
            axis = self._dimensions[1]
        else:
            raise AttributeError("Attribute %s does not exist" % attribute)

        if attribute[:5] == 'ctype':
            return decode_ascii(self.wcs.ctype[axis])
        elif attribute[:5] == 'cname':
            return decode_ascii(self.wcs.cname[axis])
        elif attribute[:5] == 'cunit':
            return str(self.wcs.cunit[axis])
        elif attribute[:5] == 'crval':
            return decode_ascii(self.wcs.crval[axis])
        elif attribute[:5] == 'crpix':
            return decode_ascii(self.wcs.crpix[axis])
        else:
            raise AttributeError("Attribute %s does not exist" % attribute)

    def wcs_world2pix(self, x, y, origin):
        if self.naxis == 2:
            if self._dimensions[1] < self._dimensions[0]:
                xp, yp = AstropyWCS.wcs_world2pix(self, y, x, origin)
                return yp, xp
            else:
                return AstropyWCS.wcs_world2pix(self, x, y, origin)
        else:
            coords = []
            s = 0
            for dim in range(self.naxis):
                if dim == self._dimensions[0]:
                    coords.append(x)
                elif dim == self._dimensions[1]:
                    coords.append(y)
                else:
                    # The following is an approximation, and will break down if
                    # the world coordinate changes significantly over the slice
                    coords.append(np.repeat(self._mean_world[dim], x.shape))
                    s += 1
            coords = np.vstack(coords).transpose()

            # Due to a bug in pywcs, we need to loop over each coordinate
            # result = AstropyWCS.wcs_world2pix(self, coords, origin)
            result = np.zeros(coords.shape)
            for i in range(result.shape[0]):
                result[i:i + 1, :] = AstropyWCS.wcs_world2pix(self, coords[i:i + 1, :], origin)

            return result[:, self._dimensions[0]], result[:, self._dimensions[1]]

    def wcs_pix2world(self, x, y, origin):
        if self.naxis == 2:
            if self._dimensions[1] < self._dimensions[0]:
                xw, yw = AstropyWCS.wcs_pix2world(self, y, x, origin)
                return yw, xw
            else:
                return AstropyWCS.wcs_pix2world(self, x, y, origin)
        else:
            coords = []
            s = 0
            for dim in range(self.naxis):
                if dim == self._dimensions[0]:
                    coords.append(x)
                elif dim == self._dimensions[1]:
                    coords.append(y)
                else:
                    coords.append(np.repeat(self._slices[s] + 0.5, x.shape))
                    s += 1
            coords = np.vstack(coords).transpose()
            result = AstropyWCS.wcs_pix2world(self, coords, origin)
            return result[:, self._dimensions[0]], result[:, self._dimensions[1]]


def convert_coords(x, y, input, output):

    system_in, equinox_in = input
    system_out, equinox_out = output

    if input == output:
        return x, y

    # Need to take into account inverted coords

    if system_in['name'] == 'galactic' and system_out['name'] == 'equatorial':

        if equinox_out == 'j2000':
            x, y = gal2fk5(x, y)
        elif equinox_out == 'b1950':
            x, y = gal2fk5(x, y)
            x, y = j2000tob1950(x, y)
        else:
            raise Exception("Cannot convert from galactic to equatorial coordinates for equinox=%s" % equinox_out)

    elif system_in['name'] == 'equatorial' and system_out['name'] == 'galactic':

        if equinox_in == 'j2000':
            x, y = fk52gal(x, y)
        elif equinox_in == 'b1950':
            x, y = b1950toj2000(x, y)
            x, y = fk52gal(x, y)
        else:
            raise Exception("Cannot convert from equatorial to equatorial coordinates for equinox=%s" % equinox_in)

    elif system_in['name'] == 'equatorial' and system_out['name'] == 'equatorial':

        if equinox_in == 'b1950' and equinox_out == 'j2000':
            x, y = b1950toj2000(x, y)
        elif equinox_in == 'j2000' and equinox_out == 'b1950':
            x, y = j2000tob1950(x, y)
        elif equinox_in == equinox_out:
            pass
        else:
            raise Exception("Cannot convert between equatorial coordinates for equinoxes %s and %s" % (equinox_in, equinox_out))

    else:
        raise Exception("Cannot (yet) convert between %s, %s and %s, %s" % (system_in['name'], equinox_in, system_out['name'], equinox_out))

    # Take into account inverted coordinates
    if system_in['inverted'] is system_out['inverted']:
        return x, y
    else:
        return y, x


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

    sinb = np.sin(dec) * np.cos(DEC_0) - np.cos(dec) * np.sin(ra - RA_0) * np.sin(DEC_0)

    b = np.arcsin(sinb)

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

    xcoord = wcs.ctype_x[0:4]
    ycoord = wcs.ctype_y[0:4]
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

    units = 'degrees'

    return system, equinox, units


def world2pix(wcs, x_world, y_world):
    if np.isscalar(x_world) and np.isscalar(y_world):
        x_pix, y_pix = wcs.wcs_world2pix(np.array([x_world]), np.array([y_world]), 1)
        return x_pix[0], y_pix[0]
    elif (type(x_world) == list) and (type(y_world) == list):
        x_pix, y_pix = wcs.wcs_world2pix(np.array(x_world), np.array(y_world), 1)
        return x_pix.tolist(), y_pix.tolist()
    elif isinstance(x_world, np.ndarray) and isinstance(y_world, np.ndarray):
        return wcs.wcs_world2pix(x_world, y_world, 1)
    else:
        raise Exception("world2pix should be provided either with two scalars, two lists, or two numpy arrays")


def pix2world(wcs, x_pix, y_pix):
    if np.isscalar(x_pix) and np.isscalar(y_pix):
        x_world, y_world = wcs.wcs_pix2world(np.array([x_pix]), np.array([y_pix]), 1)
        return x_world[0], y_world[0]
    elif (type(x_pix) == list) and (type(y_pix) == list):
        x_world, y_world = wcs.wcs_pix2world(np.array(x_pix), np.array(y_pix), 1)
        return x_world.tolist(), y_world.tolist()
    elif isinstance(x_pix, np.ndarray) and isinstance(y_pix, np.ndarray):
        return wcs.wcs_pix2world(x_pix, y_pix, 1)
    else:
        raise Exception("pix2world should be provided either with two scalars, two lists, or two numpy arrays")


def celestial_pixel_scale(wcs):
    """
    If the pixels are square, return the pixel scale in the spatial
    dimensions
    """

    if not wcs.is_celestial:
        raise ValueError("WCS is not celestial, cannot determine celestial pixel scale")

    # Extract celestial part of WCS and sanitize
    from astropy.wcs import WCSSUB_CELESTIAL
    wcs = wcs.sub([WCSSUB_CELESTIAL])

    pccd = wcs.pixel_scale_matrix

    scale = np.sqrt((pccd ** 2).sum(axis=0))

    if not np.allclose(scale[0], scale[1]):
        warnings.warn("Pixels are not square, using an average pixel scale")
        return np.mean(scale)
    else:
        return scale[0]


def non_celestial_pixel_scales(wcs):

    if wcs.is_celestial:
        raise ValueError("WCS is celestial, use celestial_pixel_scale instead")

    pccd = wcs.pixel_scale_matrix

    if np.allclose(pccd[1,0], 0) and np.allclose(pccd[0,1], 0):
        return np.abs(np.diagonal(pccd))
    else:
        raise ValueError("WCS is rotated, cannot determine consistent pixel scales")
