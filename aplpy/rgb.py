from __future__ import absolute_import

from distutils import version
import os
import warnings

import tempfile
import shutil

import pyfits
import numpy as np

from aplpy.logger import logger

try:
    import Image
    installed_pil = True
except:
    installed_pil = False

try:
    import montage
    if not hasattr(montage, 'reproject_hdu'):
        raise
    montage_installed = True
except:
    montage_installed = False

try:
    from pyavm import AVM
    avm_installed = True
except:
    avm_installed = False

if montage_installed:
    if version.LooseVersion(montage.__version__) < version.LooseVersion('0.9.2'):
        warnings.warn("Python-montage installation is not recent enough (version 0.9.2 or later is required). Disabling Montage-related functionality.")
        montage_installed = False

import aplpy.image_util as image_util
import aplpy.math_util as math_util


def _data_stretch(image, vmin=None, vmax=None, pmin=0.25, pmax=99.75, \
                  stretch='linear', vmid=None, exponent=2):

    min_auto = not math_util.isnumeric(vmin)
    max_auto = not math_util.isnumeric(vmax)

    if min_auto or max_auto:
        auto_v = image_util.percentile_function(image)
        vmin_auto, vmax_auto = auto_v(pmin), auto_v(pmax)

    if min_auto:
        logger.info("vmin = %10.3e (auto)" % vmin_auto)
        vmin = vmin_auto
    else:
        logger.info("vmin = %10.3e" % vmin)

    if max_auto:
        logger.info("vmax = %10.3e (auto)" % vmax_auto)
        vmax = vmax_auto
    else:
        logger.info("vmax = %10.3e" % vmax)

    image = (image - vmin) / (vmax - vmin)

    data = image_util.stretch(image, stretch, exponent=exponent, midpoint=vmid)

    data = np.nan_to_num(data)
    data = np.clip(data * 255., 0., 255.)

    return data.astype(np.uint8)


