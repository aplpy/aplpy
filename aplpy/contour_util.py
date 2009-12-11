import wcs_util
from matplotlib.path import Path
import numpy as np

def transform(contours, wcs_in, wcs_out, filled=False):

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

            if filled:
                polygons_out.append(Path(np.array(zip(xp_out, yp_out)),codes=polygon.codes))
            else:
                polygons_out.append(zip(xp_out, yp_out))

        if filled:
            contour.set_paths(polygons_out)
        else:
            contour.set_verts(polygons_out)

        contour.apl_converted = True
