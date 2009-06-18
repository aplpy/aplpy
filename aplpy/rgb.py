import pyfits
import numpy as np
import Image
import image_util

def _data_stretch(image,stretch='linear',exponent=2,divisor=10,vmin='default',vmax='default',percentile_lower=0.0025,percentile_upper=0.9975):
    
    min_auto = type(vmin) == str
    max_auto = type(vmax) == str
    
    if min_auto or max_auto:
        auto_v = image_util.percentile_function(image)
        vmin_auto,vmax_auto = auto_v(percentile_lower),auto_v(percentile_upper)
    
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

def make_rgb_image(data,output,vmin_r='default',vmax_r='default',vmin_g='default',vmax_g='default',vmin_b='default',vmax_b='default',**kwargs):
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
        
        *vmin_r*: [ float ]
            Minimum pixel value to show for the red channel (default is to use the 0.25% percentile)
        
        *vmax_r*: [ float ]
            Maximum pixel value to show for the red channel (default is to use the 99.97% percentile)
            
        *vmin_g*: [ float ]
            Minimum pixel value to show for the green channel (default is to use the 0.25% percentile)

        *vmax_g*: [ float ]
            Maximum pixel value to show for the green channel (default is to use the 99.97% percentile)
            
        *vmin_b*: [ float ]
            Minimum pixel value to show for the blue channel (default is to use the 0.25% percentile)

        *vmax_b*: [ float ]
            Maximum pixel value to show for the blue channel (default is to use the 99.97% percentile)
            
        *stretch*: [ 'linear' | 'log' | 'sqrt' | 'arcsinh' | 'power' ]
            The stretch function to use
        
        *exponent*: [ float ]
            If stretch is set to 'power', this is the exponent to use
        
        *percentile_lower*: [ float ]
            If vmin is not specified, this value is used to determine the
            percentile position of the faintest pixel to use in the scale. The
            default value is 0.0025 (0.25%). This value is used for all channels.
        
        *percentile_upper*: [ float ]
            If vmax is not specified, this value is used to determine the
            percentile position of the brightest pixel to use in the scale. The
            default value is 0.9975 (99.75%). This value is used for all channels.
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
    image_r = Image.fromarray(_data_stretch(image_r,vmin=vmin_r,vmax=vmax_r,**kwargs))
    
    print "\nGreen:"
    image_g = Image.fromarray(_data_stretch(image_g,vmin=vmin_g,vmax=vmax_g,**kwargs))

    print "\nBlue:"
    image_b = Image.fromarray(_data_stretch(image_b,vmin=vmin_b,vmax=vmax_b,**kwargs))

    img = Image.merge("RGB",(image_r,image_g,image_b))
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(output)
    
    return
    
