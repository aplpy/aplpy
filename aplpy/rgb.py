import os
import warnings

import numpy as np
from astropy import log
from astropy.io import fits
from astropy.coordinates import ICRS
from astropy.visualization import AsymmetricPercentileInterval, simple_norm

from reproject import reproject_interp
from reproject.mosaicking import find_optimal_celestial_wcs


def _data_stretch(image, vmin=None, vmax=None, pmin=0.25, pmax=99.75,
                  stretch='linear', vmid=None, exponent=2):

    if vmin is None or vmax is None:
        interval = AsymmetricPercentileInterval(pmin, pmax, n_samples=10000)
        try:
            vmin_auto, vmax_auto = interval.get_limits(image)
        except IndexError:  # no valid values
            vmin_auto = vmax_auto = 0

    if vmin is None:
        log.info("vmin = %10.3e (auto)" % vmin_auto)
        vmin = vmin_auto
    else:
        log.info("vmin = %10.3e" % vmin)

    if vmax is None:
        log.info("vmax = %10.3e (auto)" % vmax_auto)
        vmax = vmax_auto
    else:
        log.info("vmax = %10.3e" % vmax)

    if stretch == 'arcsinh':
        stretch = 'asinh'

    normalizer = simple_norm(image, stretch=stretch, power=exponent,
                             asinh_a=vmid, min_cut=vmin, max_cut=vmax, clip=False)

    data = normalizer(image, clip=True).filled(0)
    data = np.nan_to_num(data)
    data = np.clip(data * 255., 0., 255.)

    return data.astype(np.uint8)


def make_rgb_image(data, output, indices=(0, 1, 2), vmin_r=None, vmax_r=None,
                   pmin_r=0.25, pmax_r=99.75, stretch_r='linear', vmid_r=None,
                   exponent_r=2, vmin_g=None, vmax_g=None, pmin_g=0.25,
                   pmax_g=99.75, stretch_g='linear', vmid_g=None, exponent_g=2,
                   vmin_b=None, vmax_b=None, pmin_b=0.25, pmax_b=99.75,
                   stretch_b='linear', vmid_b=None, exponent_b=2,
                   make_nans_transparent=False, embed_avm_tags=True):
    """
    Make an RGB image from a FITS RGB cube or from three FITS files.

    Parameters
    ----------

    data : str or tuple or list
        If a string, this is the filename of an RGB FITS cube. If a tuple
        or list, this should give the filename of three files to use for
        the red, green, and blue channel.

    output : str
        The output filename. The image type (e.g. PNG, JPEG, TIFF, ...)
        will be determined from the extension. Any image type supported by
        the Python Imaging Library can be used.

    indices : tuple, optional
        If data is the filename of a FITS cube, these indices are the
        positions in the third dimension to use for red, green, and
        blue respectively. The default is to use the first three
        indices.

    vmin_r, vmin_g, vmin_b : float, optional
        Minimum pixel value to use for the red, green, and blue channels.
        If set to None for a given channel, the minimum pixel value for
        that channel is determined using the corresponding pmin_x argument
        (default).

    vmax_r, vmax_g, vmax_b : float, optional
        Maximum pixel value to use for the red, green, and blue channels.
        If set to None for a given channel, the maximum pixel value for
        that channel is determined using the corresponding pmax_x argument
        (default).

    pmin_r, pmin_r, pmin_g : float, optional
        Percentile values used to determine for a given channel the
        minimum pixel value to use for that channel if the corresponding
        vmin_x is set to None. The default is 0.25% for all channels.

    pmax_r, pmax_g, pmax_b : float, optional
        Percentile values used to determine for a given channel the
        maximum pixel value to use for that channel if the corresponding
        vmax_x is set to None. The default is 99.75% for all channels.

    stretch_r, stretch_g, stretch_b : { 'linear', 'log', 'sqrt', 'arcsinh', 'power' }
        The stretch function to use for the different channels.

    vmid_r, vmid_g, vmid_b : float, optional
        Baseline values used for the log and arcsinh stretches. If
        set to None, this is set to zero for log stretches and to
        vmin - (vmax - vmin) / 30. for arcsinh stretches

    exponent_r, exponent_g, exponent_b : float, optional
        If stretch_x is set to 'power', this is the exponent to use.

    make_nans_transparent : bool, optional
        If set AND output is png, will add an alpha layer that sets pixels
        containing a NaN to transparent.

    embed_avm_tags : bool, optional
        Whether to embed AVM tags inside the image - this can only be done for
        JPEG and PNG files, and only if PyAVM is installed.
    """

    try:
        from PIL import Image
    except ImportError:
        try:
            import Image
        except ImportError:
            raise ImportError("The Python Imaging Library (PIL) is required to make an RGB image")

    if isinstance(data, str):

        image = fits.getdata(data)
        image_r = image[indices[0], :, :]
        image_g = image[indices[1], :, :]
        image_b = image[indices[2], :, :]

        # Read in header
        header = fits.getheader(data)

        # Remove information about third dimension
        header['NAXIS'] = 2
        for key in ['NAXIS', 'CTYPE', 'CRPIX', 'CRVAL', 'CUNIT', 'CDELT', 'CROTA']:
            for coord in range(3, 6):
                name = key + str(coord)
                if name in header:
                    header.__delitem__(name)

    elif (type(data) is list or type(data) is tuple) and len(data) == 3:

        filename_r, filename_g, filename_b = data
        image_r = fits.getdata(filename_r)
        image_g = fits.getdata(filename_g)
        image_b = fits.getdata(filename_b)

        # Read in header
        header = fits.getheader(filename_r)

    else:
        raise Exception("data should either be the filename of a FITS cube or a list/tuple of three images")

    # are we making a transparent layer?
    do_alpha = make_nans_transparent and output.lower().endswith('.png')

    if do_alpha:
        log.info("Making alpha layer")

        # initialize alpha layer
        image_alpha = np.empty_like(image_r, dtype=np.uint8)
        image_alpha[:] = 255

        # look for nans in images
        for im in [image_r, image_g, image_b]:
            image_alpha[np.isnan(im)] = 0

    log.info("Red:")
    image_r = Image.fromarray(_data_stretch(image_r, vmin=vmin_r, vmax=vmax_r,
                                            pmin=pmin_r, pmax=pmax_r, stretch=stretch_r,
                                            vmid=vmid_r, exponent=exponent_r))

    log.info("Green:")
    image_g = Image.fromarray(_data_stretch(image_g,
                                            vmin=vmin_g, vmax=vmax_g,
                                            pmin=pmin_g, pmax=pmax_g,
                                            stretch=stretch_g,
                                            vmid=vmid_g,
                                            exponent=exponent_g))

    log.info("Blue:")
    image_b = Image.fromarray(_data_stretch(image_b,
                                            vmin=vmin_b, vmax=vmax_b,
                                            pmin=pmin_b, pmax=pmax_b,
                                            stretch=stretch_b,
                                            vmid=vmid_b,
                                            exponent=exponent_b))

    img = Image.merge("RGB", (image_r, image_g, image_b))

    if do_alpha:
        # convert to RGBA and add alpha layer
        image_alpha = Image.fromarray(image_alpha)
        img.convert("RGBA")
        img.putalpha(image_alpha)

    img = img.transpose(Image.FLIP_TOP_BOTTOM)

    img.save(output)

    if embed_avm_tags:

        from pyavm import AVM

        if output.lower().endswith(('.jpg', '.jpeg', '.png')):
            avm = AVM.from_header(header)
            avm.embed(output, output)
        else:
            warnings.warn("AVM tags will not be embedded in RGB image, as only JPEG and PNG files are supported")


