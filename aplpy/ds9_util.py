import string
from matplotlib.pyplot import *
from numpy import array, radians, cos, sin

import wcs_util

def string_cleaner(string):
    
    dirt = ('(', ')', '{', '}', '=', '#', ', ')
    tmp = range(len(string))
    
    for i in range(len(string)):
        tmp[i] =  string[i]
    
    string = tmp[:]
    
    for j in range(len(string)):
        for k in dirt:
            if string[j] is k:
                string[j] = ' '
            else:
                pass
    
    string = string.join(string, '')
    
    string = string.replace('"', '')
    string = string.replace('    ', ' ')
    string = string.replace('   ', ' ')
    string = string.replace('  ', ' ')
    string = string.split(' ')
    return string

"""
def string_find(List, String):
    ctmp = []
    for k in range(len(List)):
        if List[k] is String:
            ctmp.append(k)
    return ctmp
"""

def string_find(List, st):
    ctmp = []
    for k in range(len(List)):
        if List[k] is st:
            return k

def circle_patch(x, y, radius, **kwargs):
    return Circle((x, y), radius=radius, alpha=0.80, fill=False, edgecolor=kwargs['edgecolor'], lw=kwargs['lw'], ls=kwargs['ls'])

def ellipse_patch(x, y, width, height, angle, **kwargs):
    return Ellipse((x, y), width, height, angle=angle, alpha=0.80, fill=False, edgecolor=kwargs['edgecolor'], lw=kwargs['lw'], ls=kwargs['ls'])

def box_patch(x, y, width, height, angle, **kwargs):
    v = []
    v.append(rotate((x-width/2., y-height/2.), (x, y), angle))
    v.append(rotate((x+width/2., y-height/2.), (x, y), angle))
    v.append(rotate((x+width/2., y+height/2.), (x, y), angle))
    v.append(rotate((x-width/2., y+height/2.), (x, y), angle))
    return Polygon(v, closed=True, alpha=0.80, fill=False, edgecolor=kwargs['edgecolor'], lw=kwargs['lw'], ls=kwargs['ls'])

def line_patch(x, y, **kwargs):
    return Polygon([(x[0], y[0]), (x[1], y[1])], closed=False, alpha=0.80, fill=False, edgecolor=kwargs['edgecolor'], lw=kwargs['lw'], ls=kwargs['ls'])

def rotate(position, position0, theta):
    x = position[0]
    y = position[1]
    x0 = position0[0]
    y0 = position0[1]
    theta = radians(theta)
    xnew = cos(theta)*(x-x0) - sin(theta)*(y-y0)+x0
    ynew = sin(theta)*(x-x0) + cos(theta)*(y-y0)+y0
    return xnew, ynew

def dict2pix(dict, wcs):
    
    xw = dict['x']
    yw = dict['y']
    
    t = type(xw)
    
    if t==float:
        xw = array([xw])
        yw = array([yw])
    
    if t==list:
        xw = array(xw)
        yw = array(yw)
    
    if dict['coord_sys']=='fk5':
        if wcs_util.system(wcs)=='fk5':
            xpix, ypix = world2pix(wcs, xw, yw)
        else:
            sys.exit("Unimplemented")
    else:
        sys.exit("Unimplemented")
    
    if t==float:
        dict['x'] = xpix[0]
        dict['y'] = ypix[0]
    elif t==list:
        dict['x'] = xpix.tolist()
        dict['y'] = ypix.tolist()
    
    arc2pix = arcperpix(wcs)
    
    if dict.has_key('width'):
        dict['width'] = dict['width'] * arc2pix
    if dict.has_key('height'):
        dict['height'] = dict['height'] * arc2pix
    if dict.has_key('radius'):
        dict['radius'] = dict['radius'] * arc2pix
    
    dict['coord_sys'] = 'pix'
    
    return dict