import numpy as np

from kapteyn_celestial import skymatrix, longlat2xyz, dotrans, xyz2longlat
import kapteyn_celestial

import pyfits

_wcs_module_import_log = []

_pywcs_installed = False
try:
    import pywcs
except ImportError:
    _wcs_module_import_log.append("Failed to import the pywcs")
else:
    if hasattr(pywcs.WCS, "sub"):
        _pywcs_installed = True
    else:
        _wcs_module_import_log.append("pywcs imported but does not have 'sub' attribute. More recent version of pywcs is required.")

_kapteyn_installed = False
try:
    import kapteyn.wcs
except ImportError:
    _wcs_module_import_log.append("Failed to import the kpateyn.wcs")
else:
    _kapteyn_installed = True


FK4 = (kapteyn_celestial.equatorial, kapteyn_celestial.fk4, 'B1950.0')
FK5 = (kapteyn_celestial.equatorial, kapteyn_celestial.fk5, 'J2000.0')
GAL = kapteyn_celestial.galactic
ICRS = (kapteyn_celestial.equatorial, kapteyn_celestial.fk5, 'J2000.0') # FIXME

coord_system = dict(fk4=FK4,
                    fk5=FK5,
                    gal=GAL,
                    galactic=GAL,
                    icrs=ICRS)

def is_equal_coord_sys(src, dest):
    return (src.lower() == dest.lower())


def is_string_like(obj):
    'Return True if *obj* looks like a string'
    if isinstance(obj, (str, unicode)): return True
    try: obj + ''
    except: return False
    return True


class sky2sky(object):
    def __init__(self, src, dest):

        if is_string_like(src):
            src = coord_system[src.lower()]

        if is_string_like(dest):
            dest = coord_system[dest.lower()]

        self.src = src
        self.dest = dest
        self._skymatrix = skymatrix(src, dest)
        #self.tran = wcs.Transformation(src, dest)

    def inverted(self):
        return sky2sky(self.dest, self.src)

    def _dotran(self, lonlat):
        xyz = longlat2xyz(lonlat)
        xyz2 = dotrans(self._skymatrix, xyz)
        lonlats2 = xyz2longlat(xyz2)
        return lonlats2

    def __call__(self, lon, lat):
        lon, lat = np.asarray(lon), np.asarray(lat)
        lonlat = np.concatenate([lon[:,np.newaxis],
                                 lat[:,np.newaxis]],1)
        ll_dest = np.asarray(self._dotran(lonlat))
        return ll_dest[:,0], ll_dest[:,1]


def coord_system_guess(ctype1_name, ctype2_name, equinox):
    if ctype1_name.upper().startswith("RA") and \
       ctype2_name.upper().startswith("DEC"):
        if equinox == 2000.0:
            return "fk5"
        elif equinox == 1950.0:
            return "fk4"
        elif equinox is None:
            return "fk5"
        else:
            return None
    if ctype1_name.upper().startswith("GLON") and \
       ctype2_name.upper().startswith("GLAT"):
        return "gal"
    return None


class ProjectionBase(object):
    """
    A wrapper for kapteyn.projection or pywcs
    """
    def _get_ctypes(self):
        pass

    def _get_equinox(self):
        pass

    def topixel(self):
        """ 1, 1 base """
        pass

    def toworld(self):
        """ 1, 1 base """
        pass

    def sub(self, axes):
        pass

    def _get_radesys(self):
        ctype1, ctype2 = self.ctypes
        equinox = self.equinox
        radecsys = coord_system_guess(ctype1, ctype2, equinox)
        return radecsys

    radesys = property(_get_radesys)



class ProjectionKapteyn(ProjectionBase):
    """
    A wrapper for kapteyn.projection
    """
    def __init__(self, header):
        if isinstance(header, pyfits.Header):
            self._proj = kapteyn.wcs.Projection(header)
        else:
            self._proj = header

    def _get_ctypes(self):
        return self._proj.ctype

    ctypes = property(_get_ctypes)

    def _get_equinox(self):
        return self._proj.equinox

    equinox = property(_get_equinox)

    def topixel(self, xy):
        """ 1, 1 base """
        return self._proj.topixel(xy)

    def toworld(self, xy):
        """ 1, 1 base """
        return self._proj.toworld(xy)

    def sub(self, axes):
        proj = self._proj.sub(axes=axes)
        return ProjectionKapteyn(proj)


