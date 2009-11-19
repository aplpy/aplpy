import numpy as np
import _region_filter as region_filter

def as_region_filter(shape_list):
    filter_list = []
    for shape in shape_list:

        if shape.name == "composite":
            continue

        if shape.name == "polygon":
            xy = np.array(shape.coord_list) - 1
            f = region_filter.Polygon(xy[::2], xy[1::2])

        elif shape.name == "rotbox" or shape.name == "box":
            xc, yc, w, h, rot = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1

            f = region_filter.Rotated(region_filter.Box(xc, yc, w, h),
                                      rot, xc, yc)

        elif shape.name == "ellipse":
            xc, yc  = shape.coord_list[:2]
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1
            angle = shape.coord_list[-1]

            maj_list, min_list = shape.coord_list[2:-1:2], shape.coord_list[3:-1:2]

            if len(maj_list) > 1:
                w1, h1 = max(maj_list), max(min_list)
                w2, h2 = min(maj_list), min(min_list)

                f1 = region_filter.Ellipse(xc, yc, w1, h1) \
                    & ~region_filter.Ellipse(xc, yc, w2, h2)
                f = region_filter.Rotated(f1, angle, xc, yc)
            else:
                w, h = maj_list[0], min_list[0]
                f = region_filter.Rotated(region_filter.Ellipse(xc, yc, w, h),
                                          angle, xc, yc)



        elif shape.name == "annulus":
            xc, yc  = shape.coord_list[:2]
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1
            r_list = shape.coord_list[2:]

            r1 = max(r_list)
            r2 = min(r_list)

            f = region_filter.Circle(xc, yc, r1) & ~region_filter.Circle(xc, yc, r2)

        elif shape.name == "circle":
            xc, yc, r = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1

            f = region_filter.Circle(xc, yc, r)

        elif shape.name == "panda":
            xc, yc, a1, a2, an, r1, r2, rn = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1

            f1 = region_filter.Circle(xc, yc, r2) & ~region_filter.Circle(xc, yc, r1)
            f = f1 & region_filter.AngleRange(xc, yc, a1, a2)

        elif shape.name == "pie":
            xc, yc, r1, r2, a1, a2 = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1

            f1 = region_filter.Circle(xc, yc, r2) & ~region_filter.Circle(xc, yc, r1)
            f = f1 & region_filter.AngleRange(xc, yc, a1, a2)

        elif shape.name == "epanda":
            xc, yc, a1, a2, an, r11, r12, r21, r22, rn, angle = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1

            f1 = region_filter.Ellipse(xc, yc, r21, r22) & ~region_filter.Ellipse(xc, yc, r11, r12)
            f2 = f1 & region_filter.AngleRange(xc, yc, a1, a2)
            f = region_filter.Rotated(f2, angle, xc, yc)
            #f = f2 & region_filter.AngleRange(xc, yc, a1, a2)

        elif shape.name == "bpanda":
            xc, yc, a1, a2, an, r11, r12, r21, r22, rn, angle = shape.coord_list
            # -1 for change origin to 0,0
            xc, yc = xc-1, yc-1

            f1 = region_filter.Box(xc, yc, r21, r22) & ~region_filter.Box(xc, yc, r11, r12)
            f2 = f1 & region_filter.AngleRange(xc, yc, a1, a2)
            f = region_filter.Rotated(f2, angle, xc, yc)
            #f = f2 & region_filter.AngleRange(xc, yc, a1, a2)

        else:
            print "'as_region_filter' does not know how to convert '%s' to mpl artist" % (shape.name,)
            continue

        if shape.exclude:
            filter_list = [region_filter.RegionOrList(*filter_list) & ~f]
        else:
            filter_list.append(f)


    return region_filter.RegionOrList(*filter_list)


