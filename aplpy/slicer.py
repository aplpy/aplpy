from __future__ import absolute_import

import operator


def slice_hypercube(hdu, dimensions=[0, 1], slices=[]):
    '''
    Extract a slice from an n-dimensional FITS HDU, and return an HDU
    '''

    if type(slices) == int:
        slices = (slices, )
    else:
        slices = slices[:]

    shape = hdu.data.shape

    if len(shape) < 2:

        raise Exception("FITS file does not have enough dimensions")

    elif len(shape) == 2:

        if dimensions[1] < dimensions[0]:
            hdu.data = hdu.data.transpose()

        return hdu

    else:

        n_total = reduce(operator.mul, shape)
        n_image = shape[dimensions[0]] * shape[dimensions[1]]

        if n_total == n_image:
            slices = [0 for i in range(1, len(shape) - 1)]

        if slices:

            if dimensions[0] < dimensions[1]:
                slices.insert(dimensions[0], slice(None, None, None))
                slices.insert(dimensions[1], slice(None, None, None))
            else:
                slices.insert(dimensions[1], slice(None, None, None))
                slices.insert(dimensions[0], slice(None, None, None))

            if type(slices) == list:
                slices = tuple(slices)

            hdu.data = hdu.data[slices[::-1]]

            if dimensions[1] < dimensions[0]:
                hdu.data = hdu.data.transpose()

        else:

            message = '''
    Attempted to read in %i-dimensional FITS cube, but
    dimensions and slices were not specified. Please specify these
    using the dimensions= and slices= argument. The cube dimensions
    are:\n\n''' % len(shape)

            for i in range(1, len(shape) + 1):

                message += " " * 10
                message += " %i %s %i\n" % (i - 1,
                                            hdu.header["CTYPE%i" % i],
                                            hdu.header["NAXIS%i" % i])

            raise Exception(message)

        return hdu
