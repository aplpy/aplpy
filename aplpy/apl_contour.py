import numpy as np
from matplotlib.collections import LineCollection
from time import time
import sys
import apl_coords as c

def draw_new_contours(ax,wcs_in,wcs_out):
	print "Transforming contour coordinates..."
	start = time()
	print len(ax.collections)
	
	# Check that both files are in same coordinate system
	
	xcoord_in  = wcs_in.wcs.ctype[0][0:4]
	xcoord_out = wcs_out.wcs.ctype[0][0:4]
	
	gal2fk5 = False
	fk52gal = False
	
	if not xcoord_in == xcoord_out:
		print xcoord_in,xcoord_out
		if not xcoord_in in ['GLON','RA--'] or not xcoord_out in ['GLON','RA--']:
			sys.exit()
		
		gal2fk5 = xcoord_in == 'GLON' and xcoord_out == 'RA--'
		fk52gal = xcoord_in == 'RA--' and xcoord_out == 'GLON'
		
	if gal2fk5: print "[warning] converting contours from galactic to equatorial"
	if fk52gal: print "[warning] converting contours from equatorial to galactic"
		
	for i in range(len(ax.collections)):
		
		try:
			process = not ax.collections[i].apl_corrected
		except AttributeError:
			process = True
			ax.collections[i].apl_corrected = True
			
		if process:
						
			polygons_out = []
			for polygon in ax.collections[i].get_paths():
			
				xp_in = polygon.vertices[:,0]
				yp_in = polygon.vertices[:,1]
				
				xw,yw = wcs_in.wcs_pix2sky_fits(xp_in,yp_in)
			
				if gal2fk5:
					for ic in range(len(xw)):
						xw[ic],yw[ic] = c.gal2fk5(xw[ic],yw[ic])
					xw = np.array(xw)
					xy = np.array(yw)
				
				if fk52gal:
					for ic in range(len(xw)):
						xw[ic],yw[ic] = c.fk52gal(xw[ic],yw[ic])
					xw = np.array(xw)
					xy = np.array(yw)
						
				xp_out,yp_out = wcs_out.wcs_sky2pix_fits(xw,yw)

				polygons_out.append(zip(xp_out,yp_out))
				
			ax.collections[i].set_verts(polygons_out)
			ax.collections[i].apl_converted = True
			
	total = round(time() - start,4)
	print "Done in "+str(total)+" seconds"
	return ax
