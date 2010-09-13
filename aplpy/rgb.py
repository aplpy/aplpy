import pyfits
import numpy as np

try:
    import Image
    installed_pil = True
except:
    installed_pil = False

import image_util
import math_util as m


def _data_stretch(image, vmin=None, vmax=None, pmin=0.25, pmax=99.75, \
                  stretch='linear', vmid=None, exponent=2):

    min_auto = not m.isnumeric(vmin)
    max_auto = not m.isnumeric(vmax)

    if min_auto or max_auto:
        auto_v = image_util.percentile_function(image)
        vmin_auto, vmax_auto = auto_v(pmin), auto_v(pmax)

    if min_auto:
        print "vmin = %10.3e (auto)" % vmin_auto
        vmin = vmin_auto
    else:
        print "vmin = %10.3e" % vmin

    if max_auto:
        print "vmax = %10.3e (auto)" % vmax_auto
        vmax = vmax_auto
    else:
        print "vmax = %10.3e" % vmax

    image = (image - vmin) / (vmax - vmin)

    data = image_util.stretch(image, stretch, exponent=exponent, midpoint=vmid)

    data = np.nan_to_num(data)
    data = np.clip(data*255., 0., 255.)

    return data.astype(np.uint8)


def make_rgb_image(data, output, \
                   vmin_r=None, vmax_r=None, pmin_r=0.25, pmax_r=99.75, \
                   stretch_r='linear', vmid_r=None, exponent_r=2, \
                   vmin_g=None, vmax_g=None, pmin_g=0.25, pmax_g=99.75, \
                   stretch_g='linear', vmid_g=None, exponent_g=2, \
                   vmin_b=None, vmax_b=None, pmin_b=0.25, pmax_b=99.75, \
                   stretch_b='linear', vmid_b=None, exponent_b=2):
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

            Mid-pixel value used for the log and arcsinh stretches. If
            set to None, this is set to a sensible value.

        *exponent_r*: [ float ]

        *exponent_g*: [ float ]

        *exponent_b*: [ float ]

            If stretch_x is set to 'power', this is the exponent to use.
        '''

    if not installed_pil:
        print '''ERROR : The Python Imaging Library (PIL) is not installed but is required for this function'''
        return

    if type(data) == str:
        image = pyfits.getdata(data)
        image_r = image[0,:,:]
        image_g = image[1,:,:]
        image_b = image[2,:,:]
    elif (type(data) == list or type(data) == tuple) and len(data) == 3:
        filename_r, filename_g, filename_b = data
        image_r = pyfits.getdata(filename_r)
        image_g = pyfits.getdata(filename_g)
        image_b = pyfits.getdata(filename_b)
    else:
        raise Exception("data should either be the filename of a FITS cube or a list/tuple of three images")

    print "Red:"
    image_r = Image.fromarray(_data_stretch(image_r, \
                                            vmin=vmin_r, vmax=vmax_r, \
                                            pmin=pmin_r, pmax=pmax_r, \
                                            stretch=stretch_r, \
                                            vmid=vmid_r, \
                                            exponent=exponent_r))

    print "\nGreen:"
    image_g = Image.fromarray(_data_stretch(image_g, \
                                            vmin=vmin_g, vmax=vmax_g, \
                                            pmin=pmin_g, pmax=pmax_g, \
                                            stretch=stretch_g, \
                                            vmid=vmid_g, \
                                            exponent=exponent_g))

    print "\nBlue:"
    image_b = Image.fromarray(_data_stretch(image_b, \
                                            vmin=vmin_b, vmax=vmax_b, \
                                            pmin=pmin_b, pmax=pmax_b, \
                                            stretch=stretch_b, \
                                            vmid=vmid_b, \
                                            exponent=exponent_b))

    img = Image.merge("RGB", (image_r, image_g, image_b))
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(output)

    return
