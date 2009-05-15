import os
import random
import string
import sys
import pyfits

def check_status(status):
    if not status == 0:
        raise Exception("An error occured while trying to use Montage")

def reproject_north(hdu):
    
    start_dir = os.path.abspath('.')
    
    # Create work dir
    if not os.path.exists('/tmp/py-montage/'):
        os.mkdir('/tmp/py-montage/')
    
    random_id = "".join([random.choice(string.letters) for i in xrange(16)])
    work_dir = "/tmp/py-montage/"+random_id
    os.mkdir(work_dir)
    
    # Go to work directory
    os.chdir(work_dir)
    
    # Create raw directory
    os.mkdir('raw')
    os.mkdir('final')
    
    # Write out image
    pyfits.writeto('raw/image.fits',hdu.data,hdu.header)
    
    # Make image table
    status = os.system("mImgtbl -c raw images_raw.tbl")
    check_status(status)
    
    # Make new north-aligned header
    os.system("mMakeHdr -n images_raw.tbl header.hdr")
    
    proj = hdu.header['CTYPE1'][5:8]
    
    if proj in ['TAN','SIN','ZEA','STG','ARC']:
        print "[montage] using fast reprojection"
        binary = 'mProjectPP'
    else:
        print "[montage] using normal reprojection"
        binary = 'mProject'
    
    # Project image
    os.system(binary+" raw/image.fits final/image.fits header.hdr")
    
    # Read in output image
    hdu = pyfits.open('final/image.fits')[0]
    
    os.chdir(start_dir)
    
    return hdu
    