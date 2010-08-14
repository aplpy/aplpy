import copy
import matplotlib.patches as mpatches
from matplotlib.text import Text
from matplotlib.path import Path
from matplotlib.lines import Line2D
from matplotlib.transforms import Affine2D, Bbox, IdentityTransform

from matplotlib.text import Annotation

import numpy as np
from math import cos, sin, pi, atan2

def rotated_polygon(xy, ox, oy, angle):
    # angle in degree
    theta = angle/180.*pi

    st = sin(theta)
    ct = cos(theta)

    xy = np.asarray(xy, dtype="d")
    x, y = xy[:,0], xy[:,1]
    x1 = x - ox
    y1 = y - oy

    x2 =  ct*x1 + -st*y1
    y2 =  st*x1 +  ct*y1

    xp = x2 + ox
    yp = y2 + oy

    return np.hstack((xp.reshape((-1,1)), yp.reshape((-1,1))))

    # sss3 = [s1[0] for s1 in sss2 if isinstance(s1[0], parser_ds9.Shape)]

_point_type_dict=dict(circle="o",
                      box="s",
                      diamond="D",
                      x="x",
                      cross="+",
                      arrow="^",
                      boxcircle="*")

_ds9_to_mpl_colormap = dict(green="lime",
                            )

def properties_func_default(shape, saved_attrs):

    attr_list = copy.copy(shape.attr[0])
    attr_dict = copy.copy(shape.attr[1])

    attr_list.extend(saved_attrs[0])
    attr_dict.update(saved_attrs[1])

    color = attr_dict.get("color", None)
    color = _ds9_to_mpl_colormap.get(color, color)

    if shape.name ==  "text":
        kwargs = dict(color=color,
                      rotation=attr_dict.get("textangle", 0),
                      )
        font = attr_dict.get("font")
        if font:
            a = font.split()
            if len(a) == 3:
                fontsize=float(a[1])
            kwargs["fontsize"]=fontsize
    elif shape.name == "point":
        marker = _point_type_dict.get(attr_dict.get("point"), "o")
        kwargs = dict(markeredgecolor=color,
                      markerfacecolor="none",
                      marker=marker,
                      markersize=int(attr_dict.get("size", 6)),
                      markeredgewidth=int(attr_dict.get("width", 1)),
                      )
    elif shape.name in ["line", "vector"]:
        font = attr_dict.get("font")
        if font:
            fontsize = int(font.split()[1])
        else:
            fontsize = 10

        kwargs = dict(color=color,
                      linewidth=int(attr_dict.get("width", 1)),
                      mutation_scale=fontsize,
                      )
        if int(attr_dict.get("dash","0")):
            kwargs["linestyle"] = "dashed"

    else:
        kwargs = dict(edgecolor=color,
                      linewidth=int(attr_dict.get("width", 1)),
                      facecolor="none"
                      )

        if "background" in attr_list:
            kwargs["linestyle"] = "dashed"

        if int(attr_dict.get("dash","0")):
            kwargs["linestyle"] = "dashed"
        if shape.exclude:
            kwargs["hatch"] = "/"

    return kwargs


def _get_text(txt, x, y, dx, dy, ha="center", va="center", **kwargs):
    if "color" in kwargs:
        textcolor = kwargs["color"]
    elif "markeredgecolor" in kwargs:
        textcolor = kwargs["markeredgecolor"]
    ann = Annotation(txt, (x, y), xytext=(dx, dy),
                     xycoords='data',
                     textcoords="offset points",
                     ha=ha, va=va,
                     **kwargs)
    ann.set_transform(IdentityTransform())

    return ann


