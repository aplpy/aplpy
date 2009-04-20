import numpy as np

import pywcs

import wcs_util

def check(header):
    
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
    
    if xproj<>yproj:
        raise Exception("x and y projections do not agree")
    
    # If projection is -CAR, then make sure the projection center is within the image
    
    if xproj == '-CAR':
        if crpix1 < 0.5 or crpix1 > nx + 0.5 or crpix2 < 0.5 or crpix2 > ny + 0.5:
            xcw,ycw = wcs_util.pix2world(wcs,xcp,ycp)
            header.update('CRVAL1',xcw)
            header.update('CRVAL2',ycw)
            header.update('CRPIX1',xcp)
            header.update('CRPIX2',ycp)
            if header.has_key('LONPOLE'):
                lonpole = float(header['LONPOLE'])
                if lonpole == 0. or lonpole == 180.:
                    if ycw >= 0.:
                        header.update('LONPOLE',0.)
                    else:
                        header.update('LONPOLE',180.)
            
            print "[check] updated projection center"
    
    return header

    
    
    