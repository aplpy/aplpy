import pywcs
import numpy as np

def check_header(header):
	
	wcs = pywcs.WCS(header)
	
	xproj = header['CTYPE1']
	yproj = header['CTYPE2']
	
	xproj = xproj[4:8]
	yproj = yproj[4:8]
	
	crpix1 = float(header['CRPIX1'])
	crpix2 = float(header['CRPIX2'])
	
	nx = int(header['NAXIS1'])
	ny = int(header['NAXIS1'])
	
	xcp = float(nx / 2)
	ycp = float(ny / 2)
		
	# Check that the two projections are equal
	
	if xproj==yproj:
		print "[check] x and y projections agree"
	else:
		print "[check] x and y projections do not agree"
		
	# If projection is -CAR, then make sure the projection center is within the image
	
	if xproj == '-CAR':
		if crpix1 < 0.5 or crpix1 > nx + 0.5 or crpix2 < 0.5 or crpix2 > ny + 0.5:
			xcw,ycw = wcs.wcs_pix2sky_fits(np.array([xcp]),np.array([ycp]))
			header.update('CRVAL1',xcw[0])
			header.update('CRVAL2',ycw[0])
			header.update('CRPIX1',xcp)
			header.update('CRPIX2',ycp)
			if header.has_key('LONPOLE'):
				lonpole = float(header['LONPOLE'])
				if lonpole == 0. or lonpole == 180.:
					if ycw[0] >= 0.:
						header.update('LONPOLE',0.)
					else:
						header.update('LONPOLE',180.)
				
			print "[check] updated projection center"	
			
	return header
		
			
	