import pyfits
import numpy as np
import Image
import image_util
import math_util as m

def _data_stretch(image,vmin=None,vmax=None,pmin=0.25,pmax=99.75,stretch='linear',exponent=2):
    
    min_auto = not m.isnumeric(vmin)
    max_auto = not m.isnumeric(vmax)
    
    if min_auto or max_auto:
        auto_v = image_util.percentile_function(image)
        vmin_auto,vmax_auto = auto_v(pmin),auto_v(pmax)
    
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
    
    stretched_image = (image - vmin) / (vmax - vmin)
    
    data = image_util.stretch(stretched_image,stretch,exponent=exponent)
    
    data = np.nan_to_num(data)
    data = np.clip(data*255.,0.,255.)
    
    return data.astype(np.uint8)

def make_rgb_image(data,output, \
                   vmin_r=None,vmax_r=None,vmin_g=None,vmax_g=None,vmin_b=None,vmax_b=None, \
                   pmin_r=0.25,pmax_r=99.75,pmin_g=0.25,pmax_g=99.75,pmin_b=0.25,pmax_b=99.75, \
                   **kwargs):
    '''
    Make an RGB image from a FITS RGB cube or from three FITS files
    
    Required arguments:
        
        *data*: [ string | tuple | list ]
            If a string, this is the filename of an RGB FITS cube. If a tuple or list,
            this should give the filename of three files to use for the red, green, and
            blue channel.
        
        *output*: [ string ]
            The output filename. The image type (e.g. PNG, JPEG, TIFF, ...) will be
            determined from the extension. Any image type supported by the Python
            Imaging Library can be used.
    
    Optional keyword arguments:
        
        *vmin_r*: [ None | float ]
        *vmin_g*: [ None | float ]
        *vmin_b*: [ None | float ]
            Minimum pixel value to use for the red, green, and blue channels.
            If set to None for a given channel, the minimum pixel value for
            that channel is determined using the corresponding pmin_? argument
            (default).
        
        *vmax_r*: [ None | float ]
        *vmax_g*: [ None | float ]
        *vmax_b*: [ None | float ]
            Maximum pixel value to use for the red, green, and blue channels.
            If set to None for a given channel, the maximum pixel value for
            that channel is determined using the corresponding pmax_? argument
            (default).
        
        *pmin_r*: [ float ]
        *pmin_g*: [ float ]
        *pmin_b*: [ float ]
            Percentile values used to determine for a given channel the
            minimum pixel value to use for that channel if the corresponding
            vmin_? is set to None. The default is 0.25% for all channels.
        
        *pmax_r*: [ float ]
        *pmax_g*: [ float ]
        *pmax_b*: [ float ]
            Percentile values used to determine for a given channel the
            maximum pixel value to use for that channel if the corresponding
            vmax_? is set to None. The default is 99.75% for all channels.
        
        *stretch*: [ 'linear' | 'log' | 'sqrt' | 'arcsinh' | 'power' ]
            The stretch function to use for all channels.
        
        *exponent*: [ float ]
            If stretch is set to 'power', this is the exponent to use.
        '''
    
    if type(data) == str:
        image = pyfits.getdata(data)
        image_r = image[0,:,:]
        image_g = image[1,:,:]
        image_b = image[2,:,:]
    elif (type(data) == list or type(data) == tuple) and len(data) == 3:
        filename_r,filename_g,filename_b = data
        image_r = pyfits.getdata(filename_r)
        image_g = pyfits.getdata(filename_g)
        image_b = pyfits.getdata(filename_b)
    else:
        raise Exception("data should either be the filename of a FITS cube or a list/tuple of three images")
    
    print "Red:"
    image_r = Image.fromarray(_data_stretch(image_r,vmin=vmin_r,vmax=vmax_r,pmin=pmin_r,pmax=pmax_r,**kwargs))
    
    print "\nGreen:"
    image_g = Image.fromarray(_data_stretch(image_g,vmin=vmin_g,vmax=vmax_g,pmin=pmin_g,pmax=pmax_g,**kwargs))
    
    print "\nBlue:"
    image_b = Image.fromarray(_data_stretch(image_b,vmin=vmin_b,vmax=vmax_b,pmin=pmin_b,pmax=pmax_b,**kwargs))
    
    img = Image.merge("RGB",(image_r,image_g,image_b))
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(output)
    
    return
    
