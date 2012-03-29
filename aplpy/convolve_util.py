from numpy.fft import fft2, ifft2
from numpy import log, exp, mgrid, array, mod, ones, isnan, nan_to_num, nan, sum

# Function was adopted from http://www.scipy.org/Cookbook/SignalSmooth


def gauss_kern(sigma, sigmay=None):
    """ Returns a normalized 2D gauss kernel array for convolutions"""
    sigma = int(sigma)
    if not sigmay:
        sigmay = sigma
    else:
        sigmay = int(sigmay)
    x, y = mgrid[-sigma:sigma + 1, -sigmay:sigmay + 1]
    g = exp(-(x ** 2 / float(sigma) + y ** 2 / float(sigmay)))
    return g / g.sum()


def box_kern(size, sizey=None):
    size = int(size)
    if not sizey:
        sizey = size
    else:
        sizey = int(sizey)
    return ones((size, sizey))

# Function was adopted and modified from
# http://www.rzuser.uni-heidelberg.de/~ge6/Programing/convolution.html


def convolve(image, smooth=3, kernel='gauss', minpad=True, pad=True):
    """ Not so simple convolution """
    if smooth is None:
        return image

    if sum(isnan(image)) > 0:
        nan_present = True
        index = isnan(image)
        image = nan_to_num(image)
    else:
        nan_present = False

    if type(smooth) == type(()):
        if kernel == 'gauss':
            kernel = gauss_kern(smooth[0], smooth[1])
        elif kernel == 'box':
            kernel = box_kern(smooth[0], smooth[1])
        else:
            kernel = kernel

    else:
        if kernel == 'gauss':
            kernel = gauss_kern(smooth)
        elif kernel == 'box':
            kernel = box_kern(smooth)
        else:
            kernel = kernel

    kernel = kernel / sum(kernel)

    FFt = fft2
    iFFt = ifft2

    #The size of the images:
    x1, y1 = image.shape
    x2, y2 = kernel.shape

    #MinPad results simpler padding, smaller images:
    if minpad:
        r = x1 + x2
        c = y1 + y2
    else:
        #if the Numerical Recipies says so:
        r = 2 * max(x1, x2)
        c = 2 * max(y1, y2)

    #For nice FFT, we need the power of 2:
    if pad:
        px2 = int(log(r) / log(2.0) + 1.0)
        py2 = int(log(c) / log(2.0) + 1.0)
        rOrig = r
        cOrig = c
        r = 2 ** px2
        c = 2 ** py2

    #numpy fft has the padding built in, which can save us some steps
    #here. The thing is the s(hape) parameter:
    fftimage = FFt(image, s=(r, c)) * FFt(kernel, s=(r, c))

    if pad:
        img = ((iFFt(fftimage))[:rOrig, :cOrig]).real
    else:
        img = (iFFt(fftimage)).real
    diff = array([img.shape[0] - image.shape[0], img.shape[1] - image.shape[1]])

    if mod(diff[0], 2) == 0:
        xcrop = [diff[0] / 2, img.shape[0] - diff[0] / 2]
    else:
        xcrop = [diff[0] / 2, img.shape[0] - diff[0] / 2 - 1]

    if mod(diff[1], 2) == 0:
        ycrop = [diff[1] / 2, img.shape[1] - diff[1] / 2]
    else:
        ycrop = [diff[1] / 2, img.shape[1] - diff[1] / 2 - 1]

    img = img[xcrop[0]:xcrop[1], ycrop[0]:ycrop[1]]

    if nan_present:
        img[index] = nan
        return img
    else:
        return img
