from __future__ import absolute_import, print_function, division


def slice_hypercube(data, header, dimensions=[0, 1], slices=[]):
    '''
    Extract a slice from an n-dimensional HDU data/header pair, and return the
    new data (without changing the header).
    '''

    if type(slices) == int:
        slices = (slices, )
    else:
        slices = slices[:]

    shape = data.shape

    if len(shape) < 2:

        raise Exception("FITS file does not have enough dimensions")

    elif len(shape) == 2:

        if dimensions[1] < dimensions[0]:
            data = data.transpose()

        return data

    else:

        if slices:

            if dimensions[0] < dimensions[1]:
                slices.insert(dimensions[0], slice(None, None, None))
                slices.insert(dimensions[1], slice(None, None, None))
            else:
                slices.insert(dimensions[1], slice(None, None, None))
                slices.insert(dimensions[0], slice(None, None, None))

            if type(slices) == list:
                slices = tuple(slices)

            data = data[slices[::-1]]

            if dimensions[1] < dimensions[0]:
                data = data.transpose()

        else:

            message = '''
    Attempted to read in %i-dimensional FITS cube, but
    dimensions and slices were not specified. Please specify these
    using the dimensions= and slices= argument. The cube dimensions
    are:\n\n''' % len(shape)

            for i in range(1, len(shape) + 1):

                message += " " * 10
                message += " %i %s %i\n" % (i - 1,
                                            header["CTYPE%i" % i],
                                            header["NAXIS%i" % i])

            raise Exception(message)

        return data