def make_rgb_cube(files, output, north=True):
    """
    Make an RGB data cube from a list of three FITS images.

    This method can read in three FITS files with different
    projections/sizes/resolutions and uses the `reproject
    <https://reproject.readthedocs.io/en/stable/>`_ package to reproject them all
    to the same projection.

    Two files are produced by this function. The first is a three-dimensional
    FITS cube with a filename give by ``output``, where the third dimension
    contains the different channels. The second is a two-dimensional FITS
    image with a filename given by ``output`` with a `_2d` suffix. This file
    contains the mean of the different channels, and is required as input to
    FITSFigure if show_rgb is subsequently used to show a color image
    generated from the FITS cube (to provide the correct WCS information to
    FITSFigure).

    Parameters
    ----------

    files : tuple or list
       A list of the filenames of three FITS filename to reproject.
       The order is red, green, blue.

    output : str
       The filename of the output RGB FITS cube.

    north : bool, optional
        Whether to rotate the image so that north is up. By default, this is
        assumed to be 'north' in the ICRS frame, but you can also pass any
        astropy :class:`~astropy.coordinates.BaseCoordinateFrame` to indicate
        to use the north of that frame.
    """

    # Check that input files exist
    for f in files:
        if not os.path.exists(f):
            raise Exception("File does not exist : " + f)

    if north is not False:
        frame = ICRS() if north is True else north
        auto_rotate = False
    else:
        frame = None
        auto_rotate = True

    # Find optimal WCS and shape based on input images
    wcs, shape = find_optimal_celestial_wcs(files, frame=frame, auto_rotate=auto_rotate)
    header = wcs.to_header()

    # Generate empty datacube
    image_cube = np.zeros((len(files),) + shape, dtype=np.float32)

    # Loop through files and reproject
    for i, filename in enumerate(files):
        image_cube[i, :, :] = reproject_interp(filename, wcs, shape_out=shape)[0]

    # Write out final cube
    fits.writeto(output, image_cube, header, overwrite=True)

    # Write out collapsed version of cube
    fits.writeto(output.replace('.fits', '_2d.fits'),
                 np.mean(image_cube, axis=0), header, overwrite=True)