class ProjectionPywcs(ProjectionBase):
    """
    A wrapper for pywcs
    """
    def __init__(self, header):
        if isinstance(header, pyfits.Header):
            self._pywcs = pywcs.WCS(header=header)
        else:
            self._pywcs = header

    def _get_ctypes(self):
        return tuple(self._pywcs.wcs.ctype)

    ctypes = property(_get_ctypes)

    def _get_equinox(self):
        return self._pywcs.wcs.equinox

    equinox = property(_get_equinox)

    def topixel(self, xy):
        """ 1, 1 base """
        xy2 = self._pywcs.wcs_sky2pix(np.asarray(xy).T, 1)
        return xy2[:,0], xy2[:,1]

    def toworld(self, xy):
        """ 1, 1 base """
        xy2 = self._pywcs.wcs_pix2sky(np.asarray(xy).T, 1)
        return xy2[:,0], xy2[:,1]

    def sub(self, axes):
        wcs = self._pywcs.sub(axes=axes)
        return ProjectionPywcs(wcs)


if _kapteyn_installed:
    ProjectionDefault = ProjectionKapteyn
elif _pywcs_installed:
    ProjectionDefault = ProjectionPywcs
else:
    ProjectionDefault = None

if not _kapteyn_installed and not _pywcs_installed:
    def get_kapteyn_projection(header):
        err = ["Either pywcs or Kapteyn python packages are required."]
        err.extend(_wcs_module_import_log)

        raise ImportError("\n".join(err))
else:
    def get_kapteyn_projection(header):
        if _kapteyn_installed and isinstance(header, kapteyn.wcs.Projection):
            projection = ProjectionKapteyn(header)
        elif _pywcs_installed and isinstance(header, pywcs.WCS):
            projection = ProjectionPywcs(header)
        elif isinstance(header, ProjectionBase):
            projection = header
        else:
            projection = ProjectionDefault(header)

        projection = projection.sub(axes=[1,2])
        return projection



def estimate_cdelt_trans(transSky2Pix, x0, y0):

    transPix2Sky = transSky2Pix.inverted()

    lon0, lat0 = transPix2Sky.transform_point((x0, y0))

    lon1, lat1 = transPix2Sky.transform_point((x0+1, y0))
    dlon = (lon1-lon0)*np.cos(lat0/180.*np.pi)
    dlat = (lat1-lat0)
    cd1 = (dlon**2 + dlat**2)**.5

    lon2, lat2 = transPix2Sky.transform_point((x0+1, y0))
    dlon = (lon2-lon0)*np.cos(lat0/180.*np.pi)
    dlat = (lat2-lat0)
    cd2 = (dlon**2 + dlat**2)**.5

    return (cd1*cd2)**.5






def estimate_angle_trans(transSky2Pix, x0, y0):
    """
    return a tuple of two angles (in degree) of increasing direction
    of 1st and 2nd coordinates.

    note that x, y = wcs_proj.topixel(sky_to_sky((l1, l2)))

    """

    cdelt = estimate_cdelt(transSky2Pix, x0, y0)

    transPix2Sky = transSky2Pix.inverted()

    lon0, lat0 = transPix2Sky.transform_point((x0, y0))

    x1, y1 = transSky2Pix.transform_point((lon0 + cdelt*np.cos(lat0/180.*np.pi),
                                           lat0))

    x2, y2 = transSky2Pix.transform_point((lon0, lat0+cdelt))

    a1 = np.arctan2(y1-y0, x1-x0)/np.pi*180.
    a2 = np.arctan2(y2-y0, x2-x0)/np.pi*180.

    return a1, a2


def estimate_cdelt(wcs_proj, x0, y0): #, sky_to_sky):
    lon0, lat0 = wcs_proj.toworld(([x0], [y0]))
    lon1, lat1 = wcs_proj.toworld(([x0+1], [y0]))

    dlon = (lon1[0]-lon0[0])*np.cos(lat0[0]/180.*np.pi)
    dlat = (lat1[0]-lat0[0])
    cd1 = (dlon**2 + dlat**2)**.5

    lon2, lat2 = wcs_proj.toworld(([x0+1], [y0]))
    dlon = (lon2[0]-lon0[0])*np.cos(lat0[0]/180.*np.pi)
    dlat = (lat2[0]-lat0[0])
    cd2 = (dlon**2 + dlat**2)**.5

    return ((cd1*cd2)**.5)


def estimate_angle(wcs_proj, x0, y0, sky_to_sky=None):
    """
    return a tuple of two angles (in degree) of increasing direction
    of 1st and 2nd coordinates.

    note that x, y = wcs_proj.topixel(sky_to_sky((l1, l2)))

    """

    cdelt = estimate_cdelt(wcs_proj, x0, y0)

    #x0, y0 = wcs_proj.topixel((lon0, lat0))
    ll = wcs_proj.toworld(([x0], [y0]))
    lon0, lat0 = sky_to_sky.inverted()(ll[0], ll[1])

    ll = sky_to_sky(lon0 + cdelt*np.cos(lat0/180.*np.pi), lat0)
    x1, y1 = wcs_proj.topixel(ll)
    a1 = np.arctan2(y1-y0, x1-x0)/np.pi*180.

    ll = sky_to_sky(lon0, lat0+cdelt)
    x2, y2 = wcs_proj.topixel(ll)
    a2 = np.arctan2(y2-y0, x2-x0)/np.pi*180.

    return a1[0], a2[0]



select_wcs = coord_system.get

UnknownWcs = "unknown wcs"

image_like_coordformats = ["image", "physical","detector","logical"]

from region_numbers import CoordOdd, CoordEven, Distance, Angle
from parser_helper import Shape, CoordCommand
from region_numbers import SimpleNumber, SimpleInteger

import copy


def convert_to_imagecoord(cl, fl, wcs_proj, sky_to_sky, xy0):
    fl0 = fl
    new_cl = []

    while cl:
        if len(fl) == 0:
            fl = fl0

        if fl[0] == CoordOdd and fl[1] == CoordEven:

            ll = sky_to_sky([cl[0]], [cl[1]])
            x0, y0 = wcs_proj.topixel(ll)
            xy0 = [x0[0], y0[0]]
            new_cl.extend(xy0)
            cl = cl[2:]
            fl = fl[2:]
        elif fl[0] == Distance:
            degree_per_pixel = estimate_cdelt(wcs_proj,
                                              *xy0)
            new_cl.append(cl[0]/degree_per_pixel)
            cl = cl[1:]
            fl = fl[1:]
        elif fl[0] == Angle:
            rot1, rot2 = estimate_angle(wcs_proj, xy0[0], xy0[1], sky_to_sky)
            new_cl.append(cl[0]+rot1-180.)
            cl = cl[1:]
            fl = fl[1:]
        else:
            new_cl.append(cl[0])
            cl = cl[1:]
            fl = fl[1:]

    return new_cl, xy0


def convert_physical_to_imagecoord(cl, fl, pc):
    fl0 = fl
    new_cl = []

    while cl:
        if len(fl) == 0:
            fl = fl0

        if fl[0] == CoordOdd and fl[1] == CoordEven:

            xy0 = pc.to_image(cl[0], cl[1])
            new_cl.extend(xy0)
            cl = cl[2:]
            fl = fl[2:]
        elif fl[0] == Distance:
            new_cl.append(pc.to_image_distance(cl[0]))
            cl = cl[1:]
            fl = fl[1:]
        else:
            new_cl.append(cl[0])
            cl = cl[1:]
            fl = fl[1:]

    return new_cl




def check_wcs_and_convert(args, all_dms=False):

    is_wcs = False

    value_list = []
    for a in args:
        if isinstance(a, SimpleNumber) or isinstance(a, SimpleInteger) \
               or all_dms:
            value_list.append(a.v)
        else:
            value_list.append(a.degree)
            is_wcs = True

    return is_wcs, value_list


def check_wcs(l):
    default_coord = "physical"

    for l1, c1 in l:
        if isinstance(l1, CoordCommand):
            default_coord = l1.text.lower()
            continue
        if isinstance(l1, Shape):
            if default_coord == "galactic":
                is_wcs, coord_list = check_wcs_and_convert(l1.params,
                                                           all_dms=True)
            else:
                is_wcs, coord_list = check_wcs_and_convert(l1.params)

            if is_wcs and (default_coord == "physical"): # ciao format
                coord_format = "fk5"
            else:
                coord_format = default_coord

            l1n = copy.copy(l1)

            l1n.coord_list = coord_list
            l1n.coord_format = coord_format

            yield l1n, c1
        else:
            yield l1, c1



if __name__ == "__main__":
    fk5_to_fk4 = sky2sky(FK5, FK4)
    print fk5_to_fk4([47.37], [6.32])
    print fk5_to_fk4([47.37, 47.37], [6.32, 6.32])
    print sky2sky("fk5", "FK4")([47.37, 47.37], [6.32, 6.32])




