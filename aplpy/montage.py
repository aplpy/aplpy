import os
import random
import string
import pyfits
import tempfile
import numpy as np

_fast = ['TAN', 'SIN', 'ZEA', 'STG', 'ARC']


def _installed():

    installed = False
    for dir in os.environ['PATH'].split(':'):
        if os.path.exists(dir+'/mProject'):
            installed=True
            break

    return installed


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
    pyfits.writeto('raw/image.fits', hdu.data, hdu.header)

    # Make image table
    status = os.system("mImgtbl -c raw images_raw.tbl")
    check_status(status)

    # Make new north-aligned header
    os.system("mMakeHdr -n images_raw.tbl header.hdr")

    proj = hdu.header['CTYPE1'][5:8]

    if proj in _fast:
        print "[montage] using fast reprojection"
        binary = 'mProjectPP'
    else:
        print "[montage] using normal reprojection"
        binary = 'mProject'

    # Project image
    os.system(binary+" raw/image.fits final/image.fits header.hdr")

    os.system("mConvert -b -32 final/image.fits final/image32.fits")

    # Read in output image
    hdu = pyfits.open('final/image32.fits')[0]

    os.chdir(start_dir)

    return hdu


def make_rgb_cube(files, output):
    '''
    Make an RGB data cube from a list of three FITS images.

    This method can read in three FITS files with different
    projections/sizes/resolutions and uses Montage to reproject
    them all to the same projection.

    Required arguments:

        *files* [ tuple | list ]
            A list of the filenames of three FITS filename to reproject.
            The order is red, green, blue.

        *output* [ string ]
            The filename of the output RGB FITS cube.

    '''

    if not _installed():
        raise Exception("Montage needs to be installed and in the $PATH in order to use aplpy.make_rgb_cube()")

    # Remember starting directory
    start_dir = os.path.abspath('.')

    # Check files are there
    for i in range(len(files)):
        files[i] = os.path.abspath(files[i])
        if not os.path.exists(files[i]): raise Exception("File does not exist : "+files[i])

    # Find path to output file
    output = os.path.abspath(output)

    # Create work dir
    work_dir = tempfile.mkdtemp()

    # Go to work directory
    os.chdir(work_dir)

    # Create raw and final directory
    os.mkdir('raw')
    os.mkdir('final')

    # Create symbolic links to input files
    for i, f in enumerate(files):
        os.symlink(f, 'raw/image'+str(i)+'.fits')

    # List files and create optimal header
    os.system('mImgtbl -c raw images_raw.tbl')
    os.system('mMakeHdr images_raw.tbl header.hdr')

    # Write out header without 'END'
    f1 = file('header.hdr', 'rb')
    f2 = file('header_py.hdr', 'wb')
    f2.writelines(f1.readlines()[:-1])
    f1.close()
    f2.close()

    # Read header in with pyfits
    header = pyfits.Header()
    header.fromTxtFile('header_py.hdr', replace=True)

    # Find image dimensions
    nx = int(header['NAXIS1'])
    ny = int(header['NAXIS2'])

    # Generate emtpy cube
    image_cube = np.zeros((len(files), ny, nx), dtype=np.float32)

    # Loop through files
    for i in range(len(files)):

        os.mkdir('raw'+str(i))
        os.mkdir('tmp'+str(i))
        os.symlink(os.path.abspath(files[i]), 'raw'+str(i)+'/image'+str(i)+'.fits')

        if header['CTYPE1'][5:8] in _fast:
            header_indiv = pyfits.getheader('raw'+str(i)+'/image'+str(i)+'.fits')
            if header_indiv['CTYPE1'][5:8] in _fast:
                binary = 'mProjectPP'
            else:
                binary = 'mProject'
        else:
            binary = 'mProject'

        os.system(binary+" raw"+str(i)+"/image"+str(i)+".fits tmp"+str(i)+"/image"+str(i)+".fits header.hdr")
        os.system("mImgtbl -c tmp"+str(i)+" images_tmp"+str(i)+".tbl")
        os.system("mAdd -e -p tmp"+str(i)+" images_tmp"+str(i)+".tbl header.hdr final/image"+str(i)+".fits")
        os.system("mConvert -b -32 final/image"+str(i)+".fits final/image"+str(i)+"32.fits")

        image_cube[i, :, :] = pyfits.getdata('final/image'+str(i)+'32.fits')

    pyfits.writeto(output, image_cube, header, clobber=True)

    pyfits.writeto(output.replace('.fits', '_2d.fits'), \
                   np.sum(image_cube, axis=0), header, clobber=True)

    os.chdir(start_dir)

    return
