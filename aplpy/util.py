import numpy as np
from numpy import log10, sqrt, arcsinh, power
from scipy.interpolate import interp1d
import scipy.ndimage as i

def resample(array,factor):
	nx,ny = np.shape(array)
	nx_new = nx / factor
	ny_new = ny / factor
	array2 = np.empty((nx_new,ny))
	for i in range(nx_new-1):
		array2[i,:] = np.sum(array[i*factor:i*factor+1,:],axis=0)
	
	array3 = np.empty((nx_new,ny_new))
	for j in range(ny_new-1):
		array3[:,j] = np.sum(array2[:,j*factor:j*factor+1],axis=1)

	return array3
	

def system(wcs):
	
	xcoord  = wcs.wcs.ctype[0][0:4]
	ycoord  = wcs.wcs.ctype[1][0:4]
	equinox = wcs.wcs.equinox
	
	if xcoord=='RA--' and ycoord=='DEC-':
		
		if equinox==1950.0:
			return 'fk4'
		elif equinox==2000.0:
			return 'fk5'

	if xcoord=='GLON' and ycoord=='GLAT':
		return 'gal'
		
	return 'unknown'

def smooth(image,sigma):
	i.gaussian_filter(image,sigma=sigma)
	
def setpar(par):
	if not type(par)==str:
		return True
	elif not par=='unset':
		return True
	else:
		return False

def percentile_function(array):

	array = array.ravel()
	array = array[np.where(np.isnan(array)==False)]
	
	n_total  = np.shape(array)[0]
	array = np.sort(array)
		
	x = np.arange(0.,n_total,1.)
	x = x / float(n_total-1)
	
	spl = interp1d(x=x,y=array)
	
	if n_total > 10000:
		x = complete_range(0.,1.,10000)
		spl = interp1d(x=x,y=spl(x))
		
	array = None
		
	return spl

# Make top-right axis from left-bottom axis

def twin(ax):
	
	ax2 = ax.figure.add_axes(ax.get_position(True),frameon=False,aspect='equal')
	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position('right')
	ax.yaxis.tick_left()

	ax2.xaxis.tick_top()
	ax2.xaxis.set_label_position('top')
	ax.xaxis.tick_bottom()

	return ax2
	
def smart_range(array):

	array.sort()

	minval = 360.
	i1 = 0
	i2 = 0

	for i in range(0,np.size(array)-1):
		if 360.-abs(array[i+1]-array[i]) < minval:
			minval = 360.-abs(array[i+1]-array[i])
			i1 = i+1
			i2 = i

	if(max(array)-min(array) < minval):
		i1 = 0
		i2 = np.size(array)-1

	x_min = array[i1]
	x_max = array[i2]

	if(x_min > x_max):
		x_min = x_min - 360.

	return x_min,x_max

def stretcher(arr, stretch, exponent = 2):
      if stretch is 'linear':
            stretchedImg = arr
      elif stretch is 'log': 
            stretchedImg = log10(arr)
      elif stretch is 'sqrt': 
            stretchedImg = sqrt(arr)
      elif stretch is 'arcsinh': 
            stretchedImg = arcsinh(arr)
      elif stretch is 'power': 
            stretchedImg = power(arr, exponent)	
      return stretchedImg

def smart_round_x(x):
	x = x / 15.
	if x > 1:
		x = round(x,0)
	else:
		x = x * 60.
		if x > 1:
			x = round(x,0) / 60.
		else:
			x = x * 60.
			if x > 1:
				x = round(x,0) / 3600.
			else:
				x = x * 100.
				if x > 1:
					x = round(x,0) / 360000.
				else:
					x = x / 100.
	x = x * 15.
	return x

def smart_round_y(y):
	if y > 1:
		y = round(y,0)
	else:
		y = y * 60.
		if y > 1:
			y = round(y,0) / 60.
		else:
			y = y * 60.
			if y > 1:
				y = round(y,0) / 3600.
			else:
				y = y * 100.
				if y > 1:
					y = round(y,0) / 360000.
				else:
					y = y / 100.
	return y
	
	
def complete_range(xmin,xmax,spacing):
	if(xmax-xmin < 1):
		spacing = 10
	xstep = (xmax - xmin) / float(spacing)
	r = np.arange(xmin,xmax,xstep)
	if(np.any(r>=xmax)):
		return r
	else:
		return np.hstack([r,xmax])