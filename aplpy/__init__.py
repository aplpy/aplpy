from distutils import version as v

import pyfits, pywcs

from matplotlib.pyplot import figure,NullFormatter,cm

from apl_ticks import *
from apl_grid import plot_grid
from apl_contour import draw_new_contours
from apl_header import check_header
from apl_util import *
from apl_ds9 import ds9Parser

# Values stored inside the axes Instances:

# ax.xaxis.apl_tick_spacing = x-axis tick spacing ('auto' or float)
# ax.yaxis.apl_tick_spacing = y-axis tick spacing ('auto' or float)
# ax.xaxis.apl_grid_spacing = spacing of grid in x-direction ('auto' or float)
# ax.yaxis.apl_grid_spacing = spacing of grid in y-direction ('auto' or float)
# ax.xaxis.apl_spacing_default = x-axis tick spacing chosen if above is 'auto'
# ax.yaxis.apl_spacing_default = y-axis tick spacing chosen if above is 'auto'
# ax.apl_show_grid = whether to show the grid

class FITSFigure(object):
	"A class for plotting FITS files."
	
	def __init__(self,filename,xinch=10,yinch=10,hdu=0,downsample=False):

		# Check that matplotlib is recent enough
		#if v.LooseVersion(matplotlib.__version__) < v.LooseVersion('0.98.5.2'):
		#	print "[error] matplotlib >= 0.98.5.2 is required"
		#	return
			
		# Open the figure
		self.fig = figure(figsize=(xinch,yinch))
		
		### FITS FILE ###
					
		# Read in FITS file
		try:
			self.hdu        = pyfits.open(filename)[hdu]
			self.hdu.header = check_header(self.hdu.header)
			self.wcs        = pywcs.WCS(self.hdu.header)
			self.wcs.nx = self.hdu.header['NAXIS1']
			self.wcs.ny = self.hdu.header['NAXIS2']
		except:
			print "[error] a problem occurred when reading the FITS file. Please "
			print "        check that the FITS file is valid using the online FITS"
			print "        verifier at http://fits.gsfc.nasa.gov/fits_verify.html."
			print "        If the FITS file is valid, please report this problem."
			return
		
		# Downsample if requested
		if downsample:
			self.wcs.nx = self.wcs.nx - np.mod(self.wcs.nx,downsample)
			self.wcs.ny = self.wcs.ny - np.mod(self.wcs.ny,downsample)
			self.hdu.data = self.hdu.data[0:self.wcs.ny,0:self.wcs.nx]
			self.hdu.data = resample(self.hdu.data,downsample)
		
		# set the image extent for matplotlib
		self.extent = (0.5,self.wcs.nx+0.5,0.5,self.wcs.ny+0.5)
		
		# Find generating function for vmin/vmax
		self.auto_v = percentile_function(self.hdu.data)
		
		### AXES ###
		
		# Create the two set of axes
		self.ax1 = self.fig.add_subplot(111)
		self.ax2 = twin(self.ax1)

		# Turn off autoscaling
		self.ax1.set_autoscale_on(False)
		self.ax2.set_autoscale_on(False)
		
		# Store WCS in axes
		self.ax1.apl_wcs = self.wcs
		self.ax2.apl_wcs = self.wcs
		
		# Set initial view interval
		self.reset_view()
		
		### TICKS ###

		# Set tick spacing to update if view limits are changed
		self.ax1.callbacks.connect('xlim_changed',find_default_spacing)
		self.ax2.callbacks.connect('xlim_changed',find_default_spacing)
		self.ax1.callbacks.connect('ylim_changed',find_default_spacing)
		self.ax2.callbacks.connect('ylim_changed',find_default_spacing)
		
		# Update tick spacing manually
		find_default_spacing(self.ax1)
		find_default_spacing(self.ax2)

		# Set tick spacing to default
		self.ticks(xspacing='auto',yspacing='auto',refresh=False)
		
		# Set major tick locators
		lx = WCSLocator(wcs=self.wcs,axist='x')
		self.ax1.xaxis.set_major_locator(lx)
		ly = WCSLocator(wcs=self.wcs,axist='y')
		self.ax1.yaxis.set_major_locator(ly)
		
		lxt = WCSLocator(wcs=self.wcs,axist='x',farside=True)
		self.ax2.xaxis.set_major_locator(lxt)
		lyt = WCSLocator(wcs=self.wcs,axist='y',farside=True)
		self.ax2.yaxis.set_major_locator(lyt)
		
		### LABELS ###
		
		# Set default label format
		if system(self.wcs)=='fk5':
			self.ax1.xaxis.apl_label_form = "hh:mm:ss"
			self.ax1.yaxis.apl_label_form = "dd:mm:ss"
		else:
			self.ax1.xaxis.apl_label_form = "ddd.dddd"
			self.ax1.yaxis.apl_label_form = "dd.dddd"
		
		# Set major tick formatters
		fx = WCSFormatter(wcs=self.wcs,axist='x')
		self.ax1.xaxis.set_major_formatter(fx)
		fy = WCSFormatter(wcs=self.wcs,axist='y')
		self.ax1.yaxis.set_major_formatter(fy)

		fxt = NullFormatter()
		self.ax2.xaxis.set_major_formatter(fxt)
		fyt = NullFormatter()
		self.ax2.yaxis.set_major_formatter(fyt)

		### GRID ###
		
		# Set grid defaults
		self.ax1.apl_show_grid = False
		self.ax1.xaxis.apl_grid_spacing = 'auto'
		self.ax1.yaxis.apl_grid_spacing = 'auto'
		self.ax1.callbacks.connect('xlim_changed',plot_grid)
		self.ax1.callbacks.connect('ylim_changed',plot_grid)
		
		### STYLE ###
		
		# Set default theme
		self.theme(theme='pretty',refresh=False)
		
		return
		
	def theme(self,theme='pretty',refresh=True):
		
		if theme=='pretty':
			self.frame(color='white',refresh=False)
			self.ticks(color='white',size=7,refresh=False)
			self.fig.apl_grayscale_invert_default = False
			self.fig.apl_colorscale_cmap_default  = 'jet'
			self.ax1.apl_grid_color_default  = 'white'
			self.ax1.apl_grid_alpha_default  = 0.5
		elif theme=='publication':
			self.frame(color='black',refresh=False)
			self.ticks(color='black',size=7,refresh=False)
			self.fig.apl_grayscale_invert_default = True
			self.fig.apl_colorscale_cmap_default  = 'gist_heat'
			self.ax1.apl_grid_color_default  = 'black'
			self.ax1.apl_grid_alpha_default  = 1.0
			
		if refresh:
			self.refresh()
			
	def reset_view(self):
		self.ax1.xaxis.set_view_interval(+0.5,self.wcs.nx+0.5)
		self.ax1.yaxis.set_view_interval(+0.5,self.wcs.ny+0.5)
		self.ax2.xaxis.set_view_interval(+0.5,self.wcs.nx+0.5)
		self.ax2.yaxis.set_view_interval(+0.5,self.wcs.ny+0.5)
		
	def grayscale(self,invert='unset',**kwargs):
		
		if not setpar(invert):
			invert = self.fig.apl_grayscale_invert_default
		
		if invert:
			self.colorscale(cmap='gist_yarg',**kwargs)
		else:
			self.colorscale(cmap='gray',**kwargs)
			
	def colorscale(self,stretch='linear',exponent=2,vmin = 'default',vmax = 'default',cmap='unset',interpolation='nearest',labels='auto',smooth=False):
		
		if not setpar(cmap):
			cmap = self.fig.apl_colorscale_cmap_default
		
		# The set of available functions
		g = cm.get_cmap(cmap,1000)
		stretchedImg = stretcher(self.hdu.data,stretch=stretch,exponent=exponent)
		
		vmin_auto = stretcher(self.auto_v(0.0025),stretch=stretch,exponent=exponent)
		vmax_auto = stretcher(self.auto_v(0.9975),stretch=stretch,exponent=exponent)
		
		vmin_auto,vmax_auto = vmin_auto-(vmax_auto-vmin_auto)/10.,vmax_auto+(vmax_auto-vmin_auto)/10.

		if type(vmin) is str:
			vmin=vmin_auto
			
		if type(vmax) is str:
			vmax=vmax_auto
			
		img = self.ax1.imshow(stretchedImg, cmap = g,vmin=vmin, vmax=vmax,interpolation=interpolation,origin='lower',extent=self.extent)
		
		self.ax1.set_xlabel('(R.A. J2000)')
		self.ax1.set_ylabel('(Dec. J2000)')
		
		self.refresh()
				
	def rgb(self,filename):
		pretty_image = imread(filename)
		self.ax1.imshow(pretty_image,extent=self.extent)
		
		self.ax1.set_xlabel('(R.A. J2000)')
		self.ax1.set_ylabel('(Dec. J2000)')
		
		self.refresh()
				
	def grid(self,show=True,xspacing='auto',yspacing='auto'):
		self.ax1.apl_show_grid = show
		self.ax1.xaxis.apl_grid_spacing = xspacing
		self.ax1.yaxis.apl_grid_spacing = yspacing
		self.ax1 = plot_grid(self.ax1)
		self.refresh()
		
	def contour(self,contourFile, levels=5, cmap = 'jet',filled=False,alpha=0.7):
		# Draw the contours
		g = cm.get_cmap(cmap,1000)
		hdu_contour = pyfits.open(contourFile)[0]
		hdu_contour.header  = check_header(hdu_contour.header)
		wcs_contour = pywcs.WCS(hdu_contour.header)
		image_contour = hdu_contour.data
		wcs_contour.nx = hdu_contour.header['NAXIS1']
		wcs_contour.ny = hdu_contour.header['NAXIS2']
		extent_contour = (0.5,wcs_contour.nx+0.5,0.5,wcs_contour.ny+0.5)
		if filled:
			self.ax1.contourf(image_contour,levels,cmap=g,alpha=alpha,extent=extent_contour)
		else:
			self.ax1.contour(image_contour,levels,cmap=g,alpha=alpha,extent=extent_contour)
		self.ax1 = draw_new_contours(self.ax1,wcs_contour,self.wcs)
		self.refresh()

	def frame(self,refresh=True,**kwargs):
		
		if kwargs.has_key('color'):
			self.ax1.frame.set_edgecolor(kwargs['color'])
		
		if refresh: self.refresh()

	def labels(self,refresh=True,**kwargs):
		
		if kwargs.has_key('xform'):
			self.ax1.xaxis.apl_label_form = kwargs['xform']

		if kwargs.has_key('yform'):
			self.ax1.yaxis.apl_label_form = kwargs['yform']

		if refresh: self.refresh()

	def ticks(self,refresh=True,**kwargs):

		if kwargs.has_key('xspacing'):
			self.ax1.xaxis.apl_tick_spacing = kwargs['xspacing']
			self.ax2.xaxis.apl_tick_spacing = kwargs['xspacing']
			
		if kwargs.has_key('yspacing'):
			self.ax1.yaxis.apl_tick_spacing = kwargs['yspacing']
			self.ax2.yaxis.apl_tick_spacing = kwargs['yspacing']

		if kwargs.has_key('color'):
			for line in self.ax1.xaxis.get_ticklines():
				line.set_color(kwargs['color'])
			for line in self.ax1.yaxis.get_ticklines():
				line.set_color(kwargs['color'])
			for line in self.ax2.xaxis.get_ticklines():
				line.set_color(kwargs['color'])
			for line in self.ax2.yaxis.get_ticklines():
				line.set_color(kwargs['color'])
				
		if kwargs.has_key('size'):
			for line in self.ax1.xaxis.get_ticklines():
				line.set_markersize(kwargs['size'])
			for line in self.ax1.yaxis.get_ticklines():
				line.set_markersize(kwargs['size'])
			for line in self.ax2.xaxis.get_ticklines():
				line.set_markersize(kwargs['size'])
			for line in self.ax2.yaxis.get_ticklines():
				line.set_markersize(kwargs['size'])
				
		if refresh: self.refresh()
	
	# This method plots markers. The input should be an Nx2 array with WCS coordinates
	# in degree format.
		
	def markers(self,wcsArray,alpha=1 ,color='r' ,marker='o' , edgecolor='red', size=30, linewidth=1,facecolors='none'):
		wcsArray = self.wcs.wcs_sky2pix_fits(wcsArray)
		self.ax1.scatter(wcsArray[:,0], wcsArray[:,1],alpha=alpha, c=color,marker=marker, s=size,edgecolor=edgecolor,linewidth=linewidth, facecolors=facecolors)
		self.refresh()
		
	def refresh(self):
		self.fig.canvas.draw()
		
	def world2pix(self,x_world,y_world):
		if type(x_world) == float:
			x_pix,y_pix = self.wcs.wcs_sky2pix_fits(np.array([x_world]),np.array([y_world]))
			return x_pix[0],y_pix[0]
		elif type(x_world) == list:
			x_pix,y_pix = self.wcs.wcs_sky2pix_fits(np.array(x_world),np.array(y_world))
			return x_pix.tolist(),y_pix.tolist()
		elif type(x_world) == np.ndarray:
			return self.wcs.wcs_sky2pix_fits(x_world,y_world)
		else:
			print "[error] world2pix should be provided either with two floats, two lists, or two numpy arrays"
			
	def pix2world(self,x_pix,y_pix):
		if type(x_pix) == float:
			x_world,y_world = self.wcs.wcs_pix2sky_fits(np.array([x_pix]),np.array([y_pix]))
			return x_world[0],y_world[0]
		elif type(x_pix) == list:
			x_world,y_world = self.wcs.wcs_pix2sky_fits(np.array(x_pix),np.array(y_pix))
			return x_world.tolist(),y_world.tolist()
		elif type(x_pix) == np.ndarray:
			return self.wcs.wcs_pix2sky_fits(x_pix,y_pix)
		else:
			print "[error] pix2world should be provided either with two floats, two lists, or two numpy arrays"
			
	def save(self,saveName,dpi = 300):
		self.fig.savefig(saveName,dpi=dpi)
		
	def ds9(self,regionfile):
		reg = ds9Parser(regionfile,self.wcs)
		for p in reg.plot():
			self.ax1.add_patch(p)
		self.refresh()
		
