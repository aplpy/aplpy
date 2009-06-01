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
    
    # Remove any extra coordinates
    for key in ['CTYPE','CRPIX','CRVAL','CUNIT','CDELT']:
        for coord in range(3,5):
           name = key + str(coord)
           if header.has_key(name):
               header.__delitem__(name)
    
    return header
    
    
    
    