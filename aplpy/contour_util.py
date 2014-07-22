from __future__ import absolute_import, print_function, division

import numpy as np
from matplotlib.path import Path

from . import wcs_util


def transform(contours, wcs_in, wcs_out, filled=False, overlap=False):

    system_in, equinox_in, units_in = wcs_util.system(wcs_in)
    system_out, equinox_out, units_out = wcs_util.system(wcs_out)

    for contour in contours.collections:

        polygons_out = []
        for polygon in contour.get_paths():

            xp_in = polygon.vertices[:, 0]
            yp_in = polygon.vertices[:, 1]

            xw, yw = wcs_util.pix2world(wcs_in, xp_in, yp_in)

            xw, yw = wcs_util.convert_coords(xw, yw,
                input=(system_in, equinox_in),
                output=(system_out, equinox_out))

            xp_out, yp_out = wcs_util.world2pix(wcs_out, xw, yw)

            if overlap:
                if np.all(xp_out < 0) or np.all(yp_out < 0) or \
                   np.all(xp_out > wcs_out.nx) or np.all(yp_out > wcs_out.ny):
                    continue

            if filled:
                polygons_out.append(Path(np.array(list(zip(xp_out, yp_out))), codes=polygon.codes))
            else:
                polygons_out.append(list(zip(xp_out, yp_out)))

        if filled:
            contour.set_paths(polygons_out)
        else:
            contour.set_verts(polygons_out)

        contour.apl_converted = True