def as_mpl_artists(shape_list,
                   properties_func=None,
                   text_offset=5.0):
    """
    Converts a region list to a list of patches and a list of artists.


    Optional Keywords:
    [ text_offset ] - If there is text associated with the regions, add
    some vertical offset (in pixels) to the text so that it doesn't overlap
    with the regions.
    """

    patch_list = []
    artist_list = []

    if properties_func is None:
        properties_func = properties_func_default

    # properties for continued(? multiline?) regions
    saved_attrs = None

    for shape in shape_list:

        patches = []

        if saved_attrs is None:
            _attrs = [], {}
        else:
            _attrs = copy.copy(saved_attrs[0]), copy.copy(saved_attrs[1])

        kwargs = properties_func(shape, _attrs)

        if shape.name == "composite":
            saved_attrs = shape.attr
            continue

        if saved_attrs is None and shape.continued:
            saved_attrs = shape.attr
#         elif (shape.name in shape.attr[1]):
#             if (shape.attr[1][shape.name] != "ignore"):
#                 saved_attrs = shape.attr

        if not shape.continued:
            saved_attrs = None

        # text associated with the shape
        txt = shape.attr[1].get("text","")


        if shape.name == "polygon":
            xy = np.array(shape.coord_list)
            xy.shape = -1,2

            # -1 for change origin to 0,0
            patches=[mpatches.Polygon(xy-1, closed=True, **kwargs)]

        elif shape.name == "rotbox" or shape.name == "box":
            xc, yc, w, h, rot = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1
            _box = np.array([[-w/2., -h/2.],
                             [-w/2., h/2.],
                             [w/2., h/2.],
                             [w/2., -h/2.]])
            box = _box + [xc, yc]
            rotbox = rotated_polygon(box, xc, yc, rot)
            patches = [mpatches.Polygon(rotbox, closed=True, **kwargs)]


        elif shape.name == "ellipse":
            xc, yc  = shape.coord_list[:2]
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1
            angle = shape.coord_list[-1]

            maj_list, min_list = shape.coord_list[2:-1:2], shape.coord_list[3:-1:2]

            patches = [mpatches.Ellipse((xc, yc), 2*maj, 2*min,
                                        angle=angle, **kwargs) \
                       for maj, min in zip(maj_list, min_list)]


        elif shape.name == "annulus":
            xc, yc  = shape.coord_list[:2]
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1
            r_list = shape.coord_list[2:]

            patches = [mpatches.Ellipse((xc, yc), 2*r, 2*r,
                                        **kwargs) \
                       for r in r_list]


        elif shape.name == "circle":
            xc, yc, major = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1
            patches = [mpatches.Ellipse((xc, yc), 2*major, 2*major,
                                        angle=0, **kwargs)]

        elif shape.name == "panda":
            xc, yc, a1, a2, an, r1, r2, rn = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1
            patches = [mpatches.Arc((xc, yc), rr*2, rr*2, angle=0,
                                    theta1=a1, theta2=a2, **kwargs) \
                       for rr in np.linspace(r1, r2, rn+1)]

            for aa in np.linspace(a1, a2, an+1):
                xx = np.array([r1, r2]) * np.cos(aa/180.*np.pi) + xc
                yy = np.array([r1, r2]) * np.sin(aa/180.*np.pi) + yc
                p = Path(np.transpose([xx,yy]))
                patches.append(mpatches.PathPatch(p, **kwargs))


        elif shape.name == "pie":
            xc, yc, r1, r2, a1, a2 = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1

            patches = [mpatches.Arc((xc, yc), rr*2, rr*2, angle=0,
                                   theta1=a1, theta2=a2, **kwargs) \
                       for rr in [r1, r2]]

            for aa in [a1, a2]:
                xx = np.array([r1, r2]) * np.cos(aa/180.*np.pi) + xc
                yy = np.array([r1, r2]) * np.sin(aa/180.*np.pi) + yc
                p = Path(np.transpose([xx,yy]))
                patches.append(mpatches.PathPatch(p, **kwargs))


        elif shape.name == "epanda":
            xc, yc, a1, a2, an, r11, r12,r21, r22, rn, angle = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1

            # mpl takes angle a1, a2 as angle as in circle before
            # transformation to ellipse.

            x1, y1 = cos(a1/180.*pi), sin(a1/180.*pi)*r11/r12
            x2, y2 = cos(a2/180.*pi), sin(a2/180.*pi)*r11/r12

            a1, a2 = atan2(y1, x1)/pi*180., atan2(y2, x2)/pi*180.

            patches = [mpatches.Arc((xc, yc), rr1*2, rr2*2,
                                    angle=angle, theta1=a1, theta2=a2,
                                  **kwargs) \
                       for rr1, rr2 in zip(np.linspace(r11, r21, rn+1),
                                           np.linspace(r12, r22, rn+1))]

            for aa in np.linspace(a1, a2, an+1):
                xx = np.array([r11, r21]) * np.cos(aa/180.*np.pi)
                yy = np.array([r11, r21]) * np.sin(aa/180.*np.pi)
                p = Path(np.transpose([xx,yy]))
                tr = Affine2D().scale(1, r12/r11).rotate_deg(angle).translate(xc, yc)
                p2 = tr.transform_path(p)
                patches.append(mpatches.PathPatch(p2, **kwargs))

        elif shape.name == "text":
            xc, yc  = shape.coord_list[:2]
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1

            if txt:
                _t = _get_text(txt, xc, yc, 0, 0, **kwargs)
                artist_list.append(_t)

        elif shape.name == "point":
            xc, yc  = shape.coord_list[:2]
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1
            artist_list.append(Line2D([xc], [yc],
                                      **kwargs))

            if txt:
                textshape = copy.copy(shape)
                textshape.name = "text"
                textkwargs = properties_func(textshape, _attrs)
                _t = _get_text(txt, xc, yc, 0, text_offset,
                               va="bottom",
                               **textkwargs)
                artist_list.append(_t)

        elif shape.name in ["line", "vector"]:
            if shape.name == "line":
                x1, y1, x2, y2  = shape.coord_list[:4]
                # -1 for change origin to 0,0
                x1, y1, x2, y2 = x1-1, y1-1, x2-1, y2-1

                a1, a2 = shape.attr[1].get("line", "0 0").strip().split()[:2]

                arrowstyle = "-"
                if int(a1):
                    arrowstyle = "<" + arrowstyle
                if int(a2):
                    arrowstyle = arrowstyle + ">"

            else: # shape.name == "vector"
                x1, y1, l, a  = shape.coord_list[:4]
                # -1 for change origin to 0,0
                x1, y1 = x1-1, y1-1
                x2, y2 = x1 + l * np.cos(a/180.*np.pi), y1 + l * np.sin(a/180.*np.pi)
                v1 = int(shape.attr[1].get("vector", "0").strip())

                if v1:
                    arrowstyle="->"
                else:
                    arrowstyle="-"

            patches = [mpatches.FancyArrowPatch(posA=(x1, y1),
                                                posB=(x2, y2),
                                                arrowstyle=arrowstyle,
                                                arrow_transmuter=None,
                                                connectionstyle="arc3",
                                                patchA=None, patchB=None,
                                                shrinkA=0, shrinkB=0,
                                                connector=None,
                                                **kwargs)]

        else:
            print "'as_mpl_artists' does not know how to convert '%s' to mpl artist" % (shape.name,)


        patch_list.extend(patches)

        if txt and patches:
            # the text associated with a shape uses different
            # matplotlib keywords than the shape itself for, e.g.,
            # color
            textshape = copy.copy(shape)
            textshape.name = "text"
            textkwargs = properties_func(textshape, _attrs)

            # calculate the text position
            _bb = [p.get_window_extent() for p in patches]
            _bbox = Bbox.union(_bb)
            x0, y0, x1, y1 = _bbox.extents
            xc = .5*(x0+x1)

            _t = _get_text(txt, xc, y1, 0, text_offset,
                           va="bottom",
                           **textkwargs)
            artist_list.append(_t)

    return patch_list, artist_list


if 0:
    import parser_ds9
    regname = "az_region.reg"
    shape_list = region_read_as_imagecoord(regname, wcs)
    p = as_mpl_patches(shape_list)

    clf()
    ax = gca()
    [ax.add_patch(p1) for p1 in p]
    xlim(0,1500)
    ylim(0,1500)

    draw()