def make_rgb_image(data, output, indices=(0, 1, 2), \
                   vmin_r=None, vmax_r=None, pmin_r=0.25, pmax_r=99.75, \
                   stretch_r='linear', vmid_r=None, exponent_r=2, \
                   vmin_g=None, vmax_g=None, pmin_g=0.25, pmax_g=99.75, \
                   stretch_g='linear', vmid_g=None, exponent_g=2, \
                   vmin_b=None, vmax_b=None, pmin_b=0.25, pmax_b=99.75, \
                   stretch_b='linear', vmid_b=None, exponent_b=2, \
                   embed_avm_tags=False):
    '''
    Make an RGB image from a FITS RGB cube or from three FITS files

    Required arguments:

        *data*: [ string | tuple | list ]
            If a string, this is the filename of an RGB FITS cube. If a tuple
            or list, this should give the filename of three files to use for
            the red, green, and blue channel.

        *output*: [ string ]
            The output filename. The image type (e.g. PNG, JPEG, TIFF, ...)
            will be determined from the extension. Any image type supported by
            the Python Imaging Library can be used.

    Optional keyword arguments:

        *indices*: [ tuple ]
            If data is the filename of a FITS cube, these indices are the
            positions in the third dimension to use for red, green, and
            blue respectively. The default is to use the first three
            indices.

        *vmin_r*: [ None | float ]

        *vmin_g*: [ None | float ]

        *vmin_b*: [ None | float ]

            Minimum pixel value to use for the red, green, and blue channels.
            If set to None for a given channel, the minimum pixel value for
            that channel is determined using the corresponding pmin_x argument
            (default).

        *vmax_r*: [ None | float ]

        *vmax_g*: [ None | float ]

        *vmax_b*: [ None | float ]

            Maximum pixel value to use for the red, green, and blue channels.
            If set to None for a given channel, the maximum pixel value for
            that channel is determined using the corresponding pmax_x argument
            (default).

        *pmin_r*: [ float ]

        *pmin_g*: [ float ]

        *pmin_b*: [ float ]

            Percentile values used to determine for a given channel the
            minimum pixel value to use for that channel if the corresponding
            vmin_x is set to None. The default is 0.25% for all channels.

        *pmax_r*: [ float ]

        *pmax_g*: [ float ]

        *pmax_b*: [ float ]

            Percentile values used to determine for a given channel the
            maximum pixel value to use for that channel if the corresponding
            vmax_x is set to None. The default is 99.75% for all channels.

        *stretch_r*: [ 'linear' | 'log' | 'sqrt' | 'arcsinh' | 'power' ]

        *stretch_g*: [ 'linear' | 'log' | 'sqrt' | 'arcsinh' | 'power' ]

        *stretch_b*: [ 'linear' | 'log' | 'sqrt' | 'arcsinh' | 'power' ]

            The stretch function to use for the different channels.

        *vmid_r*: [ None | float ]

        *vmid_g*: [ None | float ]

        *vmid_b*: [ None | float ]

            Baseline values used for the log and arcsinh stretches. If
            set to None, this is set to zero for log stretches and to
            vmin - (vmax - vmin) / 30. for arcsinh stretches

        *exponent_r*: [ float ]

        *exponent_g*: [ float ]

        *exponent_b*: [ float ]

            If stretch_x is set to 'power', this is the exponent to use.
        '''

    if not installed_pil:
        raise Exception("The Python Imaging Library (PIL) is not installed but is required for this function")

    if isinstance(data, basestring):

        image = pyfits.getdata(data)
        image_r = image[indices[0], :, :]
        image_g = image[indices[1], :, :]
        image_b = image[indices[2], :, :]

        # Read in header
        header = pyfits.getheader(data)

        # Remove information about third dimension
        header['NAXIS'] = 2
        for key in ['NAXIS', 'CTYPE', 'CRPIX', 'CRVAL', 'CUNIT', 'CDELT', 'CROTA']:
            for coord in range(3, 6):
                name = key + str(coord)
                if name in header:
                    header.__delitem__(name)

    elif (type(data) == list or type(data) == tuple) and len(data) == 3:

        filename_r, filename_g, filename_b = data
        image_r = pyfits.getdata(filename_r)
        image_g = pyfits.getdata(filename_g)
        image_b = pyfits.getdata(filename_b)

        # Read in header
        header = pyfits.getheader(filename_r)

    else:
        raise Exception("data should either be the filename of a FITS cube or a list/tuple of three images")

    logger.info("Red:")
    image_r = Image.fromarray(_data_stretch(image_r, \
                                            vmin=vmin_r, vmax=vmax_r, \
                                            pmin=pmin_r, pmax=pmax_r, \
                                            stretch=stretch_r, \
                                            vmid=vmid_r, \
                                            exponent=exponent_r))

    logger.info("\nGreen:")
    image_g = Image.fromarray(_data_stretch(image_g, \
                                            vmin=vmin_g, vmax=vmax_g, \
                                            pmin=pmin_g, pmax=pmax_g, \
                                            stretch=stretch_g, \
                                            vmid=vmid_g, \
                                            exponent=exponent_g))

    logger.info("\nBlue:")
    image_b = Image.fromarray(_data_stretch(image_b, \
                                            vmin=vmin_b, vmax=vmax_b, \
                                            pmin=pmin_b, pmax=pmax_b, \
                                            stretch=stretch_b, \
                                            vmid=vmid_b, \
                                            exponent=exponent_b))

    img = Image.merge("RGB", (image_r, image_g, image_b))
    img = img.transpose(Image.FLIP_TOP_BOTTOM)

    img.save(output)

    if embed_avm_tags:
        if not avm_installed:
            raise Exception("PyAVM needs to be installed in order to be able to embed AVM tags into the RGB image")
        else:
            avm = AVM(header)
            avm.embed(output, output)

    return


