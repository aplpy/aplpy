import operator


def slice(hdu, slices=[]):
    '''
    Extract a slice from an n-dimensional FITS HDU, and return an HDU
    '''

    if type(slices) == int:
        slices = (slices, )

    shape = hdu.data.shape

    if len(shape) < 2:

        raise Exception("FITS file does not have enough dimensions")

    elif len(shape) == 2:

        return hdu

    else:

        n_total = reduce(operator.mul, shape)
        n_image = reduce(operator.mul, shape[-2:])

        if n_total == n_image:
            slices = tuple([0 for i in range(1, len(shape)-1)])
            hdu.data = hdu.data[slices]
        elif slices:
            if type(slices) == list:
                slices = tuple(slices)
            hdu.data = hdu.data[slices]
        else:
            message = '''
    Attempted to read in %i-dimensional FITS cube, but
    slices were not specified. Please specify slices
    using the slices= argument. The extra dimensions are:\n
                       ''' % len(shape)
            for i in range(3, len(shape)+1):
                name = "CTYPE%i" % i
                message += " %s %i\n" % (hdu.header["CTYPE%i" % i],
                                         hdu.header["NAXIS%i" % i])

            raise Exception(message)

        # Remove any extra coordinates
        for key in ['CTYPE', 'CRPIX', 'CRVAL', 'CUNIT', 'CDELT', 'CROTA',
                    'NAXIS']:
            for i in range(3, len(shape)+1):
                name = "%s%i" % (key, i)
                if name in hdu.header:
                    hdu.header.__delitem__(name)

        for i in range(1, len(shape)+1):
            for j in range(1, len(shape)+1):
                if i > 2 or j > 2:
                    name = "CD%i_%i" % (i, j)
                    if name in hdu.header:
                        hdu.header.__delitem__(name)

        hdu.header.update('NAXIS', 2)

        return hdu
