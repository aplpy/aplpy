import numpy as np
from matplotlib.pyplot import Locator
from scipy.interpolate import UnivariateSpline
import sys
from util import *
from wcs_util import *

class Ticks(object):
    
    def _initialize_ticks(self):
        
        # Set tick positions
        self._ax1.yaxis.tick_left()
        self._ax1.xaxis.tick_bottom()
        self._ax2.yaxis.tick_right()
        self._ax2.xaxis.tick_top()
        
        # Initialize default tick spacing
        find_default_spacing(self._ax1)
        find_default_spacing(self._ax2)
        
        # Set tick spacing to default
        self.set_tick_spacing(xspacing='auto',yspacing='auto',refresh=False)
        
        # Set major tick locators
        lx = WCSLocator(wcs=self._wcs,axist='x')
        self._ax1.xaxis.set_major_locator(lx)
        ly = WCSLocator(wcs=self._wcs,axist='y')
        self._ax1.yaxis.set_major_locator(ly)
        
        lxt = WCSLocator(wcs=self._wcs,axist='x',farside=True)
        self._ax2.xaxis.set_major_locator(lxt)
        lyt = WCSLocator(wcs=self._wcs,axist='y',farside=True)
        self._ax2.yaxis.set_major_locator(lyt)
        
        # Set tick event handler
        self._ax1.callbacks.connect('xlim_changed',find_default_spacing)
        self._ax2.callbacks.connect('xlim_changed',find_default_spacing)
        self._ax1.callbacks.connect('ylim_changed',find_default_spacing)
        self._ax2.callbacks.connect('ylim_changed',find_default_spacing)
    
    def set_tick_spacing(self,xspacing='auto',yspacing='auto',refresh=True):
        
        self._ax1.xaxis.apl_tick_spacing = xspacing
        self._ax2.xaxis.apl_tick_spacing = xspacing
        self._ax1.yaxis.apl_tick_spacing = yspacing
        self._ax2.yaxis.apl_tick_spacing = yspacing
        
        if refresh: self.refresh()
    
    def set_tick_color(self,color,refresh=True):
        
        for line in self._ax1.xaxis.get_ticklines():
            line.set_color(color)
        for line in self._ax1.yaxis.get_ticklines():
            line.set_color(color)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_color(color)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_color(color)
        
        if refresh: self.refresh()
    
    def set_tick_size(self,size,refresh=True):
        
        for line in self._ax1.xaxis.get_ticklines():
            line.set_markersize(size)
        for line in self._ax1.yaxis.get_ticklines():
            line.set_markersize(size)
        for line in self._ax2.xaxis.get_ticklines():
            line.set_markersize(size)
        for line in self._ax2.yaxis.get_ticklines():
            line.set_markersize(size)
        
        if refresh: self.refresh()