def make_rgb_cube(files, output, north=False, system=None, equinox=None):
    '''
    Make an RGB data cube from a list of three FITS images.

    This method can read in three FITS files with different
    projections/sizes/resolutions and uses Montage to reproject
    them all to the same projection.

    Two files are produced by this function. The first is a three-dimensional
    FITS cube with a filename give by `output`, where the third dimension
    contains the different channels. The second is a two-dimensional FITS
    image with a filename given by `output` with a `_2d` suffix. This file
    contains the mean of the different channels, and is required as input to
    FITSFigure if show_rgb is subsequently used to show a color image
    generated from the FITS cube (to provide the correct WCS information to
    FITSFigure).

    Required arguments:

        *files* [ tuple | list ]
            A list of the filenames of three FITS filename to reproject.
            The order is red, green, blue.

        *output* [ string ]
            The filename of the output RGB FITS cube.

    Optional Keyword Arguments:

        *north* [ True | False ]
            By default, the FITS header generated by Montage represents the
            best fit to the images, often resulting in a slight rotation. If
            you want north to be straight up in your final mosaic, you should
            use this option.

        *system* [ string ]
            Specifies the system for the header (default is EQUJ).
            Possible values are: EQUJ EQUB ECLJ ECLB GAL SGAL

        *equinox* [ string ]
            If a coordinate system is specified, the equinox can also be given
            in the form YYYY. Default is J2000.
    '''

    # Check whether the Python montage module is installed. The Python module
    # checks itself whether the Montage command-line tools are available, and
    # if they are not then importing the Python module will fail.
    if not montage_installed:
        raise Exception("Both the Montage command-line tools and the Python-montage module are required for this function")

    # Check that input files exist
    for f in files:
        if not os.path.exists(f):
            raise Exception("File does not exist : " + f)

    # Create work directory
    work_dir = tempfile.mkdtemp()

    raw_dir = '%s/raw' % work_dir
    final_dir = '%s/final' % work_dir

    images_raw_tbl = '%s/images_raw.tbl' % work_dir
    header_hdr = '%s/header.hdr' % work_dir
    header_py_hdr = '%s/header_py.hdr' % work_dir

    # Create raw and final directory in work directory
    os.mkdir(raw_dir)
    os.mkdir(final_dir)

    # Create symbolic links to input files
    for i, f in enumerate(files):
        os.symlink(os.path.abspath(f), '%s/image_%i.fits' % (raw_dir, i))

    # List files and create optimal header
    montage.mImgtbl(raw_dir, images_raw_tbl, corners=True)
    montage.mMakeHdr(images_raw_tbl, header_hdr, north_aligned=north, system=system, equinox=equinox)

    # Write out header without 'END'
    contents = open(header_hdr).read()
    open(header_py_hdr, 'wb').write(contents.replace('END\n', ''))

    # Read header in with pyfits
    header = pyfits.Header()
    header.fromTxtFile(header_py_hdr, replace=True)

    # Find image dimensions
    nx = int(header['NAXIS1'])
    ny = int(header['NAXIS2'])

    # Generate emtpy datacube
    image_cube = np.zeros((len(files), ny, nx), dtype=np.float32)

    # Loop through files
    for i in range(len(files)):

        # Reproject channel to optimal header
        montage.reproject('%s/image_%i.fits' % (raw_dir, i),
                          '%s/image_%i.fits' % (final_dir, i),
                          header=header_hdr, exact_size=True, bitpix=-32)

        # Read in and add to datacube
        image_cube[i, :, :] = pyfits.getdata('%s/image_%i.fits' % (final_dir, i))

    # Write out final cube
    pyfits.writeto(output, image_cube, header, clobber=True)

    # Write out collapsed version of cube
    pyfits.writeto(output.replace('.fits', '_2d.fits'), \
                   np.mean(image_cube, axis=0), header, clobber=True)

    # Remove work directory
    shutil.rmtree(work_dir)

    return
