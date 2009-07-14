# from matplotlib.pyplot import Circle
from matplotlib.patches import Ellipse, Rectangle, Circle
from matplotlib.collections import PatchCollection
import wcs_util


def make_circles(xp,yp,rp,**kwargs):
    patches = []
    for i in range(len(xp)):
        patches.append(Circle((xp[i],yp[i]),radius=rp[i],**kwargs))
    return PatchCollection(patches,match_original=True)

def make_ellipses(xp,yp,width,height,**kwargs):
    patches = []
    for i in range(len(xp)):
        patches.append(Ellipse((xp[i],yp[i]),width=width[i],height=height[i],**kwargs))
    return PatchCollection(patches,match_original=True)

def make_rectangles(xp,yp,width,height,**kwargs):
    patches = []
    xp = xp - width/2.
    yp = yp - height/2.
    for i in range(len(xp)):
        patches.append(Rectangle((xp[i],yp[i]),width=width[i],height=height[i],**kwargs))
    return PatchCollection(patches,match_original=True)

def make_polygon(xp,yp,**kwargs):
    pass