class WCSLocator(Locator):
    
    def __init__(self, presets=None,wcs=False,axist='x',farside=False,minor=False):
        if presets is None:
            self.presets = {}
        else:
            self.presets = presets
        self._wcs = wcs
        self.axist = axist
        self.farside = farside
        self.minor = minor
    
    def __call__(self):
        
        ymin, ymax = self.axis.get_axes().yaxis.get_view_interval()
        xmin, xmax = self.axis.get_axes().xaxis.get_view_interval()
        
        if self.axis.apl_tick_spacing == 'auto':
            spacing = self.axis.apl_spacing_default
        else:
            spacing = self.axis.apl_tick_spacing
        
        px,py,wx,wy = tick_positions(self._wcs,spacing,self.axist,self.axist,farside=self.farside,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
        
        if self.axist=='x':
            return px
        else:
            return py

def find_default_spacing(ax):
    
    wcs = ax.apl_wcs
    
    xmin, xmax = ax.xaxis.get_view_interval()
    ymin, ymax = ax.yaxis.get_view_interval()
    
    px,py,wx,wy = axis_positions(wcs,'x',False,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
    wxmin,wxmax = smart_range(wx)
    ax.xaxis.apl_spacing_default = smart_round_x((wxmax-wxmin)/5.)
    
    px,py,wx,wy = axis_positions(wcs,'y',False,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
    wymin,wymax = min(wy),max(wy)
    ax.yaxis.apl_spacing_default = smart_round_y((wymax-wymin)/5.)

###############################################################
# find_ticks:      Find positions of ticks along a given axis
#                  axes. This function takes one argument:
#
#             wcs: wcs header of FITS file (pywcs class)
#
#                  the function returns:
#     x_min,x_max: range of x values along all axes
#     y_min,y_max: range of y values along all axes
###############################################################

def tick_positions(wcs,spacing,axis,coord,farside=False,xmin=False,xmax=False,ymin=False,ymax=False):
    
    (px,py,wx,wy) = axis_positions(wcs,axis,farside,xmin,xmax,ymin,ymax)
    
    if coord=='y':
        wx,wy = wy,wx
    
    # Check for 360 degree transition, and if encountered,
    # change the values so that there is continuity
    
    for i in range(0,len(wx)-1):
        if(abs(wx[i]-wx[i+1])>180.):
            if(wx[i] > wx[i+1]):
                 wx[i+1:] = wx[i+1:] + 360.
            else:
                 wx[i+1:] = wx[i+1:] - 360.
    
    # Convert wx to units of the spacing, then ticks are at integer values
    wx = wx / spacing
    
    # Create empty arrays for tick positions
    px_out = []
    py_out = []
    wx_out = []
    wy_out = []
    
    for w in np.arange(np.floor(min(wx)),np.ceil(max(wx)),1.):
        for i in range(len(px)-1):
            if (wx[i] <= w and wx[i+1] > w) or (wx[i] > w and wx[i+1] <= w):
                px_out.append(px[i] + (px[i+1]-px[i]) * (w - wx[i]) / (wx[i+1]-wx[i]))
                py_out.append(py[i] + (py[i+1]-py[i]) * (w - wx[i]) / (wx[i+1]-wx[i]))
                wx_tick = w*spacing % 360.
                wy_tick = (wy[i] + (wy[i+1]-wy[i]) * (w - wx[i]) / (wx[i+1]-wx[i])) % 360
                wx_out.append(wx_tick)
                wy_out.append(wy_tick)
    
    if coord=='y':
        wx_out,wy_out = wy_out,wx_out
    
    for i in range(0,np.size(wy_out)):
        if wy_out[i] > 90.:
            wy_out[i] = wy_out[i] - 360.
    
    return px_out,py_out,wx_out,wy_out

###############################################################
# axis_positions:  pixel and world positions of all pixels
#                  along a given axis. This function takes
#                  three arguments:
#
#             wcs: wcs header of FITS file (pywcs class)
#            axis: x or y axis
#         farside: if true, use top instead of bottom
#                  axis, or right instead of left.
#
#                  the function returns:
#     x_pix,y_pix: pixel coordinates of pixels along axis
# x_world,y_world: world coordinates of pixels along axis
###############################################################

def axis_positions(wcs,axis,farside,xmin=False,xmax=False,ymin=False,ymax=False):
    
    if not xmin: xmin = 0.5
    if not xmax: xmax = 0.5+wcs.naxis1
    if not ymin: ymin = 0.5
    if not ymax: ymax = 0.5+wcs.naxis2
    
    # Check options
    assert axis=='x' or axis=='y',"The axis= argument should be set to x or y"
    
    # Generate an array of pixel values for the x-axis
    if axis=='x':
        x_pix = np.arange(xmin,xmax)
        y_pix = np.ones(np.shape(x_pix))
        if(farside):
            y_pix = y_pix * ymax
        else:
            y_pix = y_pix * ymin
    else:
        y_pix = np.arange(ymin,ymax)
        x_pix = np.ones(np.shape(y_pix))
        if(farside):
            x_pix = x_pix * xmax
        else:
            x_pix = x_pix * xmin
    
    # Convert these to world coordinates
    x_world,y_world = pix2world(wcs,x_pix,y_pix)
    
    return x_pix,y_pix,x_world,y_world

###############################################################
# coord_range:     Range of coordinates that intersect the
#                  axes. This function takes one argument:
#
#             wcs: wcs header of FITS file (pywcs class)
#
#                  the function returns:
#     x_min,x_max: range of x values along all axes
#     y_min,y_max: range of y values along all axes
###############################################################

def coord_range(wcs):
    
    x_pix,y_pix,x_world_1,y_world_1 = axis_positions(wcs,'x',farside=False)
    x_pix,y_pix,x_world_2,y_world_2 = axis_positions(wcs,'x',farside=True)
    x_pix,y_pix,x_world_3,y_world_3 = axis_positions(wcs,'y',farside=False)
    x_pix,y_pix,x_world_4,y_world_4 = axis_positions(wcs,'y',farside=True)
    
    x_world = np.hstack([x_world_1,x_world_2,x_world_3,x_world_4])
    y_world = np.hstack([y_world_1,y_world_2,y_world_3,y_world_4])
    
    x_min = min(x_world)
    x_max = max(x_world)
    y_min = min(y_world)
    y_max = max(y_world)
    
    return x_min,x_max,y_min,y_max
    