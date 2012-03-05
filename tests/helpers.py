import string
import random
import os

import pyfits
import pywcs
import numpy as np


def random_id():
    return string.join(random.sample(string.letters + string.digits, 16), '')


def generate_header(header_file):

    # Read in header
    header = pyfits.Header()
    header.fromTxtFile(header_file)

    return header


def generate_data(header_file):

    # Read in header
    header = generate_header(header_file)

    # Find shape of array
    shape = []
    for i in range(header['NAXIS']):
        shape.append(header['NAXIS%i' % (i + 1)])

    # Generate data array
    data = np.zeros(shape[::-1])

    return data


def generate_hdu(header_file):

    # Read in header
    header = generate_header(header_file)

    # Generate data array
    data = generate_data(header_file)

    # Generate primary HDU
    hdu = pyfits.PrimaryHDU(data=data, header=header)

    return hdu


def generate_wcs(header_file):

    # Read in header
    header = generate_header(header_file)

    # Compute WCS object
    wcs = pywcs.WCS(header)

    return wcs


def generate_file(header_file, directory):

    # Generate HDU object
    hdu = generate_hdu(header_file)

    # Write out to a temporary file in the specified directory
    filename = os.path.join(directory, random_id() + '.fits')
    hdu.writeto(filename)

    print filename

    return filename
