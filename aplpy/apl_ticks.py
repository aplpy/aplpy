import numpy as np
from matplotlib.pyplot import Locator,Formatter
import degConvert as dc
from scipy.interpolate import UnivariateSpline
import sys
from apl_util import *

class WCSLocator(Locator):
	
	def __init__(self, presets=None,wcs=False,axist='x',farside=False,minor=False):
		if presets is None:
			self.presets = {}
		else:
			self.presets = presets
		self.wcs = wcs
		self.axist = axist
		self.farside = farside
		self.minor = minor
		
	def __call__(self):
		
#		print "[Locator]"

		ymin, ymax = self.axis.get_axes().yaxis.get_view_interval()
		xmin, xmax = self.axis.get_axes().xaxis.get_view_interval()
		
		if self.axis.apl_tick_spacing == 'auto':
			spacing = self.axis.apl_spacing_default
		else:
			spacing = self.axis.apl_tick_spacing
			
		px,py,wx,wy = tick_positions(self.wcs,spacing,self.axist,self.axist,farside=self.farside,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
			
		if self.axist=='x':
			return px
		else:
			return py
			
def find_default_spacing(ax):

#	print "[find_default_spacing]"

	wcs = ax.apl_wcs
	
	xmin, xmax = ax.xaxis.get_view_interval()
	ymin, ymax = ax.yaxis.get_view_interval()
	
	px,py,wx,wy = axis_positions(wcs,'x',False,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
	wxmin,wxmax = smart_range(wx)
	ax.xaxis.apl_spacing_default = smart_round_x((wxmax-wxmin)/5.)

	px,py,wx,wy = axis_positions(wcs,'y',False,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)
	wymin,wymax = min(wy),max(wy)
	ax.yaxis.apl_spacing_default = smart_round_y((wymax-wymin)/5.)
			
class WCSFormatter(Formatter):
	
	def __init__(self, wcs=False,axist='x'):
		self.wcs = wcs
		self.axist = axist
	
	def __call__(self,x,pos=None):
		'Return the format for tick val x at position pos; pos=None indicated unspecified'
		
#		print "[Formatter]"
		
		ymin, ymax = self.axis.get_axes().yaxis.get_view_interval()
		xmin, xmax = self.axis.get_axes().xaxis.get_view_interval()
		
		if self.axist=='x':
			y = ymin
			x = x
		else:
			y = x
			x = xmin
			
		xw,yw = self.wcs.wcs_pix2sky(np.array([x]),np.array([y]))
		
		if self.axist=='x':
			if xw[0]==360.0: xw[0]=0.0
			return dc.raer(xw[0],form=self.axis.apl_label_form)
		else:
			return dc.decer(yw[0],form=self.axis.apl_label_form)

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
	if not xmax: xmax = 0.5+wcs.nx
	if not ymin: ymin = 0.5
	if not ymax: ymax = 0.5+wcs.ny
		
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
	(x_world,y_world) = wcs.wcs_pix2sky(x_pix,y_pix)

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
	